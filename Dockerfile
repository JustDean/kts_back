FROM python:3.8-buster as bot_builder

WORKDIR /the_app
RUN apt update && apt -y install gettext-base
COPY . .
RUN pip install -r requirments.txt
CMD ["bash", "/the_app/run.sh"]