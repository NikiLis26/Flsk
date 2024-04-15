from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    owner = db.Column(db.String(100), nullable=False)


@app.route('/create', methods=['GET'])
def create_form():

    return render_template('create_form.html')


@app.route('/create', methods=['POST'])
def create_ad():

    return redirect(url_for('index'))


@app.route('/delete/<int:ad_id>', methods=['POST'])
def delete_ad(ad_id):

    return redirect(url_for('index'))

@app.route('/edit/<int:ad_id>', methods=['GET'])
def edit_form(ad_id):
    ad = Announcement.query.get_or_404(ad_id)
    return render_template('edit_form.html', ad=ad)  # Передача данных объявления в шаблон


@app.route('/edit/<int:ad_id>', methods=['POST'])
def edit_ad(ad_id):

    return redirect(url_for('index'))  # Перенаправление на главную страницу после редактирования

if __name__ == '__main__':
    app.run(debug=True)