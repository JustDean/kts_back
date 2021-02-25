FROM python:3.8-buster as bot_builder

WORKDIR /the_app

COPY . .
RUN pip install -requirment.txt
CMD ["sh", "-c", "/run.sh"]