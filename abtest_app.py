from flask import Flask, render_template, request

from abtest_handler import AbTestHandler

app = Flask(__name__)

abh = AbTestHandler()


@app.route('/', methods=["POST", "GET"])
def index():
	if request.method == 'POST' :
		if 'submit_button_negative' in request.form:
			abh.send_feedback(0)  # do something
		elif 'submit_button_positive' in request.form:
			abh.send_feedback(1)  # do something else
		else:
			pass

	try:
		class_, last_id,test_id = abh.fetch_class()
		return render_template("index.html", class_=class_, last_id=last_id, test_id=test_id)
	except Exception as e:
		print(e)
		return render_template("failed.html")


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
