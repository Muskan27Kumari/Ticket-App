from bson import ObjectId
from fastapi import HTTPException, status
from datetime import datetime
from app.database import db
from app.services.auth import AuthService
from app.models.client import ClientModel

class ClientService:
    collection = db.clients

    @staticmethod
    def create_client(client_data: dict):
        if ClientService.collection.find_one({"name": client_data["name"]}):
            raise HTTPException(status_code=400, detail="Client name already registered")
        client_data["password"] = AuthService.get_password_hash(client_data["password"])
        client_model = ClientModel(**client_data)
        result = ClientService.collection.insert_one(client_model.dict(exclude={"id"}))
        return str(result.inserted_id)

    # Similar methods for get_clients, get_client, update_client, delete_client
    # Omitted for brevity; mirror UserService but without tickets