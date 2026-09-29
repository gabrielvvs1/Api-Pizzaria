#aqui é criado as classes do banco de dados, que são as tabelas do banco de dados
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

#cria a concexão com o banco
db = create_engine("sqlite:///banco.db")

#cria abase do banco de dados
Base = declarative_base()

#cria as classes/tabelas do banco
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer,nullable=False, primary_key=True,autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String,nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


#Pedido
class Pedido(Base):
    __tablename__ = "pedidos"

    #STATUS_PEDIDOS = (
    #    ("PENDENTE", "PENDENTE"),
    #    ("CANCELADO", "CANCELADO"),
    #    ("FINALIZADO", "FINALIZADO")
    #)

    id = Column("id", Integer,nullable=False, primary_key=True,autoincrement=True)
    status = Column("status", String) #pendente, cancelado, finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float )
    items = relationship("ItensPedido", cascade="all, delete")

    def __init__(self, usuario, status = "PENDENTE", preco = 0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.items)



class ItensPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer,nullable=False, primary_key=True,autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido


#executa a criação dos metadados do banco (cria efetivamente o banco de dados)


#criar migraçao do db: alembic revision --autogenerate -m "mensagem"
#executar a migracao: alembic upgrade head