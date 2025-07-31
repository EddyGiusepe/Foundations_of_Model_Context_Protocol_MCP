from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid
from fastapi_mcp import FastApiMCP

# Metadados da API aprimorados:
app = FastAPI(
    title="Reminders API",
    description="Uma API simples para gerenciar lembretes com operações CRUD",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

mcp = FastApiMCP(app)

#mcp.mount()
# Mount the MCP server to the FastAPI app
mcp.mount_http()


# Conexão MongoDB:
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient("mongodb://mongodb:27017")
    app.mongodb = app.mongodb_client["reminders_db"]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Modelos Pydantic:
class ReminderBase(BaseModel):
    title: str = Field(..., description="O título do lembrete", example="Comprar alimentos")
    description: Optional[str] = Field(None, description="Descrição detalhada do lembrete", example="Leite, ovos, pão")
    due_date: Optional[datetime] = Field(None, description="Data de vencimento do lembrete", example="2023-12-31T12:00:00")

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Identificador único para o lembrete")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp de quando o lembrete foi criado")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Comprar comestíveis",
                "description": "Leite, ovos, pão",
                "due_date": "2023-12-31T12:00:00",
                "created_at": "2023-12-01T09:30:00"
            }
        }

# Endpoint raiz com informações da API:
@app.get("/", tags=["Raiz"])
async def root():
    """
    Endpoint raiz que retorna informações básicas da API e endpoints disponíveis.
    """
    return {
        "app": "API de Lembretes",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "create_reminder": "POST /reminders/",
            "get_all_reminders": "GET /reminders/",
            "get_reminder": "GET /reminders/{reminder_id}",
            "update_reminder": "PUT /reminders/{reminder_id}",
            "delete_reminder": "DELETE /reminders/{reminder_id}"
        }
    }

# Operações CRUD com documentação aprimorada:
@app.post(
    "/reminders/", 
    response_model=Reminder, 
    status_code=status.HTTP_201_CREATED,
    tags=["Reminders"],
    summary="Criar um novo lembrete",
    description="Criar um novo lembrete com o título fornecido, descrição opcional e data de vencimento opcional."
)
async def create_reminder(reminder: ReminderCreate):
    """
    Criar um novo lembrete com os seguintes parâmetros:
    
    - **title**: Título obrigatório do lembrete
    - **description**: Descrição opcional com detalhes
    - **due_date**: Data de vencimento opcional
    
    Retorna o lembrete criado com o ID gerado e a timestamp de criação.
    """
    new_reminder = Reminder(
        title=reminder.title,
        description=reminder.description,
        due_date=reminder.due_date
    )
    await app.mongodb["reminders"].insert_one(new_reminder.model_dump())
    return new_reminder

@app.get(
    "/reminders/", 
    response_model=List[Reminder],
    tags=["Reminders"],
    summary="Obter todos os lembretes",
    description="Obter uma lista de todos os lembretes armazenados na base de dados."
)
async def read_reminders():
    """
    Obter todos os lembretes.
    
    Retorna uma lista de todos os lembretes armazenados na base de dados (limitado a 1000 entradas).
    """
    reminders = await app.mongodb["reminders"].find().to_list(1000)
    return reminders

@app.get(
    "/reminders/{reminder_id}", 
    response_model=Reminder,
    tags=["Reminders"],
    summary="Obter um lembrete específico",
    description="Obter um lembrete específico pelo seu ID."
)
async def read_reminder(reminder_id: str):
    """
    Obter um lembrete específico pelo seu ID.
    
    - **reminder_id**: O identificador único do lembrete
    
    Retorna o lembrete se encontrado, caso contrário, retorna um erro 404.
    """
    reminder = await app.mongodb["reminders"].find_one({"id": reminder_id})
    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Lembrete com ID {reminder_id} não encontrado"
        )
    return reminder

@app.put(
    "/reminders/{reminder_id}", 
    response_model=Reminder,
    tags=["Reminders"],
    summary="Atualizar um lembrete",
    description="Atualizar um lembrete existente pelo seu ID com novos dados."
)
async def update_reminder(reminder_id: str, reminder: ReminderBase):
    """
    Atualizar um lembrete existente pelo seu ID com novos dados.
    
    - **reminder_id**: O identificador único do lembrete a ser atualizado
    - **reminder**: Os novos dados do lembrete
    
    Retorna o lembrete atualizado se encontrado, caso contrário, retorna um erro 404.
    """
    update_result = await app.mongodb["reminders"].update_one(
        {"id": reminder_id},
        {"$set": reminder.model_dump()}
    )
    
    if update_result.modified_count == 0:
        reminder_exists = await app.mongodb["reminders"].find_one({"id": reminder_id})
        if not reminder_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Lembrete com ID {reminder_id} não encontrado"
            )
        
    updated_reminder = await app.mongodb["reminders"].find_one({"id": reminder_id})
    return updated_reminder

@app.delete(
    "/reminders/{reminder_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Reminders"],
    summary="Deletar um lembrete",
    description="Deletar um lembrete existente pelo seu ID."
)
async def delete_reminder(reminder_id: str):
    """
    Deletar um lembrete existente pelo seu ID.
    
    - **reminder_id**: O identificador único do lembrete a ser deletado
    
    Retorna no content (204) se bem sucedido, caso contrário, retorna um erro 404.
    """
    delete_result = await app.mongodb["reminders"].delete_one({"id": reminder_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Lembrete com ID {reminder_id} não encontrado"
        )
    return None 

# But if you re-run the setup, the new endpoints will now be exposed.
mcp.setup_server()

