import random
import string
from datetime import datetime

from flask import redirect, request
from flask_restful import Resource, reqparse
from urllib.parse import urljoin

from app.extensions import db
from app.models import UrlModel


class UrlResource(Resource):
    # decorators = [cross_origin]
    parser = reqparse.RequestParser()
    parser.add_argument(
        'url',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def get(self, short_url=None):
        if short_url is None:
            return redirect('/swagger', 302)
        # check and update database, remove old rows
        UrlResource.filter_database(short_url)
        short_url = UrlModel.query.filter_by(shortened_url=short_url).first()
        if short_url:
            short_url.used += 1
            db.session.commit()
            return redirect(short_url.original_url, 302)
        else:
            return {
                "status": "error",
                "message": "Url not found",
                "request_url": urljoin(request.url, short_url)
            }, 404

    def post(self):
        data = UrlResource.parser.parse_args()
        original_url = data['url']
        check_url = UrlModel.query.filter_by(original_url=original_url).first()
        if check_url:
            return {
                "status": "error",
                "message": "Url already exists",
                "result": urljoin(request.url, check_url.shortened_url)
            }, 409

        # get random suffix
        while True:
            shortened_url = UrlResource.get_random()
            check_suffix = UrlModel.query.filter_by(shortened_url=shortened_url).first()
            if not check_suffix:
                break

        # add new URLs in the database model
        new_shortened_url = UrlModel()
        new_shortened_url.create(
            original_url=original_url,
            shortened_url=shortened_url,
        )
        new_shortened_url.save()

        return {
            "status": "success",
            "message": "Shortened URL created successfully",
            "result": urljoin(request.url, shortened_url)
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
        alphabet = string.ascii_lowercase
        nums = "0123456789" * 2
        return ''.join(random.choices(alphabet + nums, k=5))
