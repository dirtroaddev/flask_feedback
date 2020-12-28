from flask import Flask, redirect, render_template, session, flash
from models import connect_db, db, User, Feedback
from sqlalchemy.exc import IntegrityError
from form import UserForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///feedback_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "thisisthepasskey"

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/users/<string:username>')
def get_secret(username):
    user = User.query.get_or_404(username)
    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect('/login')
    if user.username == session['username']:
        return render_template('user.html', user=user)
    
    return redirect(f'/users/{session["username"]}')

@app.route('/users/<string:username>/delete', methods=['POST'])
def del_user(username):
    
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()

        except IntegrityError:
            form.username.errors.append('Username taken, Please pick another!!!!')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully create account!!')
        return redirect(f'/users/{username}')
    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome back, {user.username}!", 'primary')
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid username/passwords']
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username')
    flash('Goodbye!!!!', 'success')
    return redirect('/login')

@app.route('/users/<string:username>/feedback/add', methods=['GET', 'POST'])
def add_feed(username):
    form = FeedbackForm()
    if 'username' not in session:
        flash('Please login to access this page', 'danger')
        return redirect('/login')
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title,content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('feed_form.html', form=form)
    
@app.route('/users/<int:id>/feedback/edit', methods=['GET', 'POST'])
def edit_feed(id):
    
    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect('/login')
    feed = Feedback.query.get_or_404(id)
    form = FeedbackForm(obj=feed)
    if feed.username == session['username']:
        
        if form.validate_on_submit():
            feed.title = form.title.data
            feed.content = form.content.data
            db.session.commit()
            return redirect(f'/users/{feed.username}')
        else:
            return render_template('edit_feed.html', form=form)
    
    flash("Sorry you do not have permissions", 'danger')
    return redirect(f'/users/{session["username"]}')


@app.route('/users/<int:id>/feedback/delete')
def del_feed(id):
    if 'username' not in session:
        flash('You can not delete that!!!!', 'danger')
        return redirect('/login')
    else:
        feed = Feedback.query.get_or_404(id)
        db.session.delete(feed)
        db.session.commit()
        return redirect(f'/users/{session["username"]}')
