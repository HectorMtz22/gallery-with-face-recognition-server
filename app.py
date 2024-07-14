from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import json
import os
import datetime
from flask_cors import CORS

# Import our face recognition module
from reconocimiento import initialize_categories, get_image_category

app = Flask(__name__)
CORS(app)

# Directorio donde se guardarán las imágenes
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Crear Database si no existe
if (os.path.exists('db.json') == False):
    # Create it
    with open('db.json', 'w') as f:
        f.write('{"images": [], "categories": []}')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Face Recognition Variables
reference_encodings = []
reference_names = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def initialize():
    reference_directory = 'reconocimiento'
    global reference_encodings, reference_names
    reference_encodings, reference_names = initialize_categories(reference_directory)

    # Update db.json
    with open('db.json', 'r') as user_file:
        file_contents = json.load(user_file)
        # Reset categories
        file_contents['categories'] = []

    for name in reference_names:
        file_contents['categories'].append(name)

    json.dump(file_contents, open('db.json', 'w'), indent=4)

    print({"status": "Categorías inicializadas"})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # Change filename to secure filename 
        suffix = secure_filename(file.filename)
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{date}_{suffix}'

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Start face recognition
        # ...

        with open('db.json', 'r') as user_file:
            file_contents = json.load(user_file)

        file_contents['images'].append({
            'filename': filename,
            'classification': -1,
            'is_primary': False
        })
        
        # json.dump(file_contents, open('db.json', 'w'), indent=4)

        # Categorizar la imagen
        category = get_image_category(file_path, reference_encodings, reference_names)

        for image in file_contents['images']:
            if image['filename'] == filename:
                image['classification'] = category
                break

        json.dump(file_contents, open('db.json', 'w'), indent=4)
    
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/categories', methods=['GET'])
def get_categories():
    with open('db.json', 'r') as user_file:
        file_contents = json.load(user_file)
        return jsonify(file_contents['categories'])

@app.route('/gallery', methods=['GET'])
def get_gallery():
    with open('db.json', 'r') as user_file:
        file_contents = json.load(user_file)
        return jsonify(file_contents['images'])

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    initialize()
    app.run(debug=True)
