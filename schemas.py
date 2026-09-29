from pydantic import BaseModel, Field
from typing import Optional, List


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes = True
        

class Loginschema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor : str
    tamanho : str
    preco_unitario: float

    class Config:
        from_attributes = True


class ResponsePedidoSchema(BaseModel):
    id: int
    status : str
    preco : float
    itens: List[ItemPedidoSchema] = Field(validation_alias="items")

    class Config:
            from_attributes = True