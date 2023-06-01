import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from sklearn.cluster import KMeans
from skimage import morphology


def load_mask_from_pickle(path):
    with open(path, 'rb') as f:
        mask = pickle.load(f)
        px_white = np.argwhere(mask == 1)
    return mask, px_white


def reduce_mask(mask):
    px_reduce = morphology.disk(35)  # Tamaño del área de reducción: 35 píxeles
    mask_reduce = morphology.erosion(mask, px_reduce)
    return mask_reduce


def generate_patches(px_white, mask_reduce, Npatches, height, width, pitch, fs, sos):
    # Obtener los píxeles blancos reducidos
    mask_reduce = np.argwhere(mask_reduce == 1)
    if len(mask_reduce) > 1:
        # Calcular las dimensiones en píxeles de los patches
        patch_length = height * 1E-3  # Convertir el tamaño del parche a metros
        patch_width = width * 1E-3  # Convertir el tamaño del parche a metros
        lenght_axial_px = patch_length / ((1 / fs) * (sos / 2))
        width_px = patch_width / pitch

        # Con el algoritmo de clustering K-means, agrupar píxeles blancos y obtener los centroides de los clústeres
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

            # Guardar las coordenadas del parche
            coord_patches.append([px0, py0, px1, py1])

            px_coverage.update([(x, y) for x in range(int(px0), int(px1)) for y in range(int(py0), int(py1))])
        coord_patches = np.array(coord_patches)
        print(f"Npatches: {Npatches} Mask_area: {len(px_white)} Patch_dimensions: {int(width_px)} x {int(lenght_axial_px)} Reduced_mask: {len(mask_reduce)} Cover: {len(px_coverage)}")
        coverage = (len(px_coverage) / len(px_white)) * 100
        print(f"Percentage of coverage: {coverage} %")
        
        return coord_patches, coverage

    else:
        return [], 0


def save_coord_patches(coord_patches, path):
    np.save(path, coord_patches)


def visualize_patches(name_mask, mask, coord_patches):
    fig, ax = plt.subplots()
    ax.imshow(mask)

    # Mostrar los parches en la imagen
    for coord_patch in coord_patches:
        px0, py0, px1, py1 = coord_patch
        patch_rec = patches.Rectangle((px0, py0), px1 - px0, py1 - py0, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(patch_rec)

    # Configurar la visualización y guardar la imagen con los parches
    plt.axis('off')
    fig.savefig(name_mask)
    plt.show()


# Parámetros
name_center = "Raw_data_Albacete"

path = f"/bifrost2/home/ssanabria/ECOFRAIL/CLARIUS_ECOFRAIL/{name_center}"
# pathmask = "/home/estudiante/Desktop/Development_ECOFRAIL/Generate_patches/M01_LT_TRANS_BMODE_1bfe0780-8645-450c-a302-110c4a26cd10.pkl"
patient_folder = sorted(os.listdir(path))
path_patchesCoord = "/home/estudiante/Desktop/Development_ECOFRAIL/Generate_patches/Out_patches/Patches_coord"
path_patchesImg = "/home/estudiante/Desktop/Development_ECOFRAIL/Generate_patches/Out_patches/Patches_img"
path_outCsv = "/home/estudiante/Desktop/Development_ECOFRAIL/Generate_patches/Out_patches"
Npatches = 200
height, width = 5, 5
pitch = 200 * 1E-6
fs = 10 * 1E6
sos = 1540





for patient in patient_folder:
    patient_path = os.path.join(path, patient)  # Ruta completa de la carpeta del paciente
    mask_path = os.path.join(patient_path, "RawMask_images.npy")


    if not os.path.exists(f"{patient_path}/Out_patches/Out_Patches_Img"):
        os.makedirs(f"{patient_path}/Out_patches/Out_Patches_Img")
    if not os.path.exists(f"{patient_path}/Out_patches/Out_Patches_Coord"):
        os.makedirs(f"{patient_path}/Out_patches/Out_Patches_Coord")
    

    if os.path.isfile(mask_path):
        masknpy = np.load(mask_path)
        print(type(masknpy[0]))
    
        data = []
        for maskpkl in sorted(masknpy):
            print(maskpkl)
            maskpkl_path = os.path.join(f"{patient_path}/Raw_Mask", maskpkl)
            print(maskpkl_path)
            print(f"______________________________________________________________________-: {patient}")

            mask, px_white = load_mask_from_pickle(maskpkl_path)
            print("Loading mask")
            # Reducir el tamaño del músculo
            mask_reduce = reduce_mask(mask)

            # Generar los parches
            coord_patches, coverage = generate_patches(px_white, mask_reduce, Npatches, height, width, pitch, fs, sos)
            print("Generating patches")
            if coverage != 0:

                # Guardar las coordenadas de los parches
                name_coord = maskpkl.replace("pkl", "npy")
                save_coord_patches(coord_patches, f"{patient_path}/Out_patches/Out_Patches_Coord/{name_coord}")

                # Visualizar los parches en la imagen
                name = maskpkl.replace("pkl", "png")
                visualize_patches(f"{patient_path}/Out_patches/Out_Patches_Img/{name}", mask, coord_patches)
                


                data.append({
                    'Patient': patient,
                    'Maskpkl_name': maskpkl.replace("pkl", "png"),
                    "Npatches": Npatches,
                    "Patch_size": [width, height],
                    "Coverage": coverage
                })
            else:
                data.append({
                    'Patient': patient,
                    'Maskpkl_name': maskpkl.replace("pkl", "png"),
                    "Npatches": 0,
                    "Patch_size": [0, 0],
                    "Coverage": 0
                })



    else:
        print(f"No se ha encontrado RawMask_images.npy en el paciente: {patient}")
df = pd.DataFrame(data)
df.to_csv(f'{path}/Out_{name_center}.csv', index=False)
