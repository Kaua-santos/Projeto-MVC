# 1. Hash e verificação de senhas bcrypt
# 2. Gerção do token JWT
# 3. Leitura e validação do token vindo do cookiie

from datetime import datetime, timedelta, timezone
from jose import JWSError, jwt
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv
import os

# Carregar as variaveis de ambiente
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRAÇAO_MINUTOS = os.getenv("ACCESS_TOKEN_EXPIRAÇAO_MINUTOS")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# funçoes de senha 
def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)

# funçoes do token 
def criar_token(data: dict):
    
    payload = data.copy()
    # Define quando o token expira 
    expira = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRAÇAO_MINUTOS))
    payload.update({"exp": expira})

    # criar o token 
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decodificar_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

# dependencia fastapi
def get_usuario_logado(request: Request):
    token = request.cookies.get("acess_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nao autenticado"
        )
    try:
        payload = decodificar_token(token)
        email = payload.get("sub")

        if email is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalido")
        
        return payload 
    except JWSError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido ou expirado"
        )
    
def get_usuario_opcional(request: Request):
    try:
        return get_usuario_logado(request)
    except HTTPException:
        None

# Dependencia do fastapi para administradore
def get_admin(request: Request):
    ususario = get_usuario_logado(request)

    if ususario.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso apenas para administradores"
        )
    return ususario
