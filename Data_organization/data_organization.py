import os
import numpy as np

path = "/bifrost2/home/ssanabria/ECOFRAIL/CLARIUS_ECOFRAIL/Raw_data_Albacete"
path_csv = "/home/estudiante/Desktop/Development_ECOFRAIL/Data_organization/data_Albacete.csv"
folder_path = sorted(os.listdir(path))

patientListRawMask = {}
patient_iqRaw = {}

for patient in folder_path:
    try:
        value = patient.split("_")
        center = value[0]
        patient_value = value[1]
        if len(value) == 2:
            post = 1
        if len(value) == 3:
            pre = 0
        

        raw_path = f"{path}/{patient}/Raw"
        raw_list = os.listdir(raw_path)
        rawMask_list = os.listdir(f"{path}/{patient}/Raw_Mask")

        bmodeRaw_list = []
        iqRaw_list = []

        for folder_raw in raw_list:
            if "BMODE" in folder_raw and "." not in folder_raw:
                bmodeRaw_list.extend(os.listdir(f"{raw_path}/{folder_raw}"))

        for file_rawbmode in bmodeRaw_list:
            if file_rawbmode.endswith("_iq.raw"):
                iqRaw_list.append(file_rawbmode)

        patient_iqRaw[patient] = [len(iqRaw_list), sorted(iqRaw_list)]
        # np.save(f"{path}/{patient}/Raw_images.npy", np.array(iqRaw_list))

        bmodeRawMask_list = [folder_rawMask for folder_rawMask in rawMask_list if "BMODE" in folder_rawMask and ".pkl" in folder_rawMask]
        patientListRawMask[patient] = [len(bmodeRawMask_list), sorted(bmodeRawMask_list)]
        # np.save(f"{path}/{patient}/RawMask_images.npy", np.array(bmodeRawMask_list))

    except:
        pass

# print(patientListRawMask)
# print(patient_iqRaw)