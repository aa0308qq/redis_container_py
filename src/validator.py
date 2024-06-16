from pydantic import BaseModel


class ConnectionInfo(BaseModel):
    password: str
    host: str
    port: int


class DatabaseConfig(BaseModel):
    image_name: str
    container_name: str
    connection_info: ConnectionInfo
