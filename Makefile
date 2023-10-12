.PHONY: server

server:
	ip_addr="${DATABASE_API_IP_ADDRESS:"0.0.0.0"}"
	gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind ${DATABASE_API_IP_ADDRESS}:8001