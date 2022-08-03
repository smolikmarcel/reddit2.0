from traitlets import default
from reddit_2 import db, login_manager
from datetime import datetime
from reddit_2 import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_subreddit = db.Table('user_subreddit',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('subreddit_id', db.Integer, db.ForeignKey('subreddit.id'))
                    )


user_submission_like = db.Table('user_submission_like',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('submission_id', db.Integer, db.ForeignKey('submission.id')),
                    )
user_submission_dislike = db.Table('user_submission_dislike',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('submission_id', db.Integer, db.ForeignKey('submission.id')),
                    )


user_comment_like = db.Table('user_comment_like',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id')),
                    )
user_comment_dislike = db.Table('user_comment_dislike',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id')),
                    )





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    img = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    age = db.Column(db.Integer)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    
    #comments backref
    comments = db.relationship('Comment', backref='user_comments', lazy=True)
    #submissions backref
    submissions = db.relationship('Submission', backref='user_submissions', lazy=True)
    #subreddit backref
    subreddits = db.relationship('Subreddit', backref='user_subreddits', lazy=True)


    joined_subreddits = db.relationship('Subreddit', secondary=user_subreddit, backref='user_subreddit')
    
    liked_submissions_like = db.relationship('Submission', secondary=user_submission_like, backref='user_submission_like')
    liked_submissions_dislike = db.relationship('Submission', secondary=user_submission_dislike, backref='user_submission_dislike')

    liked_comments_like    = db.relationship('Comment', secondary=user_comment_like, backref='user_comment_like')
    liked_comments_dislike = db.relationship('Comment', secondary=user_comment_dislike, backref='user_comment_dislike')


    @property
    def password_hash(self):
        return self.password

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    def __repr__(self):
        return f'<User {self.firstname}>'



class Subreddit(db.Model):
    id = db.Column(db.String(30), primary_key=True)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    public_description = db.Column(db.Text)

    subreddit_logo = db.Column(db.String(100), default='default_subreddit_logo.png', nullable=False)
    subreddit_img = db.Column(db.String(100), default='default_subreddit_img.png', nullable=False)

    subscribers = db.Column(db.Integer, default=0)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    #author_ref = db.relationship("User", backref=db.backref("user_ref", uselist=False))

    #Submissions backref
    submissions = db.relationship('Submission', backref='subreddit_submissions', lazy=True)



class Submission(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    title = db.Column(db.String(256), default="")
    selftext = db.Column(db.Text, default="")

    score = db.Column(db.Integer, default=0)
    url = db.Column(db.String(256), default="default_submission_img.png")

    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    #author_ref = db.relationship("User", backref=db.backref("author_ref", uselist=False))

    subreddit = db.Column(db.String(30), db.ForeignKey('subreddit.id'))
    #subreddit_ref = db.relationship("Subreddit", backref=db.backref("subreddit_ref", uselist=False))

    thread_id = db.Column(db.String(30), db.ForeignKey('comment.id'))
    #thread_ref = db.relationship("Comment", backref=db.backref("comment_ref", remote_side=[id], uselist=False))




class Comment(db.Model):
    id = db.Column(db.String(30), primary_key=True)

    text = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    score = db.Column(db.Integer, default=0)
    
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_ref = db.relationship("User", backref=db.backref("author_ref", uselist=False))
    submission = db.Column(db.String(30), db.ForeignKey('submission.id'))

    parent_id = db.Column(db.String(30), db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')