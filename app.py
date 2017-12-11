import os
from flask import Flask, render_template, request
import recognize
import json
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 

@app.route("/")
def index():
	return render_template('upload.html')

@app.route("/upload", methods = ['POST'])
def upload():
	target = os.path.join(APP_ROOT,'images/')
	print(target)

	if not os.path.isdir(target):
		os.mkdir(target)

	for file in request.files.getlist('file'):
		print(file)
		filename = file.filename
		destination = "/".join([target,filename])
		print(destination)

		file.save(destination)

	ll = json.dumps(recognize.recognize(destination), indent = 2)
	f = open('./static/results.txt','w')
	f.write(ll)
	f.close()
	os.remove(destination)
	
	return render_template('actionDone.html')
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
if __name__ == "__main__":
	app.run()
