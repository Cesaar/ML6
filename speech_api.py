import io
import os

from flask import current_app, flash
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def audio_to_text(filename):
    # Initialize speech client
    client = speech.SpeechClient()

    # Get the file from the Google Cloud Storage bucket
    uri = 'gs://{0}/{1}'.format(current_app.config['CLOUD_STORAGE_BUCKET'], filename)
    audio = types.RecognitionAudio(uri=uri)

    config = types.RecognitionConfig(language_code='en-US')

    try:
        operation = client.long_running_recognize(config, audio)

        timeout_time = 900
        response = operation.result(timeout=timeout_time)

        # Concatenate translation results
        full_text = ''
        for result in response.results:
            # Do not consider alternatives
            full_text += u'{}. '.format(result.alternatives[0].transcript)

        return full_text
    except Exception as error:
        # For testing purpose only
        flash(str(error))
        return ''