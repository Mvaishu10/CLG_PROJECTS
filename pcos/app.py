from flask import Flask, render_template, request, jsonify
import pickle
import json
import connection as rec
import os

indices = pickle.load(open('indices.pkl', 'rb'))

app = Flask(__name__)
run_with_ngrok()


@app.route("/api/pcos", methods=['GET'])
def get_names():
    if request.method == 'GET':
        all_rest_names = indices.tolist()
        return all_rest_names


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        rest_name = request.form.get('user_input')
        rest_df = rec.similar_rests(rest_name)
        rest_json = json.loads(rest_df)
        return render_template('index.html', rec_rest=rest_json)


@app.route("/recommend")
def recommend():
    top_rest_str = rec.get_top_rests()
    top_rest_json = json.loads(top_rest_str)
    print(type(top_rest_json))

    image_name = os.listdir("static/top 30 images")
    image_name = ['/' + image for image in image_name]
    print(image_name)

    return render_template("main.html", top_rests=top_rest_json, image_name=image_name)


@app.route("/about")
def about():
    return render_template("main2.html")


if __name__ == "__main__":
    app.run(debug=True)
