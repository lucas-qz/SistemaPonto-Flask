FROM python:3

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev

WORKDIR /app

RUN pip install Flask
RUN pip install Flask-SQLAlchemy
RUN pip install Flask-Migrate
RUN pip install Flask-Bcrypt
RUN pip install mysql-connector
RUN pip install mysql-connector-python
RUN pip install mysql
RUN pip install pytz
RUN pip install python-dotenv

COPY . . 
EXPOSE 5000

CMD ["python","./app.py"]