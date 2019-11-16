from flask import Flask
from flask import request


app = Flask(__name__)

@app.route('/')
def index():
	return 'My son Favorite is Lie to my'

#parametros en orden sin nesesidad de ?
@app.route('/parametros/')
@app.route('/parametros/<name>')
def parametros(name = ''):
	param = request.args.get('parametro1', 'no hay nada')
	return 'Parametros es {}'.format(param)


if __name__ == '__main__':
	app.run(debug = True, port = 9620 )