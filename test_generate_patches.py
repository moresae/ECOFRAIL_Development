import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.cluster import KMeans
from skimage import morphology


def load_mask_from_pickle(path):
    with open(path, 'rb') as f:
        mask = pickle.load(f)
    return mask


def reduce_mask(mask):
    px_reduce = morphology.disk(35)  # Tamaño del área de reducción: 35 píxeles
    mask_reduce = morphology.erosion(mask, px_reduce)
    return mask_reduce


def generate_patches(mask_reduce, Npatches, height, width, pitch, fs, sos):
    # Obtener los píxeles blancos reducidos
    mask_reduce = np.argwhere(mask_reduce == 1)

    # Calcular las dimensiones en píxeles de los parches
    patch_length = height * 1E-3  # Convertir el tamaño del parche a metros
    patch_width = width * 1E-3  # Convertir el tamaño del parche a metros
    lenght_axial_px = patch_length / ((1 / fs) * (sos / 2))
    width_px = patch_width / pitch

    # Con el algoritmo de clustering K-means, agrupar píxeles blancos y obtener los centroides de los clústeres
    kmeans = KMeans(n_clusters=Npatches).fit(mask_reduce)
    pathCentroid = kmeans.cluster_centers_

    coord_patches = []
    # Iterar sobre los centroides
    for centroid in pathCentroid:
        px0 = int(centroid[1] - width_px / 2)
        py0 = int(centroid[0] - lenght_axial_px / 2)
        px1 = px0 + width_px
        py1 = py0 + lenght_axial_px

        # Guardar las coordenadas del parche
        coord_patches.append([px0, py0, px1, py1])

    coord_patches = np.array(coord_patches)
    return coord_patches


def save_coord_patches(coord_patches, path):
    np.save(path, coord_patches)


def visualize_patches(mask, coord_patches):
    fig, ax = plt.subplots()
    ax.imshow(mask)

    # Mostrar los parches en la imagen
    for coord_patch in coord_patches:
        px0, py0, px1, py1 = coord_patch
        patch_rec = patches.Rectangle((px0, py0), px1 - px0, py1 - py0, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(patch_rec)

    # Configurar la visualización y guardar la imagen con los parches
    plt.axis('off')
    plt.show()


# Parámetros
# path = "/bifrost2/home/ssanabria/ECOFRAIL/CLARIUS_ECOFRAIL/Raw_data_Albacete"
pathmask = "/home/estudiante/Desktop/Development_ECOFRAIL/M01_LT_TRANS_BMODE_1bfe0780-8645-450c-a302-110c4a26cd10.pkl"

# folder_path = os.listdir(path)
path_cordPatches = "/home/estudiante/Desktop/Development_ECOFRAIL/Coordenadas_patches"
Npatches = 10
height, width = 2, 5
pitch = 200 * 1E-6
fs = 10 * 1E6
sos = 1540



mask = load_mask_from_pickle(pathmask)
print("Loading mask")
# Reducir el tamaño del músculo
mask_reduce = reduce_mask(mask)

# Generar los parches
coord_patches = generate_patches(mask_reduce, Npatches, height, width, pitch, fs, sos)
print("Generating patches")


# Guardar las coordenadas de los parches
save_coord_patches(coord_patches, f"{path_cordPatches}/coordPatches.npy")

# Visualizar los parches en la imagen
visualize_patches(mask, coord_patches)

# i=0
# for patient in folder_path:
#     # print(f"Entró {i} {patient}")
#     i += 1
#     try:
#         # Cargar la imagen desde el archivo .pkl
#         path_mask = f"{path}/{patient}/RawMask_images.npy"
#         mask_list = os.listdir(path_mask)
#         print(mask_list)
        
#         for mask in mask_list:
            
            
            
            
#     except:
#         pass
#     print("Algo ha pasado")
        
    

