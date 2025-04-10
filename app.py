from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
from process_image import process_image

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({'status': 'Flask API running 🔥'})

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    ext = image.filename.rsplit('.', 1)[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    processed_filename = filename.rsplit('.', 1)[0] + '.png'
    processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)

    image.save(upload_path)

    success = process_image(upload_path, processed_path)
    if not success:
        return jsonify({'error': 'Processing failed'}), 500

    return jsonify({
        'success': True,
        'processed_url': f'/processed/{processed_filename}'
    })

@app.route('/processed/<filename>')
def serve_image(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
