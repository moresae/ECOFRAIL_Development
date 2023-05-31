import sys
import os
import numpy as np

path = "/bifrost2/home/ssanabria/ECOFRAIL/CLARIUS_ECOFRAIL/Raw_data_Albacete"
folder_path = os.listdir(path)

patientListRaw = {}
patientListRawMask = {}
patient_iqRaw = {}

# Entra a cada paciente
for patient in folder_path:
    # folder_patient = os.listdir(f"{path}/{patient}")
    try: 
        path_rawlist = f"{path}/{patient}/Raw"
        raw_list = os.listdir(path_rawlist)
        rawMask_list = os.listdir(f"{path}/{patient}/Raw_Mask")
        
        folder_bmodeRaw = []
        bmodeRawMask = []

        # Ingresa a Raw_data 
        for folder_raw in raw_list:
            if "BMODE" in folder_raw and "." not in folder_raw:
                temp_path = f"{path_rawlist}/{folder_raw}"
                folder_bmodeRaw.append(temp_path)

        raw_iq_list = []
        iqRaw = []
        # Recorre c/carpeta de Raw 
        for file_rawbmode in folder_bmodeRaw:
            rawbmodeList = os.listdir(file_rawbmode) # lista de archivos BMODE (.raw .lzo .tgc .yml)
            for file_iqraw in rawbmodeList:
                if file_iqraw.endswith("_iq.raw"):
                    temp_path = f"{file_rawbmode}/{file_iqraw}"
                    raw_iq_list.append(temp_path) # lista con el directorio de c/archivo "_iq.raw" encontrado en todos los pacientes
                    iqRaw.append(file_iqraw) 
                patient_iqRaw[patient] = [len(iqRaw), sorted(iqRaw)]
        patient_iqRaw_npy = np.array(patient_iqRaw)
        np.save(f"{path}/{patient}/Raw_images.npy",patient_iqRaw_npy)


        # Ingresa a Raw_Mask y guarda de c/paciente los archivos .pkl
        for folder_rawMask in rawMask_list:
            if "BMODE" in folder_rawMask and ".pkl" in folder_rawMask:
                bmodeRawMask.append(folder_rawMask)
        patientListRawMask[patient] = [len(bmodeRawMask), sorted(bmodeRawMask)]
        patientListRawMask_npy = np.array(patientListRawMask)
        np.save(f"{path}/{patient}/RawMask_images.npy",patientListRawMask_npy)


    except:
        pass

print(patientListRawMask)
print(patient_iqRaw)

