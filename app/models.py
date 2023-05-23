from app.extensions import db
from datetime import datetime as d, timedelta as t


class Base:

    def create(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update(cls, id, **kwargs):
        cls.query.filter_by(id=id).update(kwargs)
        db.session.commit()


class UrlModel(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(250))
    shortened_url = db.Column(db.String(35))
    date = db.Column(
        db.DateTime(timezone=True),
        default=d.now() + t(30)
    )
    used = db.Column(db.Integer, default=0)
