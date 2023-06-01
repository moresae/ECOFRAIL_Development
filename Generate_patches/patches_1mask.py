import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.cluster import KMeans
from skimage import morphology


path = "/home/estudiante/Desktop/Development_ECOFRAIL/Generate_patches/M01_LT_TRANS_BMODE_1bfe0780-8645-450c-a302-110c4a26cd10.pkl"
path_cordPatches = "/home/estudiante/Desktop/Development_ECOFRAIL"

Npatches = 500
height, width = 5, 5
patch_length = height * 1E-3  # (mm)
patch_width = width * 1E-3  # (mm)

pitch = 200 * 1E-6  # (mm)
fs = 10 * 1E6  # Hz
sos = 1540  # m/s

# Cargar la imagen desde el archivo .pkl
with open(path, 'rb') as f:
    mask = pickle.load(f)

fig, ax = plt.subplots()
ax.imshow(mask)
px_white = np.argwhere(mask == 1)

# Aplicar la erosión a la imagen binaria para reducir el tamaño del músculo
px_reduce = morphology.disk(35)  # Tamaño del área de reducción: 30 píxeles
mask_reduce = morphology.erosion(mask, px_reduce)
mask_reduce = np.argwhere(mask_reduce == 1)

lenght_axial_px = patch_length / ((1 / fs) * (sos / 2))
width_px = patch_width / pitch

# Con el algoritmo de clustering K-means agrupo px blancos y obtengo los centroides de los clústers
Kpx = KMeans(n_clusters=Npatches).fit(mask_reduce)
pathCentroid = Kpx.cluster_centers_

px_coverage = set()
coord_patches = []

# Iterar sobre los centroides
for centroid in pathCentroid:
    px0 = int(centroid[1] - width_px / 2)
    py0 = int(centroid[0] - lenght_axial_px / 2)
    px1 = px0 + width_px
    py1 = py0 + lenght_axial_px
    patch_rec = patches.Rectangle((px0, py0), width_px, lenght_axial_px, linewidth=2, edgecolor='r', facecolor='none')
    coord_patches.append([px0, py0, px1, py1])
    ax.add_patch(patch_rec)
    px_coverage.update([(x, y) for x in range(int(px0), int(px1)) for y in range(int(py0), int(py1))])

print(f"Npatches: {Npatches} Mask_area: {len(px_white)} Patch_dimensions: {int(width_px)} x {int(lenght_axial_px)} Reduced_mask: {len(mask_reduce)} Cover: {len(px_coverage)}")

coverage = (len(px_coverage) / len(px_white)) * 100
coord_patches = np.array(coord_patches)
np.save(f"{path_cordPatches}/coordPatches.npy", coord_patches)
print(f"Percentage of coverage: {coverage} %")

plt.axis('off')
fig.savefig('patches1.png')
plt.show()
