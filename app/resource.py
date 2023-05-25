import random
import string
from datetime import datetime

from flask import redirect, request
from flask_restful import Resource, reqparse

from app.extensions import db
from app.models import UrlModel


class UrlResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'url',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def get(self, short_url=None):
        if short_url is None:
            docs = {
                'message': 'Welcome to the URL Shortener API',
                'endpoints': {
                    'GET https://base_url/<string>': 'Redirects to the original URL',
                    'POST https://base_url/': 'Creates a shortened URL. Send data as JSON: {"url": "https://www.example.com"}'
                }
            }
            return docs, 200

        else:
            # check and update database, remove old rows
            UrlResource.filter_database(short_url)
            short_url = UrlModel.query.filter_by(shortened_url=short_url).first()
            # print(short_url)
            if short_url:
                short_url.used += 1
                db.session.commit()
                return redirect(short_url.original_url, 302)
            else:
                return {
                    "status": "error",
                    "message": "Url not found"
                }, 404

    def post(self):
        data = UrlResource.parser.parse_args()
        original_url = data['url']
        check_url = UrlModel.query.filter_by(original_url=original_url).first()
        if check_url:
            return {
                "status": "error",
                "message": "Url already exists",
                "result": request.url + check_url.shortened_url
            }, 409

        # get random sufix
        while True:
            shortened_url = UrlResource.get_random()
            check_sufix = UrlModel.query.filter_by(shortened_url=shortened_url).first()
            if not check_sufix:
                break
        # add new urls in database model
        new_shortened_url = UrlModel()
        new_shortened_url.create(
            original_url=original_url,
            shortened_url=shortened_url,
        )
        new_shortened_url.save()
        return {
            "status": "success",
            "message": "Shortened URL created successfully",
            "result": request.url + shortened_url
        }, 201

    @staticmethod
    def filter_database(short_url):
        now = datetime.now()
        shortened_url = UrlModel.query.filter_by(shortened_url=short_url).first()
        if shortened_url and shortened_url.date < now:
            db.session.delete(shortened_url)
            db.session.commit()

    @staticmethod
    def get_random():
        alfabet = string.ascii_lowercase
        nums = "0123456789" * 2
        return ''.join(random.choices(alfabet + nums, k=5))
