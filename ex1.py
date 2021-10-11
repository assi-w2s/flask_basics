from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


app.config.update(
    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:1mevushaliM!@localhost/catalog_db',
    # SQLALCHEMY_DATABASE_URI='<database>://<user_id>:<password>&<server>/<database_name>',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)


@app.route('/index')
@app.route('/')
def hello_flask():
    return "hello there!"


@app.route('/new/')
def query_strings(greeting = 'hello'):
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is : {0} </h1>'.format(query_val)


@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='nine'):
    return '<h1> hello there {} !</h1>'.format(name)


@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1> heres a string: {} !</h1>'.format(name)


@app.route('/numbers/<float:num>')
def working_with_numbers(num):
    return '<h1> heres a number: {} !</h1>'.format(num)


@app.route('/numbers/product/<float:num1>/<float:num2>')
def multiplication(num1, num2):
    return '<h1> heres multiplication: {} !</h1>'.format(num1 * num2)


@app.route('/temp')
def using_templates():
    return render_template('index.html')


@app.route('/watch')
def top_movies():
    movie_list = [
        'autopsy of jane doe',
        'moon demon',
        'ghost in a shell',
        'kong: skull island',
        'john wick 2',
        'spiderman - homecoming'
    ]
    return render_template('movies.html',
                           movies=movie_list,
                           name='Harry')


@app.route('/tables')
def movies_plus():
    movies_dict = {
        'autopsy of jane doe': 2.1,
        'moon demon': 3.2,
        'ghost in a shell': 2.6,
        'kong: skull island': 9.3,
        'john wick 2': 3.0,
        'spiderman - homecoming': 1.1
    }
    return render_template('table_data2.html',
                           movies=movies_dict,
                           name='Sally')


@app.route('/filters')
def filter_data():
    movies_dict = {
        'autopsy of jane doe': 2.14,
        'moon demon': 3.20,
        'ghost in a shell': 2.62,
        'kong: skull island': 9.31,
        'john wick 2': 3.03,
        'spiderman - homecoming': 1.1
    }
    return render_template('filter_data.html',
                           movies=movies_dict,
                           name=None,
                           film='a christmas carol')


@app.route('/macros')
def jinja_macros():
    movies_dict = {
        'autopsy of jane doe': 2.14,
        'moon demon': 3.20,
        'ghost in a shell': 2.62,
        'kong: skull island': 9.31,
        'john wick 2': 3.03,
        'spiderman - homecoming': 1.1
    }
    return render_template('using_macros.html',
                           movies=movies_dict)


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Publisher is {}'.format(self.name)


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, index=True)
    authors = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    format = db.Column(db.String(40), nullable=True)
    image_url = db.Column(db.String(100), nullable=True)
    num_pages = db.Column(db.Integer, nullable=True)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=True)
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, authors, rating, format, image_url, num_pages, pub_id):
        self.title = title
        self.authors = authors
        self.rating = rating
        self.format = format
        self.image_url = image_url
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.authors)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)