from app.database import Session, engine, Base
from app.models.usuario import Usuario
from app.auth import hash_senha

usuarios = [
    {
        "nome": "admin",
      "email": "admin@teste.com", 
      "senha": "admin@1234", 
      "role": "admin"},
    {
        "nome": "kaua",
        "email": "kaua@teste.com",
        "senha": "admin@1234",
        "role": "admin"
    }
]

def criar_usuarios():
    db = Session()

    try:
        for usuario in usuarios:
            # verificar se o usuario ja existe
            existe = db.query(Usuario).filter_by(email=usuario["email"]).first()

            if existe:  
                print(f"Usuario {usuario['email']} ja existe")
                continue
            else:
                novo_usuario = Usuario(
                    nome=usuario["nome"],
                    email=usuario["email"],
                    senha_hash=hash_senha(usuario["senha"]),
                    role=usuario["role"]
                )
                db.add(novo_usuario)
        db.commit()
        print(f"Usuarios criados com sucesso")
        
    except Exception as erro:
        db.rollback()
        print(erro)
    finally:
        db.close()

# chamar a função
criar_usuarios()

