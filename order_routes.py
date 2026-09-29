from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItensPedido
from typing import List


order_router = APIRouter(prefix="/pedidos", tags=["Pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    """
    Essa é rota padrão de pedidos do sistema, todas as rotas do pedidos precisam de autenticação
    """
    return {"mensagem":"Voce acessou a rota de pedidos"}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """Cria um novo pedido com o usuário informado e retorna seu identificador."""
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso - ID do Pedido: {novo_pedido.id}"}


#Cancelamento do pedido
@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    """Cancela um pedido existente; somente o administrador ou seu dono pode fazê-lo."""
    #usuario.admin = true
    #usuario.id = dono do pedido
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para cancelar pedido")
    pedido.status= "CANCELADO"
    session.commit()
    return{
        "mensagem": f"Pedido numero:{id_pedido} cancelado com sucesss",
        "pedido": pedido
    }


@order_router.get("/listar", response_model=List[ResponsePedidoSchema]) #listar pedidos
async def listar_pedidos(session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    """Lista todos os pedidos; acesso permitido somente a administradores."""
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa operação")
    else:
        pedidos = session.query(Pedido).all()
        return pedidos

@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema:ItemPedidoSchema, 
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    """Adiciona um item ao pedido e atualiza o preço; somente o administrador ou seu dono pode fazê-lo."""
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existe")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa operação")
    item_pedido = ItensPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor,
                              item_pedido_schema.tamanho, item_pedido_schema.preco_unitario,
                              id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem": "Item criado com sucess",
        "item_id" : item_pedido.id,
        "preco_pedido": pedido.preco
    }


@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int,
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    """Remove um item do pedido e recalcula o preço; somente o administrador ou seu dono pode fazê-lo."""

    item_pedido = session.query(ItensPedido).filter(ItensPedido.id == id_item_pedido).first()

    if not item_pedido:
        raise HTTPException(status_code=404, detail="Item no pedido não existe")

    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa operação")

    session.delete(item_pedido)
    session.flush()
    pedido.calcular_preco()
    session.commit()

    return {
        "mensagem": "Item removido com sucesso",
        "quantidade_itens_pedido": len(pedido.items),
        "preco_pedido": pedido.preco,
        "pedido": pedido
    }


#FINALIZAr um pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    """Finaliza um pedido existente; somente o administrador ou seu dono pode fazê-lo."""
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para cancelar pedido")
    pedido.status= "FINALIZADO"
    session.commit()
    return{
        "mensagem": f"Pedido numero:{pedido.id} finalizado com sucesss",
        "pedido": pedido
    }

#Visualizar um pedido
@order_router.get("/pedido/{id_pedido}")
async def vizualizar_pedido(id_pedido:int,  session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)): 
    """Exibe os detalhes de um pedido; somente o administrador ou seu dono pode visualizá-lo."""
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para cancelar pedido")
    return{
        "quantidade_itens_pedido": len(pedido.items),
       "pedido": pedido

    }


#Visualizar todos os pedidos de um UNICO usuario
@order_router.get("/listar/pedidos-usuario", response_model=List[ResponsePedidoSchema]) 
async def listar_pedidos(session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    """Lista os pedidos pertencentes ao usuário autenticado."""
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
    return pedidos
