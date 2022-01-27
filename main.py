
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_mail import Mail

# local_server = True
with open('config.json','r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)

mail = Mail(app)

if(params["local_server"]):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]
    
db = SQLAlchemy(app)

class Contact (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(15), unique=True, nullable=False)
    msg = db.Column(db.String(200), unique=True, nullable=False)
    date = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Posts (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    tagline = db.Column(db.String(80), nullable=True)
    slug = db.Column(db.String(21), unique=True, nullable=False)
    content = db.Column(db.String(200), unique=True, nullable=False)
    date = db.Column(db.String(20), unique=False, nullable=True)
    img_file = db.Column(db.String(20), unique=False, nullable=True)


@app.route("/")
def home():
    print("Entered home")
    post = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template("index.html",params =params,posts = post)

@app.route("/about")
def about():
    name = "happpy"
    return render_template("about.html",params =params)

@app.route("/dashboard",methods = ['GET','POST'])
def dashboard():
    cred = ""
    if request.method == 'POST':
        # redirect to admin panel
        pass
    else: 
        return render_template("login.html",params =params, cred = "Wrong Credentials !!!!")    
    

@app.route("/post/<string:post_slug>",methods = ['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug = post_slug).first()
    return render_template("post.html",post = post,params = params)

@app.route("/contact", methods= ['GET','POST'])
def contact():
    print("Contact API is called")
    if(request.method == 'POST'):
        # add entry to the database
        name  = request.form.get('name')
        email  = request.form.get('email')
        phone  = request.form.get('phone')
        message  = request.form.get('message')

        entry = Contact(name = name, phone_num = phone,msg = message,email = email,date = datetime.now())
        print(entry)
        db.session.add(entry)
        db.session.commit()
        mail.send_message("New message from " + name, 
                sender = email, 
                recipients = [params['gmail-user']],
                body = message + '\n' + phone
                 )

    print("going to contact page")
    return render_template("contact.html",params =params)

# @app.route("/<string:wrong_page>",methods = ['GET'])
# def wrong_page(wrong_page):
#     return render_template("index.html",params =params)


app.run(debug = True)