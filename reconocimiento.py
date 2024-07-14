import cv2
import face_recognition
import os

# Directorio de imágenes de referencia
reference_directory = "reconocimiento"

# Cargar todas las imágenes de referencia y obtener sus codificaciones faciales
reference_encodings = []
reference_names = []

for file_name in os.listdir(reference_directory):
    if file_name.endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(reference_directory, file_name)
        image = cv2.imread(image_path)
        face_locations = face_recognition.face_locations(image)
        if face_locations:
            face_encodings = face_recognition.face_encodings(image, known_face_locations=[face_locations[0]])[0]
            reference_encodings.append(face_encodings)
            reference_names.append(os.path.splitext(file_name)[0])  # Usar el nombre del archivo sin la extensión como categoría

# Nueva imagen a comparar
new_image_path = "uploads/jonathan-1.jpeg"  # Cambia el nombre de la imagen según sea necesario
new_image = cv2.imread(new_image_path)
new_face_locations = face_recognition.face_locations(new_image, model="cnn")

if new_face_locations:
    for new_face_location in new_face_locations:
        new_face_encodings = face_recognition.face_encodings(new_image, known_face_locations=[new_face_location])[0]
        results = face_recognition.compare_faces(reference_encodings, new_face_encodings)
        
        if True in results:
            match_index = results.index(True)
            category = reference_names[match_index]
        else:
            category = "Desconocido"
        
        print("Categoría:", category)
else:
    print("No se encontraron caras en la nueva imagen.")
