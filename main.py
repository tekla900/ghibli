

from flask import Flask, redirect, url_for, render_template, \
request, session, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ghibli.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(60))
    description = db.Column(db.VARCHAR(500))
    director = db.Column(db.VARCHAR(30))
    release_date = db.Column(db.VARCHAR(10))
    run_time = db.Column(db.Integer)



    def __str__(self):
        return f'Anime title:{self.title}; Director: {self.director}; Release Date: {self.release_date}; Run Time {self.run_time};\n Description: {self.description}'



conn = sqlite3.connect("ghibli.sqlite")
cursor = conn.cursor()
cursor.execute('SELECT * FROM ghibli')
records = cursor.fetchmany(50)
for each in records:
    title = each[1]
    description = each[2]
    director = each[3]
    release_date = each[4]
    run_time = each[5]
    info = (title, description, director, release_date, run_time)



@app.route('/list')
def list():
    return render_template('list.html', records=records, title=title, description=description, director=director, release_date=release_date, run_time=run_time, each=each)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/animes', methods=['GET', 'POST'])
def animes():
    if request.method=='POST':
        t = request.form['title']
        d = request.form['director']
        rel = request.form['release date']
        run = request.form['run time']
        desc = request.form['description']

        if t=='' or d=='':
            flash('შეავსეთ სათაურის და რეჟისორის ველი', 'error')

        elif not run.isnumeric():
            flash('ხანგძლივობა უნდა იყოს რიცხვი!', 'error')

        else:
            a1 = Anime(title=t, description=desc, director=d, release_date=rel, run_time=run )
            db.session.add(a1)
            db.session.commit()
            flash('ანიმე წარმატებით დაემატა მონაცემთა ბაზას', 'info')

    return render_template('animes.html')

if __name__ == "__main__":
    app.run(debug=True)
