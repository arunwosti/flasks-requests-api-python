from flask import Flask, render_template, request
import requests

app = Flask(__name__)

NEWS_API_KEY = "82e3e00988e248129fdd4ff5fce3e220" 

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route("/newsletterinfo", methods=["POST"])
def get_newsletter_info():
    newsletter_name = request.form.get("newsletter")
    api_key = request.form.get('apikey')

    # Verify that the API key matches your expected API key
    if api_key != NEWS_API_KEY:
        return render_template("error.html", error_message="Invalid API Key")

    # Make a request to the News API
    url = f"https://newsapi.org/v2/everything?q={newsletter_name}&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200 and data.get('status') == 'ok':
            articles = data.get('articles', [])
            return render_template("newsletterinfo.html", newsletter_data=articles)
        else:
            error_message = data.get('message', 'ERROR!!')
            return render_template("error.html", error_message=error_message)

    except requests.exceptions.HTTPError as errh:
        return render_template("error.html", error_message=f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        return render_template("error.html", error_message=f"Request Error: {err}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500)
