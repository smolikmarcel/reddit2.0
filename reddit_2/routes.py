from reddit_2 import db, app, images
from flask import render_template, request, redirect, url_for, flash, jsonify,  get_flashed_messages
from reddit_2.models import User, Subreddit, Submission, Comment
from reddit_2.forms import RegisterForm, LoginForm, CreateCommentForm, SubredditForm, EditSubredditForm, DelateSubredditForm, SubmissionForm, EditSubmissionForm, DelateSubmissionForm, UserForm
from flask_login import current_user, login_user, logout_user, login_required

import os



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('home.html'), 404


#helpful functions
def comment_data(comment, level, data):
    
    for reply in comment.replies:
        liked = 0
        if current_user.is_authenticated and reply in current_user.liked_comments_like: liked = 1
        if current_user.is_authenticated and reply in current_user.liked_comments_dislike: liked = -1

        data.append((level, reply, liked))
        comment_data(reply, level + 1, data)




#regular pages
@app.route('/')
def home_page():

    page = request.args.get('page', 1, type=int)
    subreddits = Subreddit.query.all()
    submissions = Submission.query.paginate(page=page, per_page=18)  #.all()[:24]
    return render_template('home.html', subreddits=subreddits, submissions=submissions)

@app.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    
    if request.method == 'POST':
        
        search_word = request.form['query']
        
        if search_word == '':  submissions = [] #Submission.query.all()[:5]
        else: submissions = Submission.query.filter(Submission.title.contains(search_word))[:5]
            
        return jsonify({'htmlresponse': render_template('response.html', submissions=submissions)})


@app.route("/ajaxsubscriber",methods=["POST","GET"])
def ajaxsubscribers():
    
    if request.method == 'POST':
        
        pom = int(request.form['query'])
        subreddit = Subreddit.query.filter_by(id=request.form['reddit']).first()
        if pom == 1: current_user.joined_subreddits.append(subreddit)
        else: current_user.joined_subreddits.remove(subreddit)
        subreddit.subscribers += pom
        
        db.session.commit()
        return jsonify({'htmlresponse': ""})


@app.route("/ajaxsubmission",methods=["POST","GET"])
def ajaxsubmission():
    
    if request.method == 'POST':
        
        pom = int(request.form['query'])
        submission = Submission.query.filter_by(id=request.form['submission']).first()

        if pom == 1: current_user.liked_submissions_like.append(submission)
        if pom == -3: 
            current_user.liked_submissions_like.remove(submission)
            pom = -1
        elif pom == -1: current_user.liked_submissions_dislike.append(submission)
        elif pom == 3: 
            current_user.liked_submissions_dislike.remove(submission)
            pom = 1
        elif pom == 2: 
            current_user.liked_submissions_like.append(submission)
            current_user.liked_submissions_dislike.remove(submission)
        elif pom == -2: 
            current_user.liked_submissions_like.remove(submission)
            current_user.liked_submissions_dislike.append(submission)
            
        submission.score += pom
        db.session.commit()

        print(current_user.liked_submissions_like)
        print(current_user.liked_submissions_dislike)
        return jsonify({'htmlresponse': ""})


@app.route("/ajaxcomment",methods=["POST","GET"])
def ajaxcomment():
    
    if request.method == 'POST':
        
        pom = int(request.form['query'])
        comment = Comment.query.filter_by(id=request.form['comment']).first()

        if pom == 1: current_user.liked_comments_like.append(comment)
        if pom == -3: 
            current_user.liked_comments_like.remove(comment)
            pom = -1
        elif pom == -1: current_user.liked_comments_dislike.append(comment)
        elif pom == 3: 
            current_user.liked_comments_dislike.remove(comment)
            pom = 1
        elif pom == 2: 
            current_user.liked_comments_like.append(comment)
            current_user.liked_comments_dislike.remove(comment)
        elif pom == -2: 
            current_user.liked_comments_like.remove(comment)
            current_user.liked_comments_dislike.append(comment)
            
        comment.score += pom
        db.session.commit()

        print(current_user.liked_comments_like)
        print(current_user.liked_comments_dislike)
        return jsonify({'htmlresponse': ""})




@app.route('/r/<subreddit>')
def subreddit_page(subreddit):

    subreddits = Subreddit.query.all()
    current_subreddit = Subreddit.query.filter_by(display_name=subreddit).first()
    
    
    page = request.args.get('page', 1, type=int)
    submissions = Submission.query.filter_by(subreddit=current_subreddit.id).paginate(page=page, per_page=18)  #.all()[:24]

    #submissions = current_subreddit.submissions.paginate(page=page, per_page=18)
    joined = False
    if current_user.is_authenticated and current_subreddit in current_user.joined_subreddits: joined = True
    

    return render_template('home2.html', subreddits=subreddits, submissions=submissions, current_subreddit=current_subreddit, joined=joined)

@app.route('/r/<subreddit>/learn_more')
def subreddit_learn_more_page(subreddit):

    subreddits = Subreddit.query.all()
    current_subreddit = Subreddit.query.filter_by(display_name=subreddit).first()

    joined = False
    if current_user.is_authenticated and current_subreddit in current_user.joined_subreddits: joined = True
    
    return render_template('learn_more.html', subreddits=subreddits, current_subreddit=current_subreddit, joined=joined)

@app.route('/s/<submission>', methods=['GET', 'POST'])
def submission_page(submission):

    subreddits = Subreddit.query.all()
    submission2 = Submission.query.filter_by(id=submission)[0]
    current_subreddit = Subreddit.query.filter_by(id=submission2.subreddit).first()
    try:
        submission2.selftext = submission2.selftext.replace('\\n', '</br>')
    except AttributeError:
        submission2.selftext = ""

    comments_data = []
    comments   = Comment.query.filter_by(id=submission)[0]
    comment_data(comments, 0, comments_data)


    form = CreateCommentForm()
    if form.validate_on_submit():
        comm = Comment(
                   id = os.urandom(6).hex(),
                   text = form.text.data,
                   score = 0,
                   
                   author = form.current.data,
                   submission = submission2.id,
                   parent_id = form.parrent.data)
        
        db.session.add(comm)
        db.session.commit()

        flash("Comment was successfuly created.")
        return redirect(url_for('submission_page', submission=submission2.id))
    
    liked = 0
    if current_user.is_authenticated and submission2 in current_user.liked_submissions_like: liked = 1
    if current_user.is_authenticated and submission2 in current_user.liked_submissions_dislike: liked = -1

    return render_template('submission.html', subreddits=subreddits, submission=submission2, current_subreddit=current_subreddit, comments_data=comments_data, form=form, liked=liked)




#login registration
@app.route('/logout')
def logout_page():

    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():

    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash("succesfuly loged")
            return redirect(url_for('home_page'))
        else:
            flash('Userame and password are ot match. Pleas try again.', category='danger')

    return render_template('sign_in.html', form=form)

@app.route('/registrate', methods=['GET', 'POST'])
def register_page():

    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(img='', 
                            username=form.username.data, 
                            firstname=form.firstname.data, 
                            lastname=form.lastname.data, 
                            email=form.email.data, 
                            password_hash=form.password1.data, 
                            age=form.age.data)
        
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash("succesfuly registrate", category="success")
        return redirect(url_for('profile_home'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'error {err_msg}')
    return render_template('sign_up.html', form=form)




#profile
@app.route('/p/profile', methods=['GET', 'POST'])
@login_required
def profile_home():

    form = UserForm()

    if request.method == 'POST':

        if request.form["submit"] == "Edit" and form.validate_on_submit():
            
            try: user_img = images.save(form.user_img.data)
            except: user_img = ""

            if user_img != "": current_user.img = user_img
            current_user.username = form.username.data
            current_user.firstname = form.firstname.data
            current_user.lastname = form.lastname.data
            current_user.email = form.email.data
            current_user.age = form.age.data

            db.session.commit()
            
                    
            flash("Profile was succesfuly edited.", category="success")

            return redirect(url_for('profile_home'))

    return render_template('profile_home.html', form=form)



#profile
@app.route('/p/subreddits', methods=['GET', 'POST'])
@login_required
def profile_subreddits():

    form = EditSubredditForm()
    delete = DelateSubredditForm()


    if request.method == 'POST':

        if request.form["submit"] == "Edit" and form.validate_on_submit():
            try: subreddit_logo = images.save(form.subreddit_logo.data)
            except: subreddit_logo = ""

            try: subreddit_img = images.save(form.subreddit_img.data)
            except: subreddit_img = ""
            
            for subreddit in current_user.subreddits:
                if subreddit.id == form.id.data:
                    subreddit.display_name = form.display_name.data
                    if subreddit_logo != "": subreddit.subreddit_logo = subreddit_logo
                    if subreddit_img != "": subreddit.subreddit_img = subreddit_img
                    subreddit.description = form.description.data
                    subreddit.public_description = form.public_description.data
                    db.session.commit()
            

                    flash("Subreddit was succesfuly edited.", category="success")

                    return redirect(url_for('profile_subreddits'))

        if request.form["submit"] == "Delete" and delete.validate_on_submit():
            for subreddit in current_user.subreddits:
                if subreddit.id == form.id.data:
                    db.session.delete(subreddit)
                    db.session.commit()
            
            flash("Subreddit was succesfuly deleted.", category="success")

            return redirect(url_for('profile_subreddits'))

    return render_template('profile_subreddits.html', form=form, delete=delete)


@app.route('/p/new_subreddit', methods=['GET', 'POST'])
@login_required
def profile_new_subreddit():

    form = SubredditForm()

    if form.validate_on_submit():

        subreddit_logo = images.save(form.subreddit_logo.data)
        try: subreddit_img = images.save(form.subreddit_img.data)
        except: subreddit_img = ""

        reddit_to_create = Subreddit(id = os.urandom(6).hex(),
                            display_name=form.display_name.data,
                            description=form.description.data, 
                            public_description=form.public_description.data, 
                            subreddit_logo=subreddit_logo, 
                            subreddit_img=subreddit_img, 
                            author=current_user.id)
        
        db.session.add(reddit_to_create)
        db.session.commit()

        flash("Subreddit was succesfuly created.", category="success")

        return redirect(url_for('profile_subreddits'))

    return render_template('profile_new_subreddit.html', form=form)





@app.route('/p/submissions', methods=['GET', 'POST'])
@login_required
def profile_submissions():

    form = EditSubmissionForm()
    delete = DelateSubmissionForm()

    if request.method == 'POST':

        if request.form["submit"] == "Edit" and form.validate_on_submit():
            
            for submission in current_user.submissions:
                if submission.id == form.id.data:
                    
                    print(form.title.data)
                    print(form.selftext.data)
                    print(form.url.data)

                    submission.title=form.title.data
                    submission.selftext=form.selftext.data
                    submission.url=form.url.data
                    db.session.commit()
                    
                    flash("Submission was succesfuly edited.", category="success")

                    return redirect(url_for('profile_submissions'))


        if request.form["submit"] == "Delete" and delete.validate_on_submit():
            for submission in current_user.submissions:
                if submission.id == form.id.data:

                    comments = Comment.query.filter_by(submission=submission.id)

                    for comment in comments:
                        db.session.delete(comment)

                    db.session.delete(submission)
                    db.session.commit()
                    comments = Comment.query.filter_by(submission=submission.id)
                    
                    flash("Submission was succesfuly deleted.", category="success")

                    return redirect(url_for('profile_submissions'))

    return render_template('profile_submissions.html', form=form, delete=delete)





@app.route('/p/new_submission', methods=['GET', 'POST'])
@login_required
def profile_new_submission():

    form = SubmissionForm()
    subreddits = Subreddit.query.all()

    if form.validate_on_submit():

        gen_id = os.urandom(6).hex()

        #try: url = images.save(form.url.data)
        #except: url = ""

        
        submission_to_create = Submission(id = gen_id,
                            title=form.title.data,
                            selftext=form.selftext.data, 
                            url=form.url.data, 
                            thread_id=gen_id,
                            author=current_user.id, 
                            subreddit=form.subreddit.data)

        
        
        comm = Comment(id = gen_id,
                   author = current_user.id,
                   submission = gen_id)
        

        #db.session.rollback()
        db.session.add(comm)
        db.session.add(submission_to_create)
        db.session.commit()


        flash("Submission was succesfuly created.", category="success")

        return redirect(url_for('profile_submissions'))

    return render_template('profile_new_submission.html', form=form, subreddits=subreddits)