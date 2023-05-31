# ECOFRAIL_Development

## data_organization.py 
Contiene el código para organizar los datos de todas las máscaras de cada paciente y se guarga en un archivo con formato .pkl

También contiene archivos numpy en formato .npy de RF_iq.raw del Raw Data de todos los pacientes.

## generate_patches.py
Este código toma una imagen binaria en formato .pkl que contiene una máscara del músculo. Luego, se realiza la erosión para reducir el tamaño del músculo y se aplican los parámetros para la generación de parches. A continuación, se utiliza el algoritmo K-means para agrupar los píxeles blancos reducidos y obtener los centroides de los clústeres.

Después de calcular las coordenadas de los parches, se agregan rectángulos en la imagen para visualizar los parches. Finalmente, se guardan las coordenadas de los parches en un archivo .npy y se muestra la imagen con los parches resaltados.