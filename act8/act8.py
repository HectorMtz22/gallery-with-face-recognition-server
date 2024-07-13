import cv2
import matplotlib.pyplot as plt

# Cargar la imagen
imagen = cv2.imread('./uploads/imagen.jpg')

# Convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar el algoritmo de Canny para la detección de bordes
bordes = cv2.Canny(imagen_gris, 100, 200)

# Mostrar la imagen original, la imagen en escala de grises y los bordes detectados
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

axs[0].imshow(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
axs[0].set_title('Imagen Original')
axs[0].axis('off')

axs[1].imshow(imagen_gris, cmap='gray')
axs[1].set_title('Escala de Grises')
axs[1].axis('off')

axs[2].imshow(bordes, cmap='gray')
axs[2].set_title('Detección de Bordes - Canny')
axs[2].axis('off')

plt.show()

# Guardar la imagen con los bordes detectados
cv2.imwrite('./uploads/imagen_bordes.jpg', bordes)