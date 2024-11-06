from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import io

app = Flask(__name__)

# Enable CORS for all routes with multiple origins
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})

@app.route('/')
def index():
    return '''
    <h1>Welcome to the Text-to-Speech API</h1>
    <p>Use the following endpoints:</p>
    <h2>/convert</h2>
    <p>Convert text to speech.</p>
    <p>Method: POST</p>
    <p>Request Body (JSON):</p>
    <pre>
    {
        "text": "Your text here",
        "lang": "en"  // Optional, default is 'en'
    }
    </pre>
    <h2>/summarize</h2>
    <p>Summarize the provided text.</p>
    <p>Method: POST</p>
    <p>Request Body (JSON):</p>
    <pre>
    {
        "text": "Your text here"
    }
    </pre>
    '''

@app.route('/convert', methods=['GET', 'POST', 'OPTIONS'])
def convert_text_to_speech():
    if request.method == 'OPTIONS':
        # Handle preflight requests
        response = app.make_response('')
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    if request.method == 'POST':
        # Handle POST request
        data = request.json
        text = data.get('text')
        lang = data.get('lang', 'en')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        try:
            tts = gTTS(text=text, lang=lang)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)

            response = send_file(fp, mimetype='audio/mp3')
            response.headers.add("Access-Control-Allow-Origin", "*")  # This can also be restricted to specific origins
            return response
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({'error': 'An error occurred'}), 500

    return jsonify({'error': 'Method not allowed. Use POST to convert text to speech.'}), 405

@app.route('/summarize', methods=['POST'])
def summarize_text():
    try:
        data = request.get_json()
        text = data.get('text')
        
        # Example summary generation (you would implement your summarization logic here)
        summary = text[:100]  # Just an example of a "summary" for illustration purposes

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error details

if __name__ == '__main__':
    app.run(debug=True)
