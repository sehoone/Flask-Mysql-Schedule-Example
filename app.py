from flask import Flask, url_for, render_template, request, redirect, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

import time
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<userName>:<pwd>@<ip>:<Port>/<DBName>?charset=utf8'
db = SQLAlchemy(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

###Models####
class Product(db.Model):
	__tablename__ = "products"
	__table_args__ = {"mysql_collate":"utf8_general_ci"}
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20))
	productDescription = db.Column(db.String(100))
	productBrand = db.Column(db.String(20))
	price = db.Column(db.Integer)

	def create(self):
	  db.session.add(self)
	  db.session.commit()
	  return self
	def __init__(self,title,productDescription,productBrand,price):
		self.title = title
		self.productDescription = productDescription
		self.productBrand = productBrand
		self.price = price
	def __repr__(self):
		return '' % self.id
db.create_all()
class ProductSchema(ModelSchema):
	class Meta(ModelSchema.Meta):
		model = Product
		sqla_session = db.session
	id = fields.Number(dump_only=True)
	title = fields.String(required=True)
	productDescription = fields.String(required=True)
	productBrand = fields.String(required=True)
	price = fields.Number(required=True)

@app.route('/run-tasks')
def run_tasks():
	for i in range(2):
		app.apscheduler.add_job(func=scheduled_task, trigger='interval', seconds=10, args=[i], id='j'+str(i))
 
	return 'Scheduled several long running tasks.', 200
 
def scheduled_task(task_id):
	for i in range(5):
		time.sleep(1)
		print('Task {} running iteration {}'.format(task_id, i))

@app.route('/products', methods = ['GET'])
def index():
	get_products = Product.query.all()
	product_schema = ProductSchema(many=True)
	products = product_schema.dump(get_products)
	print(make_response(jsonify({"product": products})))
	return make_response(jsonify({"product": products}))

@app.route('/products', methods = ['POST'])
def create_product():
	testVal = '{ "price": "222", "productBrand": "ㄷㄷ", "productDescription": "ㅂㅂ", "title": "ㄷㄷ" }'
	#data = request.get_json()
	data = json.loads(testVal)
	product_schema = ProductSchema()
	product = product_schema.load(data)
	result = product_schema.dump(product.create())
	return make_response(jsonify({"product": result}),200)

if __name__ == '__main__':
	app.debug = True
	db.create_all()
	app.secret_key = "123"
	app.run(host='0.0.0.0')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()


# class User(db.Model):
# 	""" Create user table"""
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(80), unique=True)
# 	password = db.Column(db.String(80))

# 	def __init__(self, username, password):
# 		self.username = username
# 		self.password = password


# @app.route('/', methods=['GET', 'POST'])
# def home():
# 	""" Session control"""
# 	if not session.get('logged_in'):
# 		return render_template('index.html')
# 	else:
# 		if request.method == 'POST':
# 			username = getname(request.form['username'])
# 			return render_template('index.html', data=getfollowedby(username))
# 		return render_template('index.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	"""Login Form"""
# 	if request.method == 'GET':
# 		return render_template('login.html')
# 	else:
# 		name = request.form['username']
# 		passw = request.form['password']
# 		try:
# 			data = User.query.filter_by(username=name, password=passw).first()
# 			if data is not None:
# 				session['logged_in'] = True
# 				return redirect(url_for('home'))
# 			else:
# 				return 'Dont Login'
# 		except:
# 			return "Dont Login"

# @app.route('/register/', methods=['GET', 'POST'])
# def register():
# 	"""Register Form"""
# 	if request.method == 'POST':
# 		new_user = User(username=request.form['username'], password=request.form['password'])
# 		db.session.add(new_user)
# 		db.session.commit()
# 		return render_template('login.html')
# 	return render_template('register.html')

# @app.route("/logout")
# def logout():
# 	"""Logout Form"""
# 	session['logged_in'] = False
# 	return redirect(url_for('home'))

# @app.route('/run-tasks')
# def run_tasks():
#     for i in range(2):
#     	app.apscheduler.add_job(func=scheduled_task, trigger='interval', seconds=5, args=[i], id='j'+str(i))
 
#     return 'Scheduled several long running tasks.', 200
 
# def scheduled_task(task_id):
#     for i in range(5):
#         time.sleep(1)
#         print('Task {} running iteration {}'.format(task_id, i))

# if __name__ == '__main__':
# 	app.debug = True
# 	db.create_all()
# 	app.secret_key = "123"
# 	app.run(host='0.0.0.0')
	