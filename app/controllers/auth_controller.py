from fastapi import APIRouter, Depends, Request, Form,status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.auth import hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

templates = Jinja2Templates(directory="app/templates")

# rota de cadastro 
@router.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/cadastro.html",
        {"request": request}
    )

# exibir tela de login 
@router.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {'request': request}
    )

# criar o usuario no banco - cadastrar usuario
@router.post("/cadastro")
def cadastrar_user(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    # verificar se o e-mail está cadastrado
    user_existente = db.query(Usuario).filter_by(email=email).first()

    if user_existente:
        # retorna o formulario com mensagem de erro
        return templates.TemplateResponse(
            request,
            "auth/cadastro",
            {"request": request, "erro": "este e-mail ja esta cadastrado"}
        )
    
    # criar um novo usuario com senha hash
    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=hash_senha(senha)
    )
    # adicionar o novo usuario ao banco de dados
    db.add(novo_usuario)
    db.commit()
    # redirecionar para a tela de login
    return RedirectResponse(url="/auth/login?cadastro=ok", status_code=302)