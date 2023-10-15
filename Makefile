.PHONY: server

server:
	gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind ${DATABASE_API_HOST_NAME}:${DATABASE_API_PORT}