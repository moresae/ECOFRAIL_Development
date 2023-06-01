# ECOFRAIL_Development

## data_organization.py 
Contiene el código para organizar los datos de todas las máscaras de cada paciente y se guarga en un archivo con formato .pkl

También contiene archivos numpy en formato .npy de RF_iq.raw del Raw Data de todos los pacientes.

## Generate_patches
### patches_1mask.py
Este código toma una imagen binaria en formato .pkl que contiene una máscara del músculo. Luego, se realiza la erosión y se aplican los parámetros para la generación de patches. A continuación, se utiliza el algoritmo K-means para agrupar los píxeles blancos reducidos y obtener los centroides de los clústeres.

Después de calcular las dimensiones de los patches, se agregan dibujan patches "rectángulos" en la imagen. Finalmente, se guardan las coordenadas de los patches en un archivo .npy y se muestra la imagen con los parches resaltados.

### generate_patches.py
Este código es modular, genera en un archivo csv con la información del porcentaje de covertura de los patches de todo el centro