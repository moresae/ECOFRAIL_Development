import numpy as np
import os
import pickle

path = "/bifrost2/home/ssanabria/ECOFRAIL/CLARIUS_ECOFRAIL/Raw_data_Albacete"
pathmask = "/home/estudiante/Desktop/Development_ECOFRAIL/M01_LT_TRANS_BMODE_1bfe0780-8645-450c-a302-110c4a26cd10.pkl"
folder_path = os.listdir(path)

Npatches = 150
Naxial = 120
Nlines = 192
sos = 1540 


# for patient in folder_path:
#     try:
#         #Cargar datos
#         # Cargar la imagen desde el archivo .pkl
#         with open(path, 'rb') as f:
#             RF_mask = pickle.load(f)

#         patches = np.zeros([Nframes*Npatches, Nlines, Naxial, 1])
#         z = 0.5*(sos/fs)
#     except:
#         pass


# Cargar la imagen desde el archivo .pkl
with open(pathmask, 'rb') as f:
    RF_mask = pickle.load(f)

#Obtener las dimensiones de la máscara (384*784)
ancho = RF_mask.shape[1]
alto = RF_mask.shape[0]

# Calcular el área de la máscara
area = (RF_mask == 1).sum()
area_mask = sum(sum(row) for row in RF_mask)


# Dimensión de pixel 
sizepx = 1/area


RF_mask[RF_mask == 0] = 1
# no lo sé
Nframes = RF_mask.shape[0]
maskArea = np.zeros(Nframes)
# coverage = np.zeros(maskArea)
# patches = np.zeros([Nframes*Npatches, Nlines, Naxial, 1])


print(ancho)
print(alto)
print(area)
print(area_mask)
print(RF_mask)


# """
# Tamaño del rawdata (384*784) (Imagen de la máscara)
# Transductor --> #de cristales que tiene dentro --> 192 líneas
# f = 4MHz
# Necesito calcular 


# Transductor_coord_X = element_index(0...191)*(separación geométrica entre los elementos de los cristales)(pitch)
# separación geométrica (pitch)del array 0.2mm 

# picht del array = 200um --> comprobar en el código el valor
# la distacia entre 2px corresponde al periodo del muestreo

# para llegar a 
# patches de 10mm*10mm
# calcular el npx que necesito 10/

# quiero que me generes 50 patches de c/img de tamaño 10mm, de forma aleatoria va a empezar a buscar patches por toda la imagen dentro del perímetro
# input --> img = Nlines * NRFsamples
# output --> array 3D --> patchCollection = Npatches * WidthPatch * HeighPatch (height más grande que el widthpatch)
# """
