import random
import string
from datetime import datetime

from flask import jsonify, redirect, request, make_response
from flask_login import current_user
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

    def get(self, short_url):
        # check and update database, remove old rows
        UrlResource.filter_database(short_url)
        short_url = UrlModel.query.filter_by(shortened_url=short_url).first()
        # print(short_url)
        if short_url:
            short_url.used += 1
            db.session.commit()
            return redirect(short_url.original_url, 302)
        else:
            return make_response(jsonify(msg="Url not found"), 404)

    def post(self):
        data = UrlResource.parser.parse_args()
        original_url = data['url']
        check_url = UrlModel.query.filter_by(original_url=original_url).first()
        if check_url:
            return make_response(jsonify({
                "error": "Url already exists",
                "msg": request.url + check_url.shortened_url
            }), 409)

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
        return make_response(jsonify(
            success="Shortened url has been created",
            message=request.url + shortened_url), 201)

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

            #         # get random sufix
            #         url_shortened = get_changed_url(UrlModel, request)
            #         # add new urls in database model
            #         add_to_database = UrlModel(
            #             url_original=url_original,
            #             url_shortened=url_shortened,
            #             user_id=current_user.id
            #         )
            # except AttributeError:
            #     url_shortened = get_changed_url(UrlModel, request)
            #     add_to_database = UrlModel(
            #         url_original=url_original,
            #         url_shortened=url_shortened
            #     )
            # db.session.add(add_to_database)
            # db.session.commit()
            # url_shortened = UrlModel.query.order_by(UrlModel.id.desc()).first()

# @url_short.route('/urls', methods=['GET'])
# def get_public_urls():

#     urls = UrlModel.query.filter_by(user=None).all()
#     urls_list = []
#     for url in urls:
#         u = {
#             "id": url.id,
#             "url_original": url.url_original,
#             "url_shortened": url.url_shortened,
#         }
#         urls_list.append(u)
#     return jsonify(urls_list)

# # get all urls
# @api.route('/api/urls', methods=['GET'])
# def get_all_urls():
#     db_query = UrlShort.query.all()
#     urls_list = []
#     for url in db_query:
#         u = {
#             "id": url.id,
#             "url_original": url.url_original,
#             "url_shortened": url.url_shortened,
#         }
#         urls_list.append(u)
#     return jsonify(urls_list)
