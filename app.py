from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)

# Directorio donde se guardarán las imágenes
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # Change filename to secure filename 
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Start face recognition
        # ...

        # Insert image into database
        if (os.path.exists('db.json') == False):
            # Create it
            with open('db.json', 'w') as f:
                f.write('{"images": []}')


        with open('db.json', 'r') as user_file:
            file_contents = json.load(user_file)

        file_contents['images'].append({
            'filename': filename,
            'classification': -1,
            'is_primary': False
        })
        
        json.dump(file_contents, open('db.json', 'w'), indent=4)
    
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
