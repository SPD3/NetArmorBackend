FROM python:3.8.10
WORKDIR /net_armor
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]