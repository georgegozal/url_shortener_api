FROM python:3.10.7-alpine3.16

RUN mkdir /usr/src/flask_url_shortener
WORKDIR /usr/src/flask_url_shortener

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy everything to the flask_app directory
COPY . . 

ENV FLASK_APP=app \
    FLASK_ENV=production

EXPOSE 5000

# CMD ["flask", "run", "--host=0.0.0.0"] 
CMD ["python", "app.py"]