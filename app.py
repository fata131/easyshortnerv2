from flask import Flask, request, redirect, render_template
import json
import os
import string
import random

app = Flask(__name__)
DATA_FILE = 'urls.json'

def load_urls():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_urls(urls):
    with open(DATA_FILE, 'w') as f:
        json.dump(urls, f, indent=2)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    urls = load_urls()
    if request.method == 'POST':
        original_url = request.form['url']
        code = generate_short_code()
        urls[code] = original_url
        save_urls(urls)
        return f"Your short link: <a href='/{code}'>easyshortner.ly/{code}</a>"
    return render_template('index.html')

@app.route('/<code>')
def redirect_url(code):
    urls = load_urls()
    if code in urls:
        return redirect(urls[code])
    return 'Invalid link', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
