FROM python:3.6.10

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP="app:app"

CMD [ "flask", "run", "--host=0.0.0.0", "--port=80"]