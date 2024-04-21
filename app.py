from flask import Flask, render_template, url_for, redirect, request
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
   data = request.form
   new_ad = Announcement(heading=data['heading'], description=data['description'], owner=data['owner'])
   try:
       db.session.add(new_ad)
       db.session.commit()
   except:
       db.session.rollback()
   return redirect(url_for('index'))

@app.route('/delete/<int:ad_id>', methods=['POST'])
def delete_ad(ad_id):
   ad_to_delete = Announcement.query.get_or_404(ad_id)
   try:
       db.session.delete(ad_to_delete)
       db.session.commit()
   except:
       db.session.rollback()
   return redirect(url_for('index'))

@app.route('/edit/<int:ad_id>', methods=['GET'])
def edit_form(ad_id):
   ad = Announcement.query.get_or_404(ad_id)
   return render_template('edit_form.html', ad=ad)

@app.route('/edit/<int:ad_id>', methods=['POST'])
def edit_ad(ad_id):
   ad_to_edit = Announcement.query.get_or_404(ad_id)
   data = request.form
   ad_to_edit.heading = data['heading']
   ad_to_edit.description = data['description']
   ad_to_edit.owner = data['owner']
   try:
       db.session.commit()
   except:
       db.session.rollback()
   return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug=True)
