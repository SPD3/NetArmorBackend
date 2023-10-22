FROM python:3.8.10
WORKDIR /net_armor
RUN apt-get update -y
RUN apt-get install -y inotify-tools
COPY ./requirements.txt /net_armor/requirements.txt
RUN pip install -r /net_armor/requirements.txt
# COPY . .
CMD ["make", "server"]
