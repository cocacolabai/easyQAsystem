# coding: utf-8
from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model):
    userId = db.Column('userId', db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column('userName', db.String(16), nullable=False)
    userPassword = db.Column('userPassword', db.String(128), nullable=False)
    userEmail = db.Column('userEmail', db.String(30), nullable=True)
    userNickname = db.Column('userNickname', db.String(20), nullable=True)
    registerTime = db.Column('registerTime', db.DateTime, default=datetime.now())
    lastLoginTime = db.Column('lastLoginTime', db.DateTime, default=datetime.now())
    userBirth = db.Column('userBirth', db.String(20))
    userConfirmed = db.Column('userConfirmed', db.Boolean, default=False)
    __tablename__ = 't_user'

    def generate_confirmation_token(self, secret_key, expiration=3600):
        s = Serializer(secret_key, expiration)
        return s.dumps({'confirm': self.userId})

    def confirm(self, token, secret_key):
        s = Serializer(secret_key, 3600)
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.userId:
            return False
        self.userConfirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, user_password):
        self.userPassword = generate_password_hash(user_password)

    def verify_password(self, user_password):
        return check_password_hash(self.userPassword, user_password)

    def __repr__(self):
        return '<User %r>' % self.userId

    def __init__(self, user_name=None, user_password=None, user_email=None, user_nickname=None, register_time=None,
                 lastlogin_time=None,user_birth=None):
        self.userName = user_name
        self.password = user_password
        self.userEmail = user_email
        self.userNickname = user_nickname
        self.registerTime = register_time
        self.lastLoginTime = lastlogin_time
        self.userBirth = user_birth


class Question(db.Model):
    questionId = db.Column('questionId', db.Integer, primary_key=True, autoincrement=True)
    # userId = db.Column('userId', db.Integer, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('t_user.userId'))
    user = db.relationship('User', backref=db.backref('questions'))
    questionTopic = db.Column('questionTopic', db.String(100), nullable=False)
    questionContent = db.Column('questionContent', db.String(2000), nullable=False)
    questionTime = db.Column('questionTime', db.DateTime, default=datetime.now())
    questionView = db.Column('questionView', db.Integer, default=0)
    # questionLike = db.Column('questionLike', db.Integer, default=0)
    __tablename__ = 't_question'

    def __repr__(self):
        return '<Question %r>' % self.questionId


class Answer(db.Model):
    answerId = db.Column('answerId', db.Integer, primary_key=True, autoincrement=True)
    # foreign key userId
    userId = db.Column(db.Integer, db.ForeignKey('t_user.userId'))
    user = db.relationship('User', backref=db.backref('answers'))
    # foreign key postId
    questionId = db.Column(db.Integer, db.ForeignKey('t_question.questionId'))
    question = db.relationship('Question', backref=db.backref('answers'))

    answerContent = db.Column('answerContent', db.String(500), nullable=False)
    answerTime = db.Column('answerTime', db.DateTime, default=datetime.now())
    __tablename__ = 't_answer'

    def __repr__(self):
        return '<Answer %r>' % self.answerId

    def __init__(self, question_id=None, user_id=None, answer_content=None, answer_time=None):
        self.questionId = question_id
        self.userId = user_id
        self.answerContent = answer_content
        self.answerTime = answer_time


class Like(db.Model):
    likeId = db.Column("likeId", db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey("t_user.userId"))
    user = db.relationship("User", backref=db.backref("likes"))
    questionId = db.Column(db.Integer, db.ForeignKey("t_question.questionId"))
    question = db.relationship("Question", backref=db.backref("likes"))
    likeTime = db.Column("likeTime", db.DateTime, default=datetime.now())
    # likeType = db.Column("likeType", db.Integer, default=0)  # 0 question 1 answer
    __tablename__ = "t_like"

    def __repr__(self):
        return '<Like %r>' % self.likeId

    def __init__(self, user_id=None, questin_id=None, like_time=None):
        self.userId = user_id
        self.questionId = questin_id
        self.likeTime = like_time
