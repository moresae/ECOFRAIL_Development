import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.cluster import KMeans


path = "/bifrost2/home/ssanabria/ECOFRAIL/CLARIUS_ECOFRAIL/Raw_data_Albacete"
pathmask = "/home/estudiante/Desktop/Development_ECOFRAIL/M01_LT_TRANS_BMODE_1bfe0780-8645-450c-a302-110c4a26cd10.pkl"
path_cordPatches = "/home/estudiante/Desktop/Development_ECOFRAIL"

# for patient in folder_path:
#     try:
#         #Cargar datos
#         # Cargar la imagen desde el archivo .pkl
#         with open(path, 'rb') as f:
#             mask = pickle.load(f)

#         patches = np.zeros([Nframes*Npatches, Nlines, Naxial, 1])
#         z = 0.5*(sos/fs)
#     except:
#         pass

pitch = (200)*1E-6 #(mm)
height,width = (10,10)
patch_length = (height)*1E-3 #(mm)
patch_width = (width)*1E-3 #(mm)


# Cargar la imagen desde el archivo .pkl
with open(pathmask, 'rb') as f:
    mask = pickle.load(f)

# Matriz para almacenar los px blancos
px_white=[]
fig, ax = plt.subplots()
ax.imshow(mask)

# Obtener las dimensiones de la máscara (384*784)
heightmask, widthmask = mask.shape

# Recorrer la imagen para almacenar los px blancos
for row in range(heightmask):
    for column in range(widthmask):    
        if mask[row][column] == 1:        
            px_white.append([row, column])
px_white = np.array(px_white) # array que contiene todos los px blancos

# circle = plt.Circle((px_white[0][1], px_white[0][0]), 2, color='red',fill=False)
# ax.add_patch(circle)
lenght_axial_px = patch_length/pitch
width_px = patch_width/pitch
Npatches = int(len(px_white)/(lenght_axial_px*width_px))

print(len(px_white),width_px, lenght_axial_px, Npatches)

# Con el algoritmo de clustering K-means agrupo px blancos y obtengo los centroides de los clústers
Kpx = KMeans(n_clusters = Npatches).fit(px_white)
pathCentroid = Kpx.cluster_centers_

coord_patches = []
# Iterar sobre los centroides 
for centroid in pathCentroid:
    px0 = int(centroid[1]-width_px/2)
    py0 = int(centroid[0]-lenght_axial_px/2)
    px1 = px0 + width_px
    py1 = py0 + lenght_axial_px
    patch_rec = patches.Rectangle((px0,py0), width_px, lenght_axial_px, linewidth = 2, edgecolor = 'r', facecolor = 'none')
    ax.add_patch(patch_rec)
    coord_patches.append([px0,py0,px1,py1])
coord_patches = np.array(coord_patches)
np.save(f"{path_cordPatches}/coordPatches.npy", coord_patches)
print(coord_patches)

plt.axis('off')
fig.savefig('patches.png')
plt.show()