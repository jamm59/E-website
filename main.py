from flask import Flask,redirect,url_for,request,render_template,flash,abort
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from flask_bootstrap import Bootstrap
from functools import wraps
from flask_ckeditor import CKEditor, CKEditorField
from forms import PostForm,LoginForm,RegisterForm,AddForm
from flask_login import login_required,login_user,logout_user,login_manager,current_user,LoginManager,UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random


app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = 'namekey'
Bootstrap(app)
#............decorator....................
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.id != 1:
            return abort(400)
        return func(*args, **kwargs)      
    return wrapper
#................................flask database..............................................................
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///blog.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    name = db.Column(db.String(100),nullable=False)
    cards = relationship("Cards",back_populates='admin')

class Cards(db.Model):
    __tablename__ = "cards"
    card_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.String(10),nullable=False)
    name = db.Column(db.String(10),nullable=False)
    description = db.Column(db.String(100),nullable=False)
    rating = db.Column(db.Integer,nullable=False)
    img_url = db.Column(db.String(1000),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)

    admin = relationship('User',back_populates='cards')
    
db.create_all()
#............................... flask login..................................................................
login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# ...........................................................................................................
@app.route('/')
def home():
    all_cards = Cards.query.all()
    if current_user.is_authenticated:
        return render_template('index.html',current_user=current_user, all_cards=all_cards,random_num=random.randint(1,10))
    flash('You need to create an account or login first')
    return redirect(url_for('login'))

@app.route('/contact')
@login_required
def contact():
    form = PostForm()
    return render_template('contact.html',form=form)

@app.route('/register',methods=['GET', 'POST'])
def register():
    form= RegisterForm()
    if form.validate_on_submit():

        user_exist = User.query.filter_by(email=request.form.get('email')).first()
        if user_exist:
            flash('An account is already registered with this email.')
            return redirect(url_for('register'))

        encypted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
            )
        new_user = User(
            name=request.form.get('name'),
            email=request.form.get('email'),
            password=encypted_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html',form=form,current_user=current_user)

@app.route('/login',methods=['GET', 'POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form.get('email')).first()

        if not user:
            flash("You haven't registered with this email")
            return redirect(url_for('register'))

        else:
            password = form.password.data
            password_is_correct = check_password_hash(user.password,password)

            if password_is_correct:
                flash('Successful login')
                login_user(user)
                return redirect(url_for('home'))

            elif not password_is_correct:
                flash('Invalid password try again')
                return redirect(url_for('login'))

    return render_template('login.html',form=form)

@app.route('/add_card',methods=['GET','POST'])
@admin_only
def add_card():
    form = AddForm()

    if form.validate_on_submit():
        body = form.body.data
        body = body.split('<p>')[1].split('</p>')[0]
        new_card = Cards(
            price=form.price.data,
            name=form.name.data,
            user_id=current_user.id,
            description=body,
            rating=form.rating.data,
            img_url=form.image.data
            )
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_cards.html',form=form)

@app.route('/logout')    
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/delete',methods=['GET','POST'])
def delete():
    card_id = request.args.get('id')
    card = Cards.query.get(card_id)
    print(card)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)



