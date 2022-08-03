from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, HiddenField, FileField 
from wtforms.validators import Length, EqualTo, Email, DataRequired




class RegisterForm(FlaskForm):


    username = StringField(label='username', validators=[Length(min=2, max=30), DataRequired()])
    firstname = StringField(label='firstname', validators=[Length(min=2, max=30), DataRequired()])
    lastname = StringField(label='lasstname', validators=[Length(min=2, max=30), DataRequired()])
    
    email = StringField(label='email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='repeat password', validators=[EqualTo("password1"), DataRequired()])
    age = IntegerField(label='age', validators=[DataRequired()])
    
    submit = SubmitField(label='Sign up')



class LoginForm(FlaskForm):

    email = StringField(label='email', validators=[Email(), DataRequired()])
    password = PasswordField(label='password', validators=[Length(min=6), DataRequired()])

    
    submit = SubmitField(label='Sign in')






class CreateCommentForm(FlaskForm):
    
    current = StringField(label='current')
    parrent = StringField(label='parrent')
    text = TextAreaField(label='text', validators=[DataRequired()])
    submit = SubmitField(label='Comment')


class EditSubredditForm(FlaskForm):
    
    id = StringField(label='id')
    display_name = StringField(label='Display name')
    subreddit_logo = FileField('Subreddit logo')
    subreddit_img = FileField('Subreddit img')
    description = TextAreaField(label='Description', validators=[DataRequired()])
    public_description = TextAreaField(label='Public description', validators=[DataRequired()])
    
    submit = SubmitField(label='Edit')


class SubredditForm(FlaskForm):
    

    display_name = StringField(label='Display name', validators=[DataRequired()])
    subreddit_logo = FileField('Subreddit logo', validators=[DataRequired()])
    subreddit_img = FileField('Subreddit img')
    description = TextAreaField(label='Description', validators=[DataRequired()])
    public_description = TextAreaField(label='Public description', validators=[DataRequired()])
    
    submit = SubmitField(label='Submit')



class DelateSubredditForm(FlaskForm):
    
    id = StringField(label='id')

    submit = SubmitField(label='Delete')




class SubmissionForm(FlaskForm):
    
    subreddit = StringField(label='subreddit', validators=[DataRequired(), Length(min=1)])

    title = StringField(label= 'title',  validators=[DataRequired()])
    selftext = TextAreaField(label='Description')
    url = StringField(label='img url')#FileField('url')

    submit = SubmitField(label='submit')


class EditSubmissionForm(FlaskForm):

    id = StringField(label='id')
    #subreddit = StringField(label='subreddit', validators=[DataRequired(), Length(min=1)])

    title = StringField(label= 'title',  validators=[DataRequired()])
    selftext = TextAreaField(label='Description')
    url = StringField(label='img url')#FileField('url')

    submit = SubmitField(label='Edit')


class DelateSubmissionForm(FlaskForm):
    
    id = StringField(label='id')

    submit = SubmitField(label='Delete')



class UserForm(FlaskForm):

    user_img = FileField('Profile img')

    username = StringField(label='username', validators=[Length(min=2, max=30), DataRequired()])
    firstname = StringField(label='firstname', validators=[Length(min=2, max=30), DataRequired()])
    lastname = StringField(label='lasstname', validators=[Length(min=2, max=30), DataRequired()])
    
    email = StringField(label='email', validators=[Email(), DataRequired()])
    #password1 = PasswordField(label='password', validators=[Length(min=6), DataRequired()])
    #password2 = PasswordField(label='repeat password', validators=[EqualTo("password1"), DataRequired()])
    age = IntegerField(label='age', validators=[DataRequired()])
    
    submit = SubmitField(label='Edit')