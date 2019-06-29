from flask import current_app, flash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
from google.auth import compute_engine
from google.cloud import storage
import six


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.split('.').pop().lower() in allowed_extensions

def upload_file(file_stream, filename, content_type):
    # Upload audio file to google cloud and return public URL

    # Get a unique filename
    filename = secure_filename(filename)

    credentials = compute_engine.Credentials()
    client = storage.Client(credentials=credentials, project=current_app.config['PROJECT_ID'])

    bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    blob = bucket.blob(filename)
    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url
