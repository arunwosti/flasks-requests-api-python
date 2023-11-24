from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route("/movieinfo", methods=["POST"])
def get_movie_info():
    movie_name = request.form.get("movie")
    imdb_api_key = request.form.get('appid')

    # IMDb API URL
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={imdb_api_key}"

    response = requests.get(url)
    data = response.json()

    # Check if the request was successful
    if response.status_code == 200 and data['Response'] == 'True':
        return render_template("movie_info.html", movie_data=data)
    else:
        error_message = data.get('Error', 'An error occurred.')
        return render_template("error.html", error_message=error_message)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
