from flask import Flask, render_template, request
import requests

app = Flask(__name__)

NEWS_API_KEY = "fc2a6edc94fc44fdbfb7e1319643bfdf" 

@app.route('/')
def homepage():
    return render_template("index.html")

def get_newsletter_info():
    newsletter_name = request.form.get("newsletter")
    api_key = request.form.get('apikey')

    # Verifing that the API key matches expected API key
    if api_key != NEWS_API_KEY:
        return render_template("error.html", error_message="Invalid API Key")

    # Request to the News API
    url = f"https://newsapi.org/v2/everything?q={newsletter_name}&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200 and data.get('status') == 'ok':
            articles = data.get('articles', [])
            # Taking only first data
            if articles:
                first_article = articles[0]
                return render_template("newsletterinfo.html", newsletter_data=[first_article])
            else:
                return render_template("error.html", error_message="No articles found.")
        else:
            #  Error message 
            if data.get('message'):
                error_message = data.get('message')
                return render_template("error.html", error_message=error_message)
            else:
                return render_template("error.html", error_message="An unexpected error occurred.")

    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)  # For debugging
        return render_template("error.html", error_message=f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        print("Request Error:", err)  # For debugging
        return render_template("error.html", error_message=f"Request Error: {err}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500)
