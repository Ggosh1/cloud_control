from flask import Flask, render_template, request, redirect, json
from flask_sqlalchemy import SQLAlchemy
import validators
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)


class Lnk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(500), nullable=False)
    shortened = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'Link id: {self.id}'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_len', methods=['POST'])
def get_len():
    origin = request.form['original']
    link_shortened, code = link_processing(origin)
    if code:
        link = Lnk(original=origin, shortened=link_shortened)
        try:
            db.session.add(link)
            db.session.commit()
        except Exception as exc:
            print(exc)
    dict1 = {'res': 'Результат: ' + link_shortened}
    return json.dumps(dict1)


@app.route('/<short_link>')
def short_link_redirect(short_link):
    try:
        db_link_id = Lnk.query.filter(Lnk.shortened == 'http://127.0.0.1:5000/' + short_link).first()
        print(db_link_id, short_link)
        if db_link_id:
            return redirect(db_link_id.original)
        else:
            return render_template('index.html')
    except:
        return render_template('index.html')


def link_processing(link):
    db_link_id = Lnk.query.filter(Lnk.original == link).first()
    if db_link_id:
        return db_link_id.shortened, False
    elif not validators.url(link):
        return 'Некорректная ссылка', False
    else:
        while True:
            try:
                short_link = 'http://127.0.0.1:5000/' + "".join(
                    random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in
                    range(8))
                return short_link, True
            except:
                pass


if __name__ == '__main__':
    app.run(debug=True)
