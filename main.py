from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Set up db for blog with auto-inc in, title, and body
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body
# display index page with all posts in db
@app.route("/")
def index():
    posts = Blog.query.all()
    return render_template("index.html", posts = posts)
# display newpost page
@app.route("/newpost", methods = ["GET", "POST"])
def newpost():
    if request.method == "GET":
        return render_template("newpost.html")
# test for blank title or body
    elif request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        blank = False
        if title == "":
            titleerror = "ERROR:Please_include_a_title"
            blank = True
        else:
            titleerror = ""

        if body == "":
            bodyerror = "ERROR:Please include text in your post"
            blank = True
        else:
            bodyerror = ""
# if one or both are blank return newpost page with error message(s)
        if blank:
            return render_template("newpost.html", title = title, titleerror = titleerror, body = body, bodyerror = bodyerror)
# otherwise, get title and body and inset into db then show the post
        else:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            id = new_blog.id
            return redirect("/posted?id={}".format(id))
# display post just added or post selected from index page
@app.route("/posted")
def posted():
    id = request.args.get("id")
    post = Blog.query.filter_by(id = id).first()
    return render_template("posted.html", id = id, post = post)
# delete select post from db
@app.route("/deleted", methods = ["POST"])
def deleted():
    id = int(request.form["postid"])
    delpost = Blog.query.filter_by(id = id).first()
    db.session.delete(delpost)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run()
