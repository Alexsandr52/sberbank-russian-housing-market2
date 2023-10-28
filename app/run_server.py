from flask import Flask, render_template, redirect, url_for, request
import pickle
import numpy as np
import pandas as pd
import sklearn



model = pickle.load(open('app/models/model.dump', 'rb'))
app = Flask(__name__)
heads = ('full_sq', 'female_f', 'build_count_monolith', 'cafe_count_3000', 'sport_count_3000', 'culture_objects_top_25', 'predict')
predicts = []
def predict(data):

	# data = {k: [int(v)] for k, v in data.items()}
	for k, v in data.items():
		if v.isdigit(): data[k] = [int(v)]
		else: data[k] = [np.nan]

	pred = model.predict(pd.DataFrame(data))
	print(pred)
	row = [v[0] for v in data.values()]
	row.append(round(np.exp(pred[0]), 2))
	predicts.append(row)


@app.route('/', methods=['POST','GET'])
def index():
	if request.method == 'POST':
		return redirect(url_for('form'))
		
	return render_template('index.html')

@app.route('/form', methods=['POST','GET'])
def form():
	data = {}
	if request.method == 'POST':
		data['full_sq'] = request.form['full_sq']
		data['female_f'] = request.form['female_f']
		data['build_count_monolith'] = request.form['build_count_monolith']
		data['cafe_count_3000'] = request.form['cafe_count_3000']
		data['sport_count_3000'] = request.form['sport_count_3000']
		try:
			request.form['culture_objects_top_25']
			data['bin_culture_objects_top_25'] = '0'
		except:
			# print(request.form['culture_objects_top_25'])
			data['bin_culture_objects_top_25'] = '1'
		
		predict(data)
	return render_template('form.html', heads=heads, predicts=predicts)


if __name__ == '__main__':
	app.run(port=8000, debug=True)
	print(sklearn.__version__)
