import os
import config
import urllib.request
from app import app
from flask import Flask, render_template, flash, request, redirect

import storage
import speech_api

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Validate file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files.get('file')
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if not (file and storage.allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS'])):
            flash('File is of illegal filetype')
            return redirect(request.url)
        
        # Upload to cloud storage
        public_url = storage.upload_file(
            file.read(),
            file.filename,
            file.content_type)

        # Start recognition
        recognized_text = speech_api.audio_to_text(file.filename)
        if(len(recognized_text) > 0):
            flash(recognized_text)

    return redirect('/')

# Program entry point
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.PORT)