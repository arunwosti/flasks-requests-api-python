from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route("/newsletterinfo", methods=["POST"])
def get_newsletter_info():
    newsletter_name = request.form.get("newsletter")
    newsletter_api_key = request.form.get('apikey')

    url = f"http://example.com/newsletter/api/info?name={newsletter_name}&apikey={newsletter_api_key}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data.get('status') == 'success':
        return render_template("newsletter_info.html", newsletter_data=data)
    else:
        error_message = data.get('error', 'ERROR!!')
        return render_template("error.html", error_message=error_message)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500)