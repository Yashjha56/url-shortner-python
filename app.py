from flask import Flask, request, redirect, render_template_string
import hashlib

app = Flask(__name__)

# Simple in-memory URL storage
urls = {}

HOME_HTML = """<!doctype html>
<title>URL Shortener</title>
<h1>URL Shortener</h1>
<form action="/" method="post">
  <input type="text" name="url" placeholder="Enter your URL here" required>
  <input type="submit" value="Shorten">
</form>
{% if short_url %}
<p>Short URL: <a href="{{ short_url }}">{{ short_url }}</a></p>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        original_url = request.form['url']
        short_id = hashlib.md5(original_url.encode()).hexdigest()[:6]
        urls[short_id] = original_url
        short_url = request.host_url + short_id
    return render_template_string(HOME_HTML, short_url=short_url)

@app.route('/<short_id>')
def redirect_to_url(short_id):
    original_url = urls.get(short_id, None)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
