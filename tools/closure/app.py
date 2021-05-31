import os
import subprocess
import uuid


from flask import Flask
from flask import request
from flask import jsonify


app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello():
	js_code = request.form.get('js_code')
	compilation_level = request.form.get('compilation_level', 'SIMPLE_OPTIMIZATIONS')
	in_file_name = '{}.js'.format(str(uuid.uuid4()))
	out_file_name = '{}.js'.format(str(uuid.uuid4()))

	with open(in_file_name, 'w') as file:
		file.write(js_code)

	process = subprocess.Popen(
		[
			'java', '-jar', 'compiler.jar',
			'--compilation_level', compilation_level,
			'--language_in', 'ECMASCRIPT5_STRICT',
			'--language_out', 'ECMASCRIPT5_STRICT',
			'--formatting', 'SINGLE_QUOTES',
			'--assume_function_wrapper',
			'--js', in_file_name,
			'--js_output_file', out_file_name,
		],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
	)

	stdout, stderr = process.communicate()
	app.logger.info(100 * '-')
	app.logger.info(f'In file name: {in_file_name}')
	app.logger.info(f'Out file name: {out_file_name}')
	app.logger.info(f'Std Out: {stdout}')
	app.logger.info(f'Std Err: {stderr}')
	app.logger.info(100 * '-')

	try:
		with open(out_file_name, 'r') as file:
			compiled_code = file.read()
		os.remove(in_file_name)
		os.remove(out_file_name)
	except Exception as e:
		app.logger.exception(e)
		compiled_code = ''

	return jsonify({
		'compiledCode': compiled_code,
		'errors': stderr.decode(),
		'output': stdout.decode(),
	})


if __name__ == '__main__':
	app.run(host='0.0.0.0')
