FROM python:3.10.7-alpine3.16

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


ENV FLASK_APP=main.py
ENV FLASK_ENV=production

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 5000

# copy project
COPY . /usr/src/app/

COPY gunicorn.sh /usr/src/app/gunicorn.sh
RUN chmod +x /usr/src/app/gunicorn.sh

ENTRYPOINT ["/usr/src/flask_url_shortener/gunicorn.sh"]