from flask import Flask, request, render_template, send_file, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import gridfs
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024  # 10GB

# MongoDB setup
client = MongoClient("mongodb+srv://sakshamranjan7:8wBCaYilCTlgdNV3@cluster0.h184m7m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['anime_stream']
fs = gridfs.GridFS(db)

OWNER_USER = "AI"
OWNER_PASS = "0909"

# -------------------------
# HOME PAGE
# -------------------------
@app.route('/')
def index():
    return render_template("index.html", owner=False)

# -------------------------
# OWNER LOGIN
# -------------------------
@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('user')
    password = request.form.get('pass')
    if user == OWNER_USER and password == OWNER_PASS:
        return render_template("index.html", owner=True)
    return "❌ Wrong credentials"

# -------------------------
# UPLOAD VIDEO
# -------------------------
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    if not file:
        return "No file uploaded"
    filename = secure_filename(file.filename)
    fs.put(file, filename=filename)
    link = url_for('watch', filename=filename, _external=True)
    return f"✅ Uploaded! Streaming link: <a href='{link}' target='_blank'>{link}</a>"

# -------------------------
# WATCH VIDEO
# -------------------------
@app.route('/watch/<filename>')
def watch(filename):
    grid_out = fs.find_one({'filename': filename})
    if not grid_out:
        return "⚠️ Video not available"
    return send_file(BytesIO(grid_out.read()), attachment_filename=filename, mimetype="video/mp4")

# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

