import pickle
import numpy as np

def load(file_name):
    with open(file_name, 'rb') as pickle_file:
        return pickle.load(pickle_file)
model = load('C:/Users/giladBrudner/myproject/model.pkl')

from flask import Flask,request,render_template,send_file

#initialize the server
app = Flask(__name__)

#define what to do when client requests to reach path '/'
@app.route('/', methods=['GET'])
def hello_world():
    return ('Hello, World!')

#even though we are not using the HTTP POST request, we can still feed the server with variables using this syntax
@app.route('/<username>', methods=['GET'])
def hello_user(username):
    # show the user profile for that user
    return ('Hello %s' % username)

@app.route('/get_image', methods=['GET'])
def get_image():
	if request.args.get('type') == '1':
		filename = 'ok.gif'
	else:
		filename = 'error.gif'
	return send_file(filename, mimetype='image/gif')

#define a route that receives URL parameters and returns a value
@app.route('/predict_get', methods=['GET'])
def show_post():
	variables=[]
	columns = ['average_montly_hours','number_project','last_evaluation','satisfaction_level']
	for column in columns:
		variables.append(float(request.args.get(column)))
	a = model.predict(np.array(variables).reshape(1,-1))[0]
	if a==0:
		return ("Prediction: Employee won't leave")
	else:
		return ("Prediction: Employee will leave")	

#define a routing that displays an html form
@app.route('/index')
def index():
    return (render_template('index.html')) #a form that send a post request to /predict_post

#define a route that receives a post request and returns a value
@app.route('/predict_post', methods=['POST'])
def pred_post():
	result=request.form
	variables = [float(result['average_montly_hours']),
				float(result['number_project']),
				float(result['last_evaluation']),
				float(result['satisfaction_level'])]
	a = model.predict(np.array(variables).reshape(1,-1))[0]
	if a==0:
		return ("Prediction: Employee won't leave")
	else:
		return ("Prediction: Employee will leave")