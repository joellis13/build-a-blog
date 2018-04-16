from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:asdf@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'U6JtITN8Qc'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120)) 
    body = db.Column(db.String(1000))
    blog_date = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        blog_date = datetime.utcnow()
        self.blog_date = blog_date

@app.route('/blog')
def blog():
    if (request.args.get('id')):
        id = request.args.get('id')
        blog = Blog.query.filter_by(id=id).first()
        title = blog.title
        body = blog.body
        return render_template('viewpost.html', title=title, body=body)
    else:
        blogs = Blog.query.order_by(Blog.blog_date.desc()).all()
        return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body_name = request.form['body']

        title_error = ''
        body_error = ''

        if title == '':
            title_error = 'Please fill in the title'

        if body_name == '':
            body_error = 'Please fill in the body'

        if title_error == '' and body_error == '':
            new_blog = Blog(title, body_name)
            db.session.add(new_blog)
            db.session.commit()
            id = str(new_blog.id)
            return redirect('/blog?id=' + id)

        else:
            return render_template('newpost.html', title_error=title_error, body_error=body_error)

    else:
        return render_template('newpost.html')


if __name__ == '__main__':
    app.run()