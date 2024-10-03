import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import random
from PIL import Image

class encontrarUnion:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size

    def encontrar(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.encontrar(self.parent[x]) 
        return self.parent[x]

    def union(self, x, y):
        raizX = self.encontrar(x)
        raizY = self.encontrar(y)
        if raizX != raizY:
            if self.rank[raizX] > self.rank[raizY]:
                self.parent[raizY] = raizX
            elif self.rank[raizX] < self.rank[raizY]:
                self.parent[raizX] = raizY
            else:
                self.parent[raizY] = raizX
                self.rank[raizX] += 1

    def componentes(self):
        components = {}
        for i in range(len(self.parent)):
            raiz = self.encontrar(i)
            if raiz in components:
                components[raiz].append(i)
            else:
                components[raiz] = [i]
        return components

def binarizar(image, threshold=128):
    return np.where(image < threshold, 0, 1)

def componentesConectados(image, connectivity=4):
    height, width = image.shape
    etiquetas = np.zeros((height, width), dtype=int)
    uf = encontrarUnion(height * width)
    next_etiqueta = 1

    for y in range(height):
        for x in range(width):
            if image[y, x] == 0:
                continue
            
            vecinos = []
            if y > 0 and image[y - 1, x] == 1:
                vecinos.append(etiquetas[y - 1, x])
            if x > 0 and image[y, x - 1] == 1:
                vecinos.append(etiquetas[y, x - 1])
            
            if connectivity == 8:
                if y > 0 and x > 0 and image[y - 1, x - 1] == 1:
                    vecinos.append(etiquetas[y - 1, x - 1])
                if y > 0 and x < width - 1 and image[y - 1, x + 1] == 1:
                    vecinos.append(etiquetas[y - 1, x + 1])

            if not vecinos:
                etiquetas[y, x] = next_etiqueta
                next_etiqueta += 1
            else:
                min_etiqueta = min(vecinos)
                etiquetas[y, x] = min_etiqueta
                for neighbor in vecinos:
                    if neighbor != min_etiqueta:
                        uf.union(min_etiqueta - 1, neighbor - 1)

    for y in range(height):
        for x in range(width):
            if etiquetas[y, x] > 0:
                etiquetas[y, x] = uf.encontrar(etiquetas[y, x] - 1) + 1

    return etiquetas, uf

def colorear(image, etiquetas):
    seleccion_etiquetas = np.seleccion(etiquetas)
    imagenColoreada = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    colors = {etiqueta: [random.randint(0, 255) for _ in range(3)] for etiqueta in seleccion_etiquetas if etiqueta != 0}

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if etiquetas[y, x] != 0:
                imagenColoreada[y, x] = colors[etiquetas[y, x]]
    
    return imagenColoreada

def cargarImagenes(path, connectivity=4):
    
    all_files = os.listdir(path)
    
    images = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not images:
        print("Carpeta vacía")
        return
    
    for imagen in images:
        imagePath = os.path.join(path, imagen)
        print(f"Procesando: {imagePath}")
        
        try:
            image = Image.open(imagePath).convert('L')
            imagenBinaria = binarizar(np.array(image))
            plt.imshow(imagenBinaria, cmap='gray')
            plt.title(f'Imagen binarizada: {imagen}')
            plt.show()

            etiquetas, uf = componentesConectados(imagenBinaria, connectivity=connectivity)
            imagenColoreada = colorear(imagenBinaria, etiquetas)

            output_path = os.path.join(path, f"colored_{imagen}")
            plt.imsave(output_path, imagenColoreada)
            print(f"Procesada y guardada: {output_path}")
        except Exception as e:
            print(f"Error procesando {imagen}: {e}")

def main():
    path = r'C:\Users\Anna Beristain\Downloads\practica1.3'
    
    cargarImagenes(path, connectivity=4)

    cargarImagenes(path, connectivity=8)

if __name__ == "__main__":
    main()