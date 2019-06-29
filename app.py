from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROJECT_ID'] = 'audiototext-api'
app.config['CLOUD_STORAGE_BUCKET'] = 'audiototext-api'
app.config['ALLOWED_EXTENSIONS'] = set(['flac', 'wav'])visu