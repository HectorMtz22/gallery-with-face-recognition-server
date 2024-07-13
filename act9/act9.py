import cv2
import matplotlib.pyplot as plt

# Cargar la imagen
imagen = cv2.imread('./uploads/imagen.jpg')

# Convertir a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar el operador Sobel vertical
sobel_vertical = cv2.Sobel(imagen_gris, cv2.CV_64F, 1, 0, ksize=3)

# Mostrar la imagen original, la imagen en escala de grises y el resultado del Sobel vertical
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.title('Imagen Original')
plt.imshow(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))

plt.subplot(1, 3, 2)
plt.title('Imagen en Escala de Grises')
plt.imshow(imagen_gris, cmap='gray')

plt.subplot(1, 3, 3)
plt.title('Operador Sobel Vertical')
plt.imshow(sobel_vertical, cmap='gray')

plt.show()

# Guardar el resultado del operador Sobel vertical
cv2.imwrite('./uploads/imagen_sobel_vertical.jpg', sobel_vertical)