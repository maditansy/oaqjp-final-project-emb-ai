"""
This module sets up a Flask application that provides an endpoint for emotion detection.
It uses the emotion_detector function to analyze text and returns the detected emotions
along with the dominant emotion.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['GET'])
def emo_detector():
    """
    Handle emotion detection requests. Analyzes the text provided as a query parameter
    and returns the detected emotions along with the dominant emotion.

    Returns:
        A formatted string with emotion analysis results or an error message.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "<p>Invalid text! Please try again.</p>", 400

    try:
        # Pass the text to the emotion_detector function and store the response
        response = emotion_detector(text_to_analyze)

        # Check if the dominant emotion is None (indicating an invalid text)
        if response['dominant_emotion'] is None:
            return "<p>Invalid text! Please try again.</p>", 400

        # Extract the emotion and score from the response
        anger            = response['anger']
        disgust          = response['disgust']
        fear             = response['fear']
        joy              = response['joy']
        sadness          = response['sadness']
        dominant_emotion = response['dominant_emotion']

        # Return a formatted string with the emotion response
        return (f"For the given statement, the system response is "
                f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
                f"'joy': {joy} and 'sadness': {sadness}. The dominant emotion is "
                f"<b>{dominant_emotion}</b>.")
    except KeyError as e:
        # Handle KeyError specifically if the expected keys are not found in the response
        return f"Unexpected response format: missing key {e}", 500

@app.route('/')
def render_index_page():
    """
    Render the index page.

    Returns:
        The rendered HTML content of the index page.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
