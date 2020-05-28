from datetime import datetime
from flaskstudy1 import db,loginManager
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(userID):
    return User.query.get(int(userID))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(20),unique=True, nullable=False)
    avatar = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post',backref='HTs',lazy=True)
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.avatar}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    postDate = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    userID = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
        return f"User('{self.title}','{self.postDate}')" #'{self.content}' Later