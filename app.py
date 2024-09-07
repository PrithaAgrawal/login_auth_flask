from flask import Flask,render_template,url_for, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, login_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired,  Length, ValidationError, Email 
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pritha:newpassword@localhost/master'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False) 

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length( min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length( min=4, max=20)], render_kw={"placeholder": "Password"})
    email = StringField(validators=[InputRequired(), Length( min=4, max=20)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length( min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length( min=4, max=20)], render_kw={"placeholder": "Password"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"Placeholder": "Email"})
    submit = SubmitField("Login")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print("User found")
        else:
            print("User not found")
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            print("Invalid credentials")
    return render_template('login.html', form=form)


@app.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    print(f"Current user: {current_user.username}")
    return render_template('dashboard.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print(f"New user {form.username.data} added to the database.")
        return redirect(url_for("login"))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    # Manually push the app context
    ctx = app.app_context()
    ctx.push()

    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        ctx.pop()

    app.run(debug=True)
