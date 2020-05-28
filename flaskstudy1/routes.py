import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect,send_from_directory,request, abort
from flaskstudy1 import app,db,bcrypt
from flaskstudy1.forms import RegForm, LoginForm, UpdateForm, PostForm
from flaskstudy1.models import User, Post
from flask_login import login_user, current_user, logout_user,login_required

HTs = [
    {
        'Name' : 'David Tran',
        'Age' : '25',
        'Role':'Doan Truong',
    },
{
        'Name' : 'Tuyet Hoang',
        'Age' : '24',
        'Role':'Doan Pho Nghiem Huan',
    },
    {
        'Name' : 'Cecilia Tran',
        'Age' : '24',
        'Role':'Doan Pho Quan Tri',
    }
]
@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts = posts)

@app.route('/info')
def info():
    return render_template('info.html', HTs = HTs)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return register(url_for('home'))
    form = RegForm()
    if form.validate_on_submit():
        testpw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email= form.email.data, password=testpw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Welcome to TMT!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form = form)

@app.route('/login',methods=['GET','POST'])
def login():
        form=LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            passworrd_ = '''
            Accessing Database to check for input user email
            This part needs to be careful since this is where 
            you are getting the database and access the email and passworrd
            '''

            if user and bcrypt.check_password_hash(user.password,form.password.data):
                # If user name entered exist in database, if it does the background will pull up the password to
                # check with the entered password from user (Behind background of Flask)
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('info'))
                '''If a user try to go to account page without login in before they will be redirect to login
                after they login they will be direct to there account page, or in specific - the page they 
                couldn't access to because they weren't login; if a user didn't try to go to the account page
                but they go to login first then the next page they will be direct to is the info page'''
            else:
                flash('Login Unsuccessful. Check your sign in info','danger')
        return render_template('login.html', title='Login', form= form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture): # this is just a resize and resave for image processing function not a route definition
    randomHex = secrets.token_hex(8)
    _, fileExt = os.path.splitext(form_picture.filename)
    pictureFN = randomHex+ fileExt
    picPath = os.path.join(app.root_path,'static/profileImg',pictureFN)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picPath)
    return pictureFN

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picFile = save_picture(form.picture.data)
            current_user.avatar = picFile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    imageFile = url_for('static',filename = 'profileImg/' + current_user.avatar )
    return render_template('account.html', title ="Account",
                            imageFile = imageFile, form = form)

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title= form.title.data, content= form.content.data, HTs = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post has been created!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title = "New Post",
                           form = form, legend = 'New Post')


@app.route("/post/<int:post_id>/<post_date>/<post_title>")
def post(post_id,post_date, post_title):
    '''Route is created base on the order of Models' item
    so if your models is in this order ID/Post/Tile/UserID
    then route must process through each variable /column/ '''
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post = post)

@app.route("/post/<int:post_id>/<post_date>/<post_title>/update", methods=['GET','POST'])
@login_required
def update_post(post_id,post_date, post_title):
    post = Post.query.get_or_404(post_id)
    if post.HTs != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post',post_id = post.id, post_date = post.postDate, post_title = post.title))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title="Update Post",
                           form=form, legend = 'Update Post')

@app.route("/post/<int:post_id>/<post_date>/<post_title>/delete", methods=['POST'])
@login_required
def delete_post(post_id,post_date, post_title):
    post = Post.query.get_or_404(post_id)
    if post.HTs != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))