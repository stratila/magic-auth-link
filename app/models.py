from app import db, login
from flask_login import UserMixin
from datetime import datetime, timedelta
import app
import jwt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    counter = db.Column(db.Integer, index=True, default=int)
    auth_link = db.Column(db.String(256))

    def generate_auth_link(self, expiration):
        # for generating token we use JSON Web Token library
        self.auth_link = jwt.encode({'exp': datetime.utcnow() + timedelta(seconds=expiration), 'user_id': self.id},
                                    app.app.config['SECRET_KEY'], algorithm='HS256')
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def verify_auth_link(auth_link):
        try:
            decoded_data = jwt.decode(auth_link, app.app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(decoded_data['user_id'])
            return user
        except jwt.exceptions.ExpiredSignatureError:
            return None
        except jwt.exceptions.InvalidTokenError:
            return None


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def get_or_create(session, model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance




