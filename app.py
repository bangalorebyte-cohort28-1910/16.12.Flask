from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.name


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print("post request submitted") 
        name = request.form['name']
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        name_list = User.query.all()
        return render_template('index.html',name_list=name_list)
    elif request.method == 'GET':
        print("get request is asked")
        return render_template('index.html')

@app.route('/about')
def about():
    return 'About US page'

@app.route('/contact')
def contact():
    return 'Contact Us page'

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)
