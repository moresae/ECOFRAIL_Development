import os
import csv


# Parámetros
name_center = "Raw_data_Albacete"

path = f"/bifrost2/home/ssanabria/ECOFRAIL/CLARIUS_ECOFRAIL/{name_center}"
# pathmask = "/home/estudiante/Desktop/Development_ECOFRAIL/Generate_patches/M01_LT_TRANS_BMODE_1bfe0780-8645-450c-a302-110c4a26cd10.pkl"
patient_folder = sorted(os.listdir(path))


csv_file = f"/bifrost2/home/ssanabria/ECOFRAIL/CLARIUS_ECOFRAIL/{name_center}/Out_Raw_data_Albacete.csv"


with open(csv_file, 'r') as file:

    csv_reader = csv.reader(file)

    for row in csv_reader:

        print(row)
