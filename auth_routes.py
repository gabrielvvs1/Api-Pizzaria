from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import false
from dependencies import pegar_sessao, verificar_token
from models import Usuario, db
from sqlalchemy.orm import sessionmaker
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, Loginschema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)): #JWT
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get("/")
async def home():
    """
    Essa é rota padrão de autenticação o sistema
    """
    return {"mensagem": "Voce acessou a rota de padraao de autenticação", "autenticado":False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)): #cria uma sessao do banco de dados
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        #ja existe um usuario com esse email 
        raise HTTPException(status_code=400, detail="Email do usuário já está cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)  # Criptografa a senha usando bcrypt
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)  # Cria um novo usuário com a senha criptografada
        session.add(novo_usuario)   
        session.commit()
        return {"mensagem": f"Usuario criado com sucesso {usuario_schema.email}"}
    

#rota de login com token login > email e senha > token jwt 
@auth_router.post("/login")
async def login(login_schema: Loginschema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == login_schema.email).first()
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
                "access_token": access_token,
                "refresh_token":refresh_token,
                "token_type": "Bearer"
            
                }


#Formulario
@auth_router.post("/login-form")
async def login_form(dados_formularios : OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formularios.username, dados_formularios.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
                "access_token": access_token,
                "token_type": "Bearer"
            
                }
    

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    #verifica o token
    access_token = criar_token(usuario.id)
    return {
                "access_token": access_token,
                "token_type": "Bearer"
                
            }
    