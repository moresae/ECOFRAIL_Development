import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.cluster import KMeans
from skimage import morphology


def load_mask_from_pickle(path):
    with open(path, 'rb') as f:
        mask = pickle.load(f)
    return mask


def reduce_mask(mask):
    px_reduce = morphology.disk(35)  # Tamaño del área de reducción: 30 píxeles
    mask_reduce = morphology.erosion(mask, px_reduce)
    mask_reduce = np.argwhere(mask_reduce == 1)
    return mask_reduce


def calculate_patch_dimensions(height, width, pitch, fs, sos):
    patch_length = height * 1E-3  # (mm)
    patch_width = width * 1E-3  # (mm)
    lenght_axial_px = patch_length / ((1 / fs) * (sos / 2))
    width_px = patch_width / pitch
    return lenght_axial_px, width_px


def cluster_patches(mask_reduce, n_patches):
    Kpx = KMeans(n_clusters=n_patches).fit(mask_reduce)
    pathCentroid = Kpx.cluster_centers_
    return pathCentroid


def generate_patch_coordinates(pathCentroid, width_px, lenght_axial_px):
    coord_patches = []
    for centroid in pathCentroid:
        px0 = int(centroid[1] - width_px / 2)
        py0 = int(centroid[0] - lenght_axial_px / 2)
        px1 = px0 + width_px
        py1 = py0 + lenght_axial_px
        coord_patches.append([px0, py0, px1, py1])
    return np.array(coord_patches)


def calculate_coverage(px_white, px_coverage):
    coverage = (len(px_coverage) / len(px_white)) * 100
    return coverage


def plot_patches(mask, coord_patches, px_white, px_coverage, Npatches):
    fig, ax = plt.subplots()
    ax.imshow(mask)
    for patch_coords in coord_patches:
        px0, py0, px1, py1 = patch_coords
        patch_rec = patches.Rectangle((px0, py0), px1 - px0, py1 - py0, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(patch_rec)
    print(f"Npatches: {Npatches} Mask_area: {len(px_white)} Patch_dimensions: {int(px1-px0)} x {int(py1-py0)} Reduced_mask: {len(px_coverage)} Cover: {len(px_coverage)}")
    plt.axis('off')
    fig.savefig('patches1.png')
    plt.show()


# Configuración
path = "/home/estudiante/Desktop/Development_ECOFRAIL/M01_LT_TRANS_BMODE_1bfe0780-8645-450c-a302-110c4a26cd10.pkl"
path_cordPatches = "/home/estudiante/Desktop/Development_ECOFRAIL"
Npatches = 500
height, width = 5, 5
pitch = 200 * 1E-6  # (mm)
fs = 10 * 1E6  # Hz
sos = 1540  # m/s

# Cargar la imagen desde el archivo .pkl
mask = load_mask_from_pickle(path)

# Reducción de la máscara
mask_reduce = reduce_mask(mask)

# Cálculo de las dimensiones del parche
lenght_axial_px, width_px = calculate_patch_dimensions(height, width, pitch, fs, sos)

# Agrupar los parches utilizando K-means
pathCentroid = cluster_patches(mask_reduce, Npatches)

# Generar las coordenadas de los parches
coord_patches = generate_patch_coordinates(pathCentroid, width_px, lenght_axial_px)

# Calcular la cobertura de los parches
px_white = np.argwhere(mask == 1)
px_coverage = set([(x, y) for x in range(int(px0), int(px1)) for y in range(int(py0), int(py1))])
coverage = calculate_coverage(px_white, px_coverage)

# Guardar las coordenadas de los parches
np.save(f"{path_cordPatches}/coordPatches.npy", coord_patches)

# Generar la visualización de los parches
plot_patches(mask, coord_patches, px_white, px_coverage, Npatches)

# Imprimir el porcentaje de cobertura
print(f"Percentage of coverage: {coverage} %")
