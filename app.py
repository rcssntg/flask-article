from flask import Flask, render_template, url_for, request, flash, redirect, session, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)


# Config MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['USER'] = 'root'
app.config['PASSWORD'] = '338356'
app.config['DB'] = 'myflaskapp'
app.config['CURSORCLASS'] = 'DictCursor'
# init MySQL
mysql = MySQL(app)

Articles = Articles()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25) ])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data 
        email = form.email.data
        username = form.username.data 
        password = sha256_crypt.hash(str(form.password.data))     
    return render_template('register.html', form=form)
        
        # Cretae cursor
    cur = mysql.connection.cursor()
        
        # Execute query
    cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password)
)  
    
        # Commit to DB
    Mysql.connection.commit()
        
        # Close connection
    cur.close()
        
    flash('You are now registered and can login', 'success')
        
    redirect(url_for('home'))
        
    return render_template('register.html', form=form)


# User login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        
        # Create Cursor
        cur = mysql.connection.cursor()
        
        # get user by username
        result = cur.execute("SELECT * FORM users WHERE username = %s", [username])
        
        if result > 0:
            # get stored hash
            data = cur.fetchone()
            password = data['password']
            
            # compare the passwords
            if sha256_crypt.verified(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
            else:
                app.logger.info('PASSWORD NOT MATCHED')
        else:
            app.logger.info('NO USER')
        
    return render_template('login.html')
        
        

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)