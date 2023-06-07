from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost/blogy"
app.config['SECRET_KEY'] = "helloworld"
db = SQLAlchemy(app)
admin = Admin(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime)
    slug = db.Column(db.String(255))

admin.add_view(ModelView(Posts, db.session))

@app.route("/")
def homepage():
    posts = Posts.query.all()
    return render_template("index.html", posts=posts)

@app.route("/post/<string:slug>")
def post(slug):
    post = Posts.query.filter_by(slug=slug).one()
    return render_template("post.html", post=post)

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)