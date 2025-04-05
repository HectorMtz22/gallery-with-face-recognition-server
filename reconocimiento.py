import cv2
import face_recognition
import os

import uuid
import json

def initialize_categories(reference_directory):
    reference_encodings = []
    reference_names = []
    processed_names = set()  # Mantener un registro de los nombres ya procesados

    categories = []

    # Verifica las categorías en db.json
    with open('db.json', 'r') as user_file:
        file_contents = json.load(user_file)
        images = file_contents['images']
        for image in images:
            if image['classification'] != -1:
                if image['filename'] not in processed_names:
                    # Solo agrega una imagen
                    categories.append(image)
                    processed_names.add(image['filename'])  # Marcar este nombre como procesado

    # Procesar las imágenes de referencia
    # Verifica si el directorio de referencia existe
    if not os.path.exists(reference_directory):
        raise FileNotFoundError(f"El directorio {reference_directory} no existe.")
    # Verifica si hay imágenes en el directorio de referencia
    if not os.listdir(reference_directory):
        raise FileNotFoundError(f"No se encontraron imágenes en el directorio {reference_directory}.")
    # Procesar las imágenes de referencia
    # Iterar sobre las imágenes en el directorio de referencia
    print("Inicializando categorías...")
    for element in categories:
        print(element)
        file_name = element['filename']
        classification = element['classification']

        if file_name.endswith(('.jpg', '.jpeg', '.png')):
            # Obtener el nombre de la imagen sin la extensión
            # name_without_extension = os.path.splitext(file_name)[0]

            image_path = os.path.join(reference_directory, file_name)
            image = cv2.imread(image_path)
            face_locations = face_recognition.face_locations(image)
            if face_locations:
                face_encodings = face_recognition.face_encodings(image, known_face_locations=[face_locations[0]])[0]
                # Si hay más de una cara en la imagen, se toma la primera
                reference_encodings.append(face_encodings)
                reference_names.append(classification)
    
    return reference_encodings, reference_names

def get_image_category(new_image_path, reference_encodings, reference_names):
    new_image = cv2.imread(new_image_path)
    new_face_locations = face_recognition.face_locations(new_image, model="hog")

    if new_face_locations:
        for new_face_location in new_face_locations:
            new_face_encodings = face_recognition.face_encodings(new_image, known_face_locations=[new_face_location])[0]
            results = face_recognition.compare_faces(reference_encodings, new_face_encodings)
            
            if True in results:
                match_index = results.index(True)
                category = reference_names[match_index]
            else:
                category = "Desconocido"
            
            return category
    else:
        return "No se encontraron caras en la nueva imagen."

# Ejemplo de uso:
# reference_directory = "reconocimiento"
# reference_encodings, reference_names = initialize_categories(reference_directory)

# new_image_path = "uploads/jonathan-1.jpeg"  # Cambia el nombre de la imagen según sea necesario
# category = get_image_category(new_image_path, reference_encodings, reference_names)
# print("Categoría:", category)
