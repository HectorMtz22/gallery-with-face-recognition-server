from PIL import Image, ImageOps
import numpy as np

# Cargar la imagen
imagen = Image.open('uploads/imagen.jpg')

# Convertir a escala de grises
imagen_gris = ImageOps.grayscale(imagen)

# Convertir la imagen gris a un array numpy
imagen_gris_np = np.array(imagen_gris)

# Seleccionar un color para sombrear (por ejemplo, rojo con RGB (255, 0, 0))
color_sombreado = (0, 0, 255)

# Crear una matriz vacía para la imagen coloreada
datos_coloreados = np.zeros((imagen_gris_np.shape[0], imagen_gris_np.shape[1], 3), dtype=np.uint8)

# Aplicar el sombreado
for i in range(imagen_gris_np.shape[0]):
    for j in range(imagen_gris_np.shape[1]):
        datos_coloreados[i, j] = color_sombreado if imagen_gris_np[i, j] < 128 else (255, 255, 255)

# Crear la imagen sombreada a partir del array modificado
imagen_coloreada = Image.fromarray(datos_coloreados, 'RGB')

# Guardar la imagen sombreada
imagen_coloreada.save('uploads/imagen_sombreada_blue.jpg')

# Mostrar la imagen sombreada (opcional, puede causar advertencias en algunos sistemas Linux)
# imagen_coloreada.show()
