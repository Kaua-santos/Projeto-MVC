# Instale o requirements.txt

```bash
pip install -r requirements.txt
```

# iniciar o alembic
```bash
python -m alembic init migrations
```


```bash
python -m alembic revision --autogenerate -m "Criar tabela usuarios"

```
# como rodar o codigo:
```bash
python -m uvicorn app.main:app --reload

```
python -m alembic upgrade head

