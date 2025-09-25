import pandas as pd

'''
https://datos.cdmx.gob.mx/dataset/reportes-de-agua

https://datos.cdmx.gob.mx/dataset/57ffc13a-7207-4b69-a9a9-2fef3fce6331/resource/a8069e94-c7cb-45d7-8166-561e80884422/download/reportes_agua_2024_01.csv

******************* Reportes de agua *******************
En este conjunto de datos encontrarás la información diaria referente a los reportes realizados
por ciudadanos con respecto a servicios del Sistema de Aguas de la Ciudad de México en tres ejes:
Drenaje, agua potable y agua tratada.

La tabla cuenta con información diaria sobre reportes referentes a diversos temas, entre ellos:

Fugas
Drenaje obstruido
Falta de agua
Mala calidad
Mal uso
Encharcamientos
La información puede desagregarse por el medio de recepción del reporte, la clásificación,
colonia, alcaldía y coordenadas puntuales.

La información es actualizada mensualmente, sin embargo, el recurso Histórico de reportes de
agua (2018-2021) muestra únicamente la información capturada por el antiguo sistema de registro,
previo a 2022, por lo cual es un archivo histórico que no se actualiza.
'''

'''
csv_files = [
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/reportes_agua_2024_01.csv",
]

dataframes = []

for i, file in enumerate(csv_files):
    df = pd.read_csv(file)
    dataframes.append(df)
    print(df.columns.tolist())
    print(df.head())



def mostrar_valores_unicos(df, columna):
    if columna not in df.columns:
        print(f"La columna '{columna}' no existe en este dataset.")
        return
    print("Conteo por valor: ")
    print(df[columna].value_counts())

mostrar_valores_unicos(dataframes[0], "clasificacion")
print()
mostrar_valores_unicos(dataframes[0], "reporte")


# Nueva dataframe para limpieza de datos
# Drenaje Obstruido, Brote en aguas negras, Encharcamiento, 

valores_interes = ["Drenaje Obstruido", "Brote en aguas negras", "Encharcamiento"]
df_filtrado = dataframes[0][dataframes[0]["reporte"].isin(valores_interes)]

print(f"\nNúmero de filas después del filtrado: {len(df_filtrado)}")
print(df_filtrado.head())

output_path = "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/reportes_de_agua_filtrados.csv"
df_filtrado.to_csv(output_path, index=False, encoding="utf-8")
print(f"\nArchivo guardado en: {output_path}")
'''

############################################################################################

'''
https://datos.cdmx.gob.mx/dataset/0311

https://datos.cdmx.gob.mx/dataset/529aac27-d1c1-426f-8c45-fd76fba43bf4/resource/44913088-806d-4f80-acca-1409a8225e9c/download/locatel0311-2024.csv
https://datos.cdmx.gob.mx/dataset/529aac27-d1c1-426f-8c45-fd76fba43bf4/resource/1ece1ddf-3e82-44f4-9435-486b1b9167f5/download/locatel0311-2023.csv
https://archivo.datos.cdmx.gob.mx/suac/locatel0311-2022.csv
https://archivo.datos.cdmx.gob.mx/suac/locatel0311-2021.csv
https://archivo.datos.cdmx.gob.mx/suac/locatel0311-2020.csv
https://archivo.datos.cdmx.gob.mx/suac/locatel0311-2019.csv

******************* Solicitudes *0311 *******************
Descripción

El conjunto de datos de 0311 Locatel muestra información de solicitudes realizadas a través del sistema 0311 Locatel.

El sistema 0311 Locatel es el primer sistema de este tipo en América Latina que concentra todas las solicitudes realizadas al gobierno de la Ciudad de México en una plataforma que permite una atención cálida, rápida y efectiva.

Las personas pueden realizar su solicitud a través de los siguientes medios, la nueva marcación corta * 0311 o el número 5556581111, chat habilitado en los principales sitios web del Gobierno de la Ciudad de México, la App CDMX, redes sociales de Locatel, y en las distintas áreas de atención ciudadana en dependencias y alcaldías.

El nuevo sistema incluye notificaciones del avance de los reportes de manera automatizada así como para informar la viabilidad del reporte. Otra novedad es que ahora el cierre de reportes lo deciden las usuarias y no las autoridades: tendrán 72 horas para confirmar a la autoridad responsable si el reporte fue solucionado, si en ese lapso de tiempo no lo confirman, se cerrará automáticamente; en cambio, sí señalan que no ha quedado resuelto, el reporte permanecerá abierto. De esta forma siempre tendrán el control del reporte, lo que garantiza su resolución.

Reclasificación de datos

En noviembre de 2021 el Sistema Único de Atención Ciudadana (SUAC) se convirtió en el Sistema 0311 Locatel; este cambio implicó la existencia de un nuevo catálogo de motivos de solicitudes, más explícito y entendible.

Entre las novedades del nuevo sistema 0311 Locatel se encuentra un algoritmo de Inteligencia Artificial que clasifica y despacha en tiempo real los reportes para que sean atendidos mucho más rápido por las autoridades responsables. Este nuevo algoritmo también se ha encargado de reclasificar reportes previos al inicio de operación del Sistema 0311 Locatel por lo que es posible que algunos reportes hayan sufrido cambios o bien, que se sumen reportes que no contaban con una clasificación y que ahora sí la tienen.

División de la base de datos

A partir del 14 de septiembre de 2022, debido al tamaño de la base y para una mejor manipulación y visualización, la base se dividió anualmente.

Aviso

A partir de la actualización del 23 de noviembre de 2022, se renombró la columna "colonia_solicitud" por "0311_colonia_registro". Esta columna corresponde a la colonia registrada en el sistema 0311 Locatel. Asimismo se incorporó una nueva variable: "colonia_datos". Esta variable se generó a partir del cruce de la georreferenciación (latitud y longitud) y el catalogo de colonias utilizado para la herramienta de visualización.

Base completa (01/06/2019 - 20/11/2022) En caso de querer descargar la base completa de solicitudes al 0311, puedes dar clic en el siguiente enlace: Base completa *0311

'''

'''
csv_files = [
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/0311/locatel0311-2019.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/0311/locatel0311-2020.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/0311/locatel0311-2021.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/0311/locatel0311-2022.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/0311/locatel0311-2023.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/0311/locatel0311-2024.csv"
]

dataframes = []

for i, file in enumerate(csv_files):
    df = pd.read_csv(file)
    dataframes.append(df)
    print(df.columns.tolist())
    print(df.head())



def mostrar_valores_unicos(df, columna):
    if columna not in df.columns:
        print(f"La columna '{columna}' no existe en este dataset.")
        return
    print("Conteo por valor: ")
    print(df[columna].value_counts())

mostrar_valores_unicos(dataframes[0], "tema_solicitud")
mostrar_valores_unicos(dataframes[1], "tema_solicitud")
mostrar_valores_unicos(dataframes[2], "tema_solicitud")
mostrar_valores_unicos(dataframes[3], "tema_solicitud")
mostrar_valores_unicos(dataframes[4], "tema_solicitud")
mostrar_valores_unicos(dataframes[5], "tema_solicitud")
print()


columnas_requeridas = ['id_folio', 'fecha_solicitud', 'tema_solicitud', 'latitud', 'longitud']
temas_interes = [
    "MANTENIMIENTO DE COLADERA / ALCANTARILLA",
    "MANTENIMIENTO DRENAJE",
    "DESAZOLVE"
]

dfs = []

for file in csv_files:
    df = pd.read_csv(file, low_memory=False)

    # Asegurarse de que existan latitud y longitud
    for col in ['latitud', 'longitud']:
        if col not in df.columns:
            df[col] = pd.NA

    # Asegurarse de que existan todas las columnas requeridas
    for col in columnas_requeridas:
        if col not in df.columns:
            df[col] = pd.NA

    df = df[columnas_requeridas]

    # Limpiar filas con NaN o lat/lon = 0
    df = df.dropna()
    df = df[(df['latitud'] != 0) & (df['longitud'] != 0)]

    # Filtrar solo los temas de interés
    df = df[df['tema_solicitud'].isin(temas_interes)]

    dfs.append(df)

# Unir todos los DataFrames filtrados
df_final = pd.concat(dfs, ignore_index=True)

# Guardar a CSV
output_path = "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/0311/locatel_filtrado.csv"
df_final.to_csv(output_path, index=False, encoding='utf-8')

print(f"DataFrame final tiene {len(df_final)} filas")
print(f"Archivo guardado en: {output_path}")
'''
#################################################################################################

'''
https://datos.cdmx.gob.mx/dataset/rios-cdmx

https://datos.cdmx.gob.mx/dataset/f77aba04-efe7-4010-aac0-766b30973bf7/resource/41a19583-dd59-4087-8605-7309a07959c2/download/diccionario-de-datos-4.csv
https://datos.cdmx.gob.mx/dataset/f77aba04-efe7-4010-aac0-766b30973bf7/resource/be4de719-8696-4c87-8c31-d936b2d0366c/download/rios_cdmx-2.zip

******************* Ríos de CDMX *******************

Contiene la ubicación de los arroyos, canales y ríos (intermitente y perenne) en la
Ciudad de México.

'''
'''

import geopandas as gpd

# Carga el shapefile
shapefile_path = "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/rios/rios_cdmx-2/rios_cdmx/Ríos de CDMX.shp"  # ruta al archivo .shp
rios = gpd.read_file(shapefile_path)

# Muestra los primeros registros en forma de tabla
print(rios.head())

# Si quieres ver toda la tabla (puede ser grande)
print(rios)

'''

#################################################################################################

'''
https://datos.cdmx.gob.mx/dataset/llamadas-numero-de-atencion-a-emergencias-911

https://archivo.datos.cdmx.gob.mx/911/llamadas_911_2019_s1.csv
https://archivo.datos.cdmx.gob.mx/911/llamadas_911_2019_s2.csv
https://archivo.datos.cdmx.gob.mx/911/llamadas_911_2020_s1.csv
https://archivo.datos.cdmx.gob.mx/911/llamadas_911_2020_s2.csv
https://archivo.datos.cdmx.gob.mx/911/llamadas_911_2021_s1.csv
https://archivo.datos.cdmx.gob.mx/911/llamadas_911_2021_s2.csv
https://archivo.datos.cdmx.gob.mx/911/llamadas_911_2022_s1.csv

******************* Llamadas número de atención a emergencias 911 *******************

El número de emergencias 9-1-1 es un servicio público mediante el cual se brinda atención a la ciudadanía, en coordinación con diversas dependencias, en temas relacionados con delitos, emergencias, faltas cívicas, servicios públicos y urgencias médicas.

Desde abril de 2011 el CAEPCCM comenzó a administrar y operar los Servicios de Atención a
Llamadas de Emergencia del extinto 066, y a partir de enero de 2017, el Centro de Comando,
Control, Cómputo, Comunicaciones y Contacto Ciudadano comenzó la operación del teléfono de
emergencias unificado 9-1-1 en la Ciudad de México, en el que se atienden y canalizan de manera
inmediata los reportes de delitos y emergencias como incendios, robos, accidentes
automovilísticos, urgencias médicas, entre otros, las 24 horas, los 365 días del año.
'''

'''
csv_files = [
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/911/llamadas_911_2019_s1.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/911/llamadas_911_2019_s2.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/911/llamadas_911_2020_s1.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/911/llamadas_911_2020_s2.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/911/llamadas_911_2021_s1.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/911/llamadas_911_2021_s2.csv",
    "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/911/llamadas_911_2022_s1.csv"
]

dataframes = []

for i, file in enumerate(csv_files):
    #df = pd.read_csv(file)
    df = pd.read_csv(file, encoding='latin1', low_memory=False)
    dataframes.append(df)
    print(df.columns.tolist())
    print(df.head())


valores_unicos = set()

for df in dataframes:
    if 'incidente_c4' in df.columns:
        valores_unicos.update(df['incidente_c4'].dropna().unique())

valores_unicos = sorted(valores_unicos)
print(f"Total de valores únicos: {len(valores_unicos)}\n")
for valor in valores_unicos:
    print(valor)

columnas_requeridas = ['folio', 'incidente_c4', 'fecha_creacion', 'latitud', 'longitud']

incidentes_filtrados = ['Encharcamiento', 'Inundacion', 'Desborde canal rio presa']

dataframes = []

for file in csv_files:
    df = pd.read_csv(file, encoding='latin1', low_memory=False)
    df = df[[col for col in columnas_requeridas if col in df.columns]]
    df = df[df['incidente_c4'].isin(incidentes_filtrados)]
    dataframes.append(df)

df_final = pd.concat(dataframes, ignore_index=True)

print(df_final.head())

output_path = "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/911/llamadas_filtradas.csv"
df_final.to_csv(output_path, index=False, encoding='utf-8')

print(f"DataFrame final tiene {len(df_final)} filas")
print(f"Archivo guardado en: {output_path}")

'''

#################################################################################################

'''
https://datos.cdmx.gob.mx/dataset/formas-del-relieve-de-la-ciudad-de-mexico

https://datos.cdmx.gob.mx/dataset/74457e0a-e587-417b-a6de-a8438c7dae31/resource/47fc7e87-4b15-438b-be55-0a2294b98dc7/download/formas-del-relieve.zip

******************* Formas del relieve de la Ciudad de México *******************

Contiene las topoformas (cuerpo de agua, llanura, lomerío, meseta, sierra) de la Ciudad de México

'''

'''
import geopandas as gpd

gdf = gpd.read_file("/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/relieve/formas-del-relieve/formas del relieve.shp")
print(gdf.head())
print(gdf.info())
print(gdf['ENTIDAD'].unique())
print(gdf['NOMBRE'].unique())
print(gdf['DESCRIPCIO'].unique())
gdf.plot(figsize=(8,8))
'''

#################################################################################################

'''
https://datos.cdmx.gob.mx/dataset/atlas-de-riesgo-precipitacion

https://datos.cdmx.gob.mx/dataset/35438758-700a-466a-a4f5-05aaf2bbdd83/resource/3390d969-bc84-4b00-8cf9-5be10e39e101/download/atlas-de-riesgo-precipitacion.csv

******************* Atlas de riesgo - Precipitación *******************

Indicador de precipitación del módulo de peligros del Atlas de riegos de la Ciudad de México a nivel Ageb.

'''
'''
import pandas as pd

df = pd.read_csv("/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/atlas_riesgo_precipitaciones/atlas-de-riesgo-precipitacion.csv")

pd.set_option('display.max_columns', None)

print(df.head())

df_filtrado = df[[
    "geo_point_2d",
    "fenomeno",
    "taxonomia",
    "intensidad",
    "alcaldia",
    "area_m2",
    "period_ret",
    "intens_num",
    "int2"
]]

df_filtrado.to_csv("datos_limpios.csv", index=False)

print(df_filtrado.head())
print(f"DataFrame filtrado y guardado con {len(df_filtrado)} filas y {len(df_filtrado.columns)} columnas.")
'''

#################################################################################################

'''
https://datos.cdmx.gob.mx/dataset/convergencia-de-multiples-riesgos-en-la-ciudad-de-mexico

https://datos.cdmx.gob.mx/dataset/d5a4f648-33a9-4764-b82c-dc22978ecadf/resource/5ffa4b73-88e6-497f-a3a8-cea468130d35/download/sintesis_riesgos.zip

******************* Convergencia de múltiples riesgos en la Ciudad de México *******************

Identificación de zonas con presencia de múltiples riesgos: sismicidad; inundaciones; olas de calor; sequía; inestabilidad de laderas.

'''

'''
import geopandas as gpd

ruta_shp = "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/convergencia_riegos_CDMX/sintesis_riesgos/sintesis_riesgos.shp"
gdf = gpd.read_file(ruta_shp)

gdf_inundaciones = gdf[gdf['R_H1'] == 'Inundaciones']
gdf_inundaciones = gdf_inundaciones[['R_H1', 'SUMATORIA', 'geometry']]
gdf_inundaciones.to_file(ruta_shp)
print(gdf_inundaciones.head())
'''

#################################################################################################

'''
https://datos.cdmx.gob.mx/dataset/presencia-de-encharcamientos-del-ano-2000-al-2017-en-la-ciudad-de-mexico

https://datos.cdmx.gob.mx/dataset/d5a4f648-33a9-4764-b82c-dc22978ecadf/resource/5ffa4b73-88e6-497f-a3a8-cea468130d35/download/sintesis_riesgos.zip

******************* Convergencia de múltiples riesgos en la Ciudad de México *******************

Identificación de zonas con presencia de múltiples riesgos: sismicidad; inundaciones; olas de calor; sequía; inestabilidad de laderas.

'''

'''
import geopandas as gpd
ruta_shp = "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/presencia_de_encharcamientos/presencia-de-encharcamientos-del-ano-2000-al-2017-en-la-ciudad-de-mexico/Presencia de encharcamientos del año 2000 al 2017 en la Ciudad de México/encharcamientos_2000_2017_e.shp"

gdf = gpd.read_file(ruta_shp)
print(gdf.info())


gdf_filtrado = gdf[['CAUSA', 'VOLUMEN', 'geometry']]

causas_relevantes = [
    'INSUFICIENCIA DE ATARJEA Y COLECTOR',
    'COLADERA OBSTRUIDA',
    'COLADERA OBTRUIDA',
    'COLADERA OBSTRUDA',
    'ATARJEA OBSTRUIDA',
    'FALTA DE DRENAJE',
    'FALTA DRENAJE',
    'NO SE OPERÓ CARCAMO DE BOMBEO',
    'NO SE OPERO CARCAMO DE BOMBEO',
    'RUPTURA DE TUBO DE AGUA POTABLE',
    'HUNDIMIENTO DE LA CARPETA ASFALTICA',
    'HUNDIMIENTO DE CARPETA ASFALTICA',
    'HUNDIMIENTO DE LA CARPETA ASFÁLTICA',
    'HUNDIMIENTO DE PISO',
    'HUNDIMIENTODE PISO'
]

gdf_filtrado = gdf_filtrado[gdf_filtrado['CAUSA'].isin(causas_relevantes)]

gdf_filtrado.to_file(ruta_shp)
pd.set_option('display.max_columns', None)
print(gdf_filtrado.head())
print(gdf_filtrado.info())

# valores_unicos_causa = pd.unique(gdf_filtrado['CAUSA'].dropna())
# print("Valores únicos de CAUSA:", valores_unicos_causa)
'''

#################################################################################################

'''
https://datos.cdmx.gob.mx/dataset/sitios-recurrentes-de-encharcamiento-en-ciudad-de-mexico

https://datos.cdmx.gob.mx/dataset/75b84746-d9fe-4343-a733-d3e1da77344a/resource/eadeb623-52e9-4594-82ae-30ba70c7dfe7/download/sitios-recurrentes-de-encharcamiento-en-ciudad-de-mexico.zip

******************* Sitios recurrentes de encharcamiento en Ciudad de México *******************

Capa de información geoespacial con los sitios recurrentes de encharcamientos en Ciudad de México

'''

'''
import geopandas as gpd
ruta_shp = "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/sitios_recurrentes_de_encharcamiento/sitios-recurrentes-de-encharcamiento-en-ciudad-de-mexico/Sitios recurrentes de encharcamiento en Ciudad de México/sitios_mayor_recurrencia_encharcamientos.shp"

gdf = gpd.read_file(ruta_shp)
pd.set_option('display.max_columns', None)
print(gdf.info())
print(gdf.head())
'''

#################################################################################################

'''
https://datos.cdmx.gob.mx/dataset/epma-1-niveles-de-inundacion-y-carencia-de-cobertura-de-areas-verdes

https://datos.cdmx.gob.mx/dataset/8571952d-315a-4f5b-a11c-6f8a4a9c5029/resource/8e9c0bd8-155e-4210-96c4-60ddb23339d3/download/epma_1.zip

******************* Niveles de inundación y carencia de cobertura de áreas verdes *******************

Capa de información geoespacial con los Niveles de inundación y carencia de cobertura de áreas verdes(m2/hab), en Ciudad de México.

'''

'''
import geopandas as gpd
ruta_shp = "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/niveles_inundación_cobertura_áreas_verdes/epma_1/epma_1.shp"

gdf = gpd.read_file(ruta_shp)
pd.set_option('display.max_columns', None)
print(gdf.info())
print(gdf.head())


# Valores únicos
valores_unicos_C_INUNDA = pd.unique(gdf['C_INUNDA'].dropna())
valores_unicos_INT_NUM_IN = pd.unique(gdf['INT_NUM_IN'].dropna())

print("Valores únicos de C_INUNDA:", valores_unicos_C_INUNDA)
print("Valores únicos de INT_NUM_IN:", valores_unicos_INT_NUM_IN)

gdf_filtrado = gdf[['INUNDACION', 'C_INUNDA', 'INT_NUM_IN', 'geometry']]

print(gdf_filtrado.head())


gdf_filtrado.to_file(ruta_shp)
pd.set_option('display.max_columns', None)
print(gdf_filtrado.head())
print(gdf_filtrado.info())
'''


#################################################################################################

'''
https://datos.cdmx.gob.mx/dataset/red-hidrografica-superficial-lidar

https://datos.cdmx.gob.mx/dataset/42c99e5c-ecfc-4f6f-adc5-9d5a6bc4b583/resource/ee42ace8-ce63-47de-944b-9d45830024e7/download/red_hidrografica-2.zip

******************* Red hidrográfica superficial (Escorrentías por Orden Strahler) *******************

Contiene la red hidrográfica superficial de escorrentías por orden Strahler (3 - 10) a través de la técnica LIDAR (Light Detection and Ranging)en la Ciudad de México


GRID_CODE -> Valores bajos (1, 2) → arroyos pequeños o ramificaciones secundarias.
Valores altos (hasta 10) → ríos principales o escurrimientos con mayor caudal potencial.
Básicamente, indica la jerarquía de los flujos de agua en la red superficial. Esto te ayuda a saber qué partes de la red son más propensas a causar inundaciones si se saturan.

'''

'''
import geopandas as gpd
ruta_shp = "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/red_hidrográfica_superficial/red_hidrografica-2/red_hidrografica/Red hidrográfica superficial LIDAR.shp"

gdf = gpd.read_file(ruta_shp)
pd.set_option('display.max_columns', None)
print(gdf.info())
print(gdf.head())


print(pd.unique(gdf['GRID_CODE'].dropna()))
'''



#################################################################################################

import os
import pandas as pd
import geopandas as gpd

# Carpeta principal
base_path = "/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/DatosEntrenamiento/DATOS LIMPIOS"

# Recorrer todas las subcarpetas
for root, dirs, files in os.walk(base_path):
    # Ignorar carpetas __MACOSX
    if "__MACOSX" in root:
        continue

    for file in files:
        # Ignorar archivos basura de macOS
        if file.startswith("._"):
            continue

        file_path = os.path.join(root, file)
        
        # CSV (opcional)
        if file.endswith(".csv"):
            try:
                df = pd.read_csv(file_path)
                print("Columnas:", df.columns.tolist())
                print("Primeras filas:")
                print(df.head(3))
            except Exception as e:
                print(f"No se pudo leer {file_path}: {e}")

        # SHP
        elif file.endswith(".shp"):
            try:
                gdf = gpd.read_file(file_path)
                print("Columnas:", gdf.columns.tolist())
                print("Primeras filas:")
                print(gdf.head(3))
            except Exception as e:
                print(f"No se pudo leer {file_path}: {e}")
