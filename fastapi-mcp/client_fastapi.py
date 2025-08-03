#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

client_fastapi.py
================
Cliente para interagir com a API de lembretes.
Este cliente permite realizar operações CRUD (Create, Read, Update, Delete)
nos lembretes armazenados na API.

Executar
========
uv run client_fastapi.py http://localhost:8000
"""
import asyncio
import json
from datetime import datetime
from typing import Optional, Dict, List, Any
import sys
import aiohttp

class FastAPIClient:
    def __init__(self):
        # Inicializa a sessão HTTP
        self.base_url = ""
        self.session = None

    async def connect_to_server(self, api_url: str):
        """Conecta ao servidor FastAPI

        Args:
            api_url: URL da API de lembretes
        """
        self.base_url = api_url
        self.session = aiohttp.ClientSession()
        
        # Verifica conexão com a API
        try:
            async with self.session.get(self.base_url) as response:
                data = await response.json()
                print("\n✅ Conectado à API de lembretes")
                print(f"Nome da API: {data.get('app')}")
                print(f"Versão: {data.get('version')}")
                print("Endpoints disponíveis:")
                for endpoint_name, endpoint_path in data.get('endpoints', {}).items():
                    print(f"  - {endpoint_name}: {endpoint_path}")
                return True
        except Exception as e:
            print(f"❌ Erro ao conectar à API: {str(e)}")
            return False

    async def create_reminder(self, title: str, description: Optional[str] = None, 
                            due_date: Optional[str] = None) -> Dict[str, Any]:
        """Cria um novo lembrete

        Args:
            title: Título do lembrete
            description: Descrição do lembrete (opcional)
            due_date: Data de vencimento no formato ISO (opcional)

        Returns:
            Lembrete criado
        """
        data = {"title": title}
        if description:
            data["description"] = description
        if due_date:
            data["due_date"] = due_date

        async with self.session.post(f"{self.base_url}/reminders/", json=data) as response:
            if response.status == 201:
                return await response.json()
            else:
                error = await response.text()
                raise Exception(f"Erro ao criar lembrete: {error}")

    async def get_all_reminders(self) -> List[Dict[str, Any]]:
        """Obtém todos os lembretes

        Returns:
            Lista de lembretes
        """
        async with self.session.get(f"{self.base_url}/reminders/") as response:
            if response.status == 200:
                return await response.json()
            else:
                error = await response.text()
                raise Exception(f"Erro ao obter lembretes: {error}")

    async def get_reminder(self, reminder_id: str) -> Dict[str, Any]:
        """Obtém um lembrete específico

        Args:
            reminder_id: ID do lembrete

        Returns:
            Lembrete solicitado
        """
        async with self.session.get(f"{self.base_url}/reminders/{reminder_id}") as response:
            if response.status == 200:
                return await response.json()
            else:
                error = await response.text()
                raise Exception(f"Erro ao obter lembrete: {error}")

    async def update_reminder(self, reminder_id: str, title: Optional[str] = None, 
                            description: Optional[str] = None, 
                            due_date: Optional[str] = None) -> Dict[str, Any]:
        """Atualiza um lembrete existente

        Args:
            reminder_id: ID do lembrete a ser atualizado
            title: Novo título (opcional)
            description: Nova descrição (opcional)
            due_date: Nova data de vencimento (opcional)

        Returns:
            Lembrete atualizado
        """
        data = {}
        if title:
            data["title"] = title
        if description is not None:  # Permite string vazia
            data["description"] = description
        if due_date is not None:
            data["due_date"] = due_date

        async with self.session.put(f"{self.base_url}/reminders/{reminder_id}", json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                error = await response.text()
                raise Exception(f"Erro ao atualizar lembrete: {error}")

    async def delete_reminder(self, reminder_id: str) -> bool:
        """Deleta um lembrete

        Args:
            reminder_id: ID do lembrete a ser deletado

        Returns:
            True se deletado com sucesso
        """
        async with self.session.delete(f"{self.base_url}/reminders/{reminder_id}") as response:
            if response.status == 204:
                return True
            else:
                error = await response.text()
                raise Exception(f"Erro ao deletar lembrete: {error}")

    async def format_reminder(self, reminder: Dict[str, Any]) -> str:
        """Formata um lembrete para exibição

        Args:
            reminder: Dados do lembrete

        Returns:
            String formatada
        """
        result = [
            f"ID: {reminder.get('id')}",
            f"Título: {reminder.get('title')}",
            f"Descrição: {reminder.get('description') or 'Nenhuma'}",
        ]
        
        if reminder.get('due_date'):
            due_date = reminder.get('due_date')
            result.append(f"Data de vencimento: {due_date}")
            
        if reminder.get('created_at'):
            created_at = reminder.get('created_at')
            result.append(f"Criado em: {created_at}")
            
        return "\n".join(result)

    async def interactive_loop(self):
        """Executa o loop interativo do cliente"""
        print("\n🔔 Cliente de Lembretes Iniciado 🔔")
        print("Digite um comando ou 'ajuda' para ver as opções disponíveis")
        print("\nExemplos de comandos:")
        print("  - 'listar' → Verifica se existem lembretes salvos")
        print("  - 'criar' → Cria um novo lembrete como 'Reunião de equipe'")
        print("  - 'buscar 550e8400-e29b-41d4-a716-446655440000' → Busca um lembrete específico")
        print("  - 'atualizar 550e8400-e29b-41d4-a716-446655440000' → Atualiza um lembrete existente")
        print("  - 'deletar 550e8400-e29b-41d4-a716-446655440000' → Remove um lembrete")
        
        while True:
            try:
                command = input("\nComando: ").strip().lower()
                
                if command == "quit" or command == "sair":
                    break
                    
                elif command == "ajuda" or command == "help":
                    print("\nComandos disponíveis:")
                    print("  criar - Criar um novo lembrete")
                    print("  listar - Listar todos os lembretes")
                    print("  buscar <id> - Buscar um lembrete específico")
                    print("  atualizar <id> - Atualizar um lembrete existente")
                    print("  deletar <id> - Deletar um lembrete")
                    print("  sair - Sair do programa")
                    print("\nExemplos:")
                    print("  - Para verificar se existem lembretes: 'listar'")
                    print("  - Para criar um lembrete para compras: 'criar' e siga as instruções")
                    print("  - Para buscar um lembrete: 'buscar 550e8400-e29b-41d4-a716-446655440000'")
                    
                elif command == "criar":
                    title = input("Título: ").strip()
                    if not title:
                        print("O título é obrigatório!")
                        continue
                    description = input("Descrição (opcional): ").strip()
                    due_date = input("Data de vencimento (AAAA-MM-DD HH:MM, opcional): ").strip()
                    
                    if due_date:
                        try:
                            # Converte para formato ISO
                            dt = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
                            due_date = dt.isoformat()
                        except ValueError:
                            print("Formato de data inválido! Use AAAA-MM-DD HH:MM")
                            continue
                    
                    reminder = await self.create_reminder(title, description, due_date)
                    print("\nLembrete criado com sucesso:")
                    print(await self.format_reminder(reminder))
                    print("\nDica: Anote o ID do lembrete para consultas futuras!")
                    
                elif command == "listar":
                    reminders = await self.get_all_reminders()
                    if not reminders:
                        print("Nenhum lembrete encontrado! Use 'criar' para adicionar um novo lembrete.")
                    else:
                        print(f"\nEncontrados {len(reminders)} lembretes:")
                        for i, reminder in enumerate(reminders, 1):
                            print(f"\n--- Lembrete {i} ---")
                            print(await self.format_reminder(reminder))
                            
                elif command.startswith("buscar "):
                    reminder_id = command.split(" ", 1)[1].strip()
                    try:
                        reminder = await self.get_reminder(reminder_id)
                        print("\nLembrete encontrado:")
                        print(await self.format_reminder(reminder))
                    except Exception as e:
                        print(f"Erro: {str(e)}")
                        print("Dica: Use o comando 'listar' para ver todos os lembretes disponíveis.")
                        
                elif command.startswith("atualizar "):
                    reminder_id = command.split(" ", 1)[1].strip()
                    try:
                        # Primeiro busca o lembrete para mostrar ao usuário
                        current = await self.get_reminder(reminder_id)
                        print("\nLembrete atual:")
                        print(await self.format_reminder(current))
                        
                        # Solicita novos valores
                        print("\nDigite os novos valores (deixe em branco para manter o valor atual):")
                        title = input(f"Título [{current.get('title')}]: ").strip()
                        description = input(f"Descrição [{current.get('description') or 'Nenhuma'}]: ").strip()
                        due_date = input(f"Data de vencimento [{current.get('due_date') or 'Nenhuma'}]: ").strip()
                        
                        # Prepara valores para atualização
                        update_title = title if title else None
                        update_description = description if description else None
                        update_due_date = None
                        if due_date:
                            try:
                                dt = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
                                update_due_date = dt.isoformat()
                            except ValueError:
                                print("Formato de data inválido! Use AAAA-MM-DD HH:MM")
                                continue
                        
                        # Atualiza apenas se algum valor foi fornecido
                        if any([update_title, update_description is not None, update_due_date is not None]):
                            reminder = await self.update_reminder(
                                reminder_id, update_title, update_description, update_due_date
                            )
                            print("\nLembrete atualizado com sucesso:")
                            print(await self.format_reminder(reminder))
                        else:
                            print("Nenhuma alteração realizada.")
                            
                    except Exception as e:
                        print(f"Erro: {str(e)}")
                        print("Dica: Use o comando 'listar' para ver todos os lembretes disponíveis.")
                        
                elif command.startswith("deletar "):
                    reminder_id = command.split(" ", 1)[1].strip()
                    try:
                        # Primeiro busca o lembrete para confirmar
                        try:
                            reminder = await self.get_reminder(reminder_id)
                            print("\nLembrete a ser deletado:")
                            print(await self.format_reminder(reminder))
                            
                            confirm = input("\nConfirmar exclusão? (s/n): ").strip().lower()
                            if confirm == "s":
                                await self.delete_reminder(reminder_id)
                                print("Lembrete deletado com sucesso!")
                            else:
                                print("Operação cancelada.")
                        except:
                            print(f"Lembrete com ID {reminder_id} não encontrado!")
                            print("Dica: Use o comando 'listar' para ver todos os lembretes disponíveis.")
                            
                    except Exception as e:
                        print(f"Erro: {str(e)}")
                        
                elif command == "tenho algum lembrete salvo" or command == "tenho lembretes":
                    print("Verificando lembretes salvos...")
                    reminders = await self.get_all_reminders()
                    if not reminders:
                        print("Você não tem nenhum lembrete salvo. Use 'criar' para adicionar um novo.")
                    else:
                        print(f"Sim! Você tem {len(reminders)} lembrete(s) salvo(s).")
                        print("Use o comando 'listar' para ver todos eles.")
                        
                elif command == "exemplos" or command == "exemplo":
                    print("\nExemplos de uso:")
                    print("1. Criar um lembrete para reunião:")
                    print("   > criar")
                    print("   > Título: Reunião de equipe")
                    print("   > Descrição: Discutir novos projetos")
                    print("   > Data: 2023-12-31 14:30")
                    print("\n2. Verificar lembretes existentes:")
                    print("   > listar")
                    print("\n3. Buscar um lembrete específico:")
                    print("   > buscar 550e8400-e29b-41d4-a716-446655440000")
                    print("\n4. Atualizar um lembrete:")
                    print("   > atualizar 550e8400-e29b-41d4-a716-446655440000")
                    print("\n5. Deletar um lembrete:")
                    print("   > deletar 550e8400-e29b-41d4-a716-446655440000")
                    
                else:
                    print("Comando desconhecido. Digite 'ajuda' para ver as opções disponíveis.")
                    print("Ou tente 'exemplos' para ver exemplos de uso.")
                    
            except Exception as e:
                print(f"\nErro: {str(e)}")
                
    async def cleanup(self):
        """Limpa recursos"""
        if self.session:
            await self.session.close()


async def main():
    if len(sys.argv) < 2:
        print("Uso: python client_fastapi.py <url_da_api>")
        print("Exemplo: python client_fastapi.py http://localhost:8000")
        sys.exit(1)

    client = FastAPIClient()
    try:
        api_url = sys.argv[1]
        connected = await client.connect_to_server(api_url)
        if connected:
            await client.interactive_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
