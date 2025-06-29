from flask import Flask, request, render_template
import requests
import re

app = Flask(__name__)

def get_instagram_video_url(post_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        res = requests.get(post_url, headers=headers)
        match = re.search(r'"video_url":"([^"]+)"', res.text)
        if match:
            return match.group(1).replace("\u0026", "&").replace("\", "")
        else:
            return "⚠️ No video found or it's a photo post."
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    if request.method == "POST":
        urls = request.form["urls"].splitlines()
        for url in urls:
            url = url.strip()
            if url:
                results[url] = get_instagram_video_url(url)
    return render_template("index.html", results=results)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the port from Render
    app.run(debug=False, host='0.0.0.0', port=port)

