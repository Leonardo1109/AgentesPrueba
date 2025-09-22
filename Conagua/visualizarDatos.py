import geopandas as gpd

datos = gpd.read_file('InfraConagua/Infraestruc_agua_potable.shp')

print(datos.head())

print(datos)

print(datos.info())


print(datos.tail(10))


