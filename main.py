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
    title = db.Column(db.String(120)) # creates a column that is a string only consisting of 120 characters
    body = db.Column(db.Text) # creates a text column 

    def __init__(self, title, body):
        self.title = title
        self.body = body

# Displays the blog page
@app.route('/blog', methods=['POST', 'GET'])
def post():
    
        blog_posts = Blog.query.all() # Query the database and assign to a variable object
        different_id = request.args.get('id') # a get request based of the id tag in the blog.html

        if different_id: # If there is a get request do this
            blog_posts = Blog.query.filter_by(id=different_id).first() # Query database and filter the query based off the id from the get request
            return render_template('individual_post.html', blog_posts=blog_posts) # render the new blog post based off the id from the database

        return render_template('blog.html', blog_posts=blog_posts) # renders the blog if not a get request

# Adds blog post into a data base
@app.route('/newpost', methods=['POST','GET'])
def newpost():
    
    if request.method == 'POST': # If you submit data go through steps below
        title = request.form['title'] # grab information from the form
        body = request.form['body']
        
        if title and body: # If title and body is true do what is below (This returns a falsely if length is 0)
            newpost = Blog(title, body)
            db.session.add(newpost) # Stage the data for the database
            db.session.commit() # Commmit addtion to the database
            return redirect('/blog?id=' + str(newpost.id)) # This should render tempate 

        else:
            flash('Body and Title can not be empty', 'error') # flash message if title or body is empty
            return render_template("newpost.html", title=title, body=body)
        
    else:
        return render_template("newpost.html")

if __name__ == '__main__':
    app.run()