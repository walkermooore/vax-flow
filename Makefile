run:
	uv run fastapi run app/main.py --port 8000 --host 0.0.0.0

# Esse comando cria o arquivo das migrations. Sempre que alterar algum model rode:
# make migration d="add status to vacinas"
migration:
	uv run alembic revision --autogenerate -m "$(d)"

# Esse comando adiciona o estado atual das migrations no banco
stamp:
	uv run alembic stamp head

# Após criar a versão rode:
# make migrate
migrate:
	uv run alembic upgrade head

# Parametro d= :
# base = Volta ao inicio
# -n = Volta a quantidade especificada em d de migrations no banco
# head = Volta ao inicio e up denovo
downgrade:
	uv run alembic downgrade $(d)

# Apenas vê as migrations
history:
	uv run alembic history

# Gera openapi.json para desenvolvimento
# Copiar este arquivo gerado para o repositório APP local
# Não precisa rodar esse comando, só se quiser debugar algo, o hey-api gera o client baseado na url local
openapi:
	uv run python -c "import api.main; import json; print(json.dumps(api.main.app.openapi()))" > openapi.json