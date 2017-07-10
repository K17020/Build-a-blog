from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'rF1iDxY6qlTmvyJl'

# Creates a database called blog
class Blog(db.Model):
    # Creates the table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

# Displays the blog page
@app.route('/blog', methods=['POST', 'GET'])
def post():
    blog_posts = Blog.query.all()
    return render_template('blog.html', blog_posts=blog_posts)



# Adds blog post into a data base
@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title and body:
            newpost = Blog(title, body)
            db.session.add(newpost)
            db.session.commit()
        else:
            flash("Title and body can not be empty.")
            return render_template("newpost.html", title=title, body=body)
        return redirect('/')
    else:
        return render_template("newpost.html")
if __name__ == '__main__':
    app.run()