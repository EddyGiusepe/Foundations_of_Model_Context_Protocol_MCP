import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Se você modificar estes escopos, delete o arquivo token.json.
SCOPES = ["https://www.googleapis.com/auth/documents"]

def create_document(title: str="Placeholder", text: str="Placeholder") -> str:
    """Cria um novo documento com o título 'example' e o texto 'made with API'."""
    creds = None
    # O arquivo token.json armazena os tokens de acesso e atualização do usuário, e é
    # criado automaticamente quando o fluxo de autorização é concluído pela primeira vez.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # Se não houver credenciais válidas disponíveis, permita que o usuário faça login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Salve as credenciais para a próxima execução:
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("docs", "v1", credentials=creds)

        # Crie um novo documento
        document = {
            'title': title
        }
        doc = service.documents().create(body=document).execute()
        print(f'Created document with title: {doc.get("title")}')
        
        # Obtenha o ID do documento
        document_id = doc.get('documentId')
        
        # Adicione o corpo de texto ao documento:
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': text
                }
            }
        ]
        
        service.documents().batchUpdate(
            documentId=document_id, body={'requests': requests}).execute()
        
        print(f'Texto adicionado ao documento. ID do documento: {document_id}')
        return "Documento criado com sucesso."
        
    except HttpError as err:
        print(err)
        return f"Ocorreu um erro: {err}"


if __name__ == "__main__":
    create_document("Made with API", "Este documento foi criado e modificado usando a API do Google Docs.")