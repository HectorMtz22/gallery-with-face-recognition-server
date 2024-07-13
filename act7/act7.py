import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen
imagen = cv2.imread('./uploads/imagen.jpg')

# Convertir la imagen de BGR a RGB
imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

# Crear una máscara de ceros (negra)
mascara = np.zeros(imagen.shape[:2], dtype="uint8")

# Definir el centro y el radio del círculo
centro = (imagen.shape[1] // 2, imagen.shape[0] // 2)
radio = min(imagen.shape[1] // 4, imagen.shape[0] // 4)

# Dibujar el círculo en la máscara (blanco)
cv2.circle(mascara, centro, radio, 255, -1)

# Aplicar la máscara a la imagen
imagen_mascarada = cv2.bitwise_and(imagen_rgb, imagen_rgb, mask=mascara)

# Mostrar la imagen original y la imagen con la máscara aplicada
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].imshow(imagen_rgb)
axs[0].set_title('Imagen Original')
axs[0].axis('off')

axs[1].imshow(imagen_mascarada)
axs[1].set_title('Imagen con Máscara')
axs[1].axis('off')

plt.show()

# Save the image with the mask applied
imagen_mascarada = cv2.cvtColor(imagen_mascarada, cv2.COLOR_RGB2BGR)

cv2.imwrite('./uploads/imagen_mascarada.jpg', imagen_mascarada)
