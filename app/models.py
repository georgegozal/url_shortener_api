from app.extensions import db
from datetime import datetime as d, timedelta as t
from werkzeug.security import generate_password_hash, check_password_hash


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


class User(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, index=True)
    password_hash = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    pro_user = db.Column(db.String(4), default=False)
    urls = db.relationship('UrlShort', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class UrlShort(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    url_original = db.Column(db.String(250))
    url_shortened = db.Column(db.String(35))
    date = db.Column(
        db.DateTime(timezone=True),
        default=d.now() + t(30)
    )
    used = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
