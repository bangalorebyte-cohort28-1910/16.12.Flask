from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flask!'

@app.route('/about/')
def about():
    return 'About US page'

@app.route('/contact')
def contact():
    return 'Contact Us page'

if __name__ == '__main__':
    app.run(debug=True)