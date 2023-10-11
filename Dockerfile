FROM python:3.8.10
WORKDIR /net_armor
COPY ./requirements.txt /net_armor/requirements.txt
RUN pip install -r /net_armor/requirements.txt
COPY . .
CMD ["make", "server"]
