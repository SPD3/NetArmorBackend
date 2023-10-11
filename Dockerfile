FROM python:3.8.10
WORKDIR /net_armor
COPY ./requirements.txt /net_armor/requirements.txt
RUN pip install -r /net_armor/requirements.txt
COPY ./src /net_armor/src
CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001"]
