from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__, static_folder="react-hello-world/build/static", template_folder="react-hello-world/build")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# SqlAlchemy - Initialize database
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)

  def __init__(self, name):
    self.name = name

class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class Indicator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

class IndicatorSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name')

indicator_schema = IndicatorSchema()
indicators_schema = IndicatorSchema(many=True)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

class TemplateSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name')

template_schema = TemplateSchema()
templates_schema = TemplateSchema(many=True)

# Routes go here
@app.route('/', methods=['GET'])
def index():
   return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    if request.args.get('starts'):
        start_string = request.args.get('starts')
        start_product_names = Product.query.filter(Product.name.startswith(start_string)).all()
        result = products_schema.dump(start_product_names)
        # list_of_products = [product['name'] for product in result]
        # return str(list_of_products)
        return jsonify(result)
    else:        
        all_products = Product.query.all()
        result = products_schema.dump(all_products)
        return jsonify(result)


@app.route('/product/<id>', methods=['POST','GET'])
def products(id): 
    if request.method == 'GET':
        result = Product.query.filter_by(id=id).first()
        return product_schema.jsonify(result)   
    elif request.method == 'POST':
        product_name = request.form['name']
        new_product = Product(name = product_name)
        db.session.add(new_product)
        db.session.commit()
        return f'Product {product_name} posted into database'
    else:
        return f'Invalid route'

@app.route('/indicators', methods=['GET'])
def get_indicators():
    if request.args.get('starts'):
        start_string = request.args.get('starts')
        start_indicator_names = Indicator.query.filter(Indicator.name.startswith(start_string)).all()
        result = indicators_schema.dump(start_indicator_names)
        return jsonify(result)
    else:        
        all_indicators = Indicator.query.all()
        result = products_schema.dump(all_indicators)
        return jsonify(result)

@app.route('/indicator/<name>', methods=['POST','GET'])
def indicator(name): 
    if request.method == 'GET':
        result = Indicator.query.filter_by(name=name).first()
        return indicator_schema.jsonify(result)   
    elif request.method == 'POST':
        indicator_name = request.form['name']
        new_product = Indicator(name = indicator_name)
        db.session.add(new_product)
        db.session.commit()
        return f'Indicator {indicator_name} posted into database'
    else:
        return f'Invalid route'

@app.route('/templates', methods=['GET'])
def get_templates():
    if request.args.get('starts'):
        start_string = request.args.get('starts')
        start_template_names = Template.query.filter(Template.name.startswith(start_string)).all()
        result = templates_schema.dump(start_template_names)
        return jsonify(result)
    else:        
        all_templates = Template.query.all()
        result = templates_schema.dump(all_templates)
        return jsonify(result)

@app.route('/template/<name>', methods=['POST','GET'])
def template(name): 
    if request.method == 'GET':
        result = Template.query.filter_by(name=name).first()
        return template_schema.jsonify(result)   
    elif request.method == 'POST':
        template_name = request.form['name']
        new_template = Template(name = template_name)
        db.session.add(new_template)
        db.session.commit()
        return f'Template {template_name} posted into database'
    else:
        return f'Invalid route'

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    for item in ['apple','mango','grapes']:
        db.session.add(Product(name='product'+item))
        db.session.add(Template(name='template'+item))
        db.session.add(Indicator(name='indicator'+item))
        db.session.commit()
    app.run(debug=True,port=5001)


