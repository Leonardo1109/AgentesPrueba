import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import pandas as pd
from shapely.geometry import Point

# Cargar los datos
gdf = gpd.read_file('/home/leonardo/Escritorio/atlas_de_riesgo_inundaciones/atlas_de_riesgo_inundaciones.shp')

# Convertir a un CRS proyectado para cálculos de distancia correctos
gdf_projected = gdf.to_crs('EPSG:6369')  # CRS proyectado para México

def consultar_riesgo_por_coordenadas(lat: float, lon: float) -> str:
    """
    Consulta el riesgo de inundación para coordenadas específicas en la CDMX
    """
    try:
        print(f"📍 Consultando coordenadas: {lat}, {lon}")
        
        # Crear punto y convertir a CRS proyectado
        punto = Point(lon, lat)
        punto_projected = gpd.GeoSeries([punto], crs='EPSG:4326').to_crs('EPSG:6369').iloc[0]
        
        # Encontrar el polígono más cercano en el CRS proyectado
        gdf_projected['distancia'] = gdf_projected.geometry.distance(punto_projected)
        riesgo_encontrado = gdf_projected.loc[gdf_projected['distancia'].idxmin()]
        
        # Obtener la fila correspondiente en el dataframe original
        riesgo_original = gdf.loc[riesgo_encontrado.name]
        
        distancia_km = riesgo_encontrado['distancia'] / 1000  # Convertir a km
        dentro_zona = distancia_km < 0.1  # Considerar "dentro" si está a menos de 100m
        
        # Preparar respuesta
        nivel = riesgo_original['int2']
        niveles = {1: "Muy Bajo", 2: "Bajo", 3: "Medio", 4: "Alto", 5: "Muy Alto"}
        
        response = f"📋 **Riesgo de inundación para coordenadas:**\n"
        response += f"🌐 **Latitud:** {lat:.6f}\n"
        response += f"🌐 **Longitud:** {lon:.6f}\n"
        response += f"🏙️ **Alcaldía:** {riesgo_original['alcaldi']}\n\n"
        
        if dentro_zona:
            response += f"✅ **Dentro de zona de riesgo**\n"
            response += f"⚠️ **Nivel de riesgo:** {nivel} - {niveles.get(nivel, 'Desconocido')}\n"
        else:
            response += f"ℹ️ **Fuera de zonas de riesgo** (a {distancia_km:.2f} km de la zona más cercana)\n"
            response += f"⚠️ **Nivel de riesgo más cercano:** {nivel} - {niveles.get(nivel, 'Desconocido')}\n"
        
        response += f"📏 **Área de la zona:** {riesgo_original['area_m2']:,.0f} m²\n"
        
        # Información adicional si está disponible
        if 'descrpc' in riesgo_original and pd.notna(riesgo_original['descrpc']):
            response += f"📝 **Descripción:** {riesgo_original['descrpc']}\n"
        
        # Crear mapa interactivo
        m = folium.Map(location=[lat, lon], zoom_start=16)
        
        # Marcador de la ubicación
        folium.Marker(
            [lat, lon],
            popup=f"""Coordenadas consultadas:
Lat: {lat:.6f}
Lon: {lon:.6f}
Nivel riesgo: {nivel} - {niveles.get(nivel, 'Desconocido')}""",
            tooltip="Ubicación consultada",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
        
        # Añadir el polígono de riesgo más cercano
        folium.GeoJson(
            riesgo_original.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': 'red' if nivel >= 4 else 'orange' if nivel == 3 else 'yellow',
                'color': 'black',
                'weight': 2,
                'fillOpacity': 0.5,
            },
            tooltip=f"Riesgo nivel {nivel} - {niveles.get(nivel, 'Desconocido')}"
        ).add_to(m)
        
        # Nombre del archivo descriptivo
        mapa_nombre = f"mapa_riesgo_{lat:.4f}_{lon:.4f}"
        mapa_path = f"{mapa_nombre}.html"
        m.save(mapa_path)
        
        response += f"\n🗺️ **Mapa generado:** {mapa_path}"
        
        # Interpretación del riesgo
        response += f"\n\n🔍 **Interpretación del riesgo nivel {nivel}:**\n"
        if nivel == 1:
            response += "Riesgo muy bajo. Inundaciones poco probables incluso con lluvias intensas."
        elif nivel == 2:
            response += "Riesgo bajo. Inundaciones ocasionales en temporada de lluvias."
        elif nivel == 3:
            response += "Riesgo medio. Puede haber inundaciones con lluvias fuertes."
        elif nivel == 4:
            response += "Riesgo alto. Inundaciones frecuentes durante la temporada de lluvias."
        else:
            response += "Riesgo muy alto. Zona con historial de inundaciones severas."
        
        return response
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def consultar_multiples_coordenadas(coordenadas_lista):
    """
    Consulta el riesgo para múltiples coordenadas
    """
    resultados = []
    for i, (lat, lon) in enumerate(coordenadas_lista, 1):
        print(f"\n🔍 Consultando coordenada {i}: {lat}, {lon}")
        resultado = consultar_riesgo_por_coordenadas(lat, lon)
        resultados.append(resultado)
    
    return resultados

# Ejecutar para probar con tus coordenadas
if __name__ == "__main__":
    print("=" * 80)
    print("🔍 CONSULTA DE RIESGO DE INUNDACIÓN POR COORDENADAS")
    print("=" * 80)
    
    # Tus coordenadas específicas
    coordenadas = [
        (19.437801, -99.149101)

    ]
    
    resultados = consultar_multiples_coordenadas(coordenadas)
    
    for i, resultado in enumerate(resultados, 1):
        print(f"\n{'='*50}")
        print(f"RESULTADO {i}:")
        print(f"{'='*50}")
        print(resultado)
    
    # Consulta individual específica
    print(f"\n{'='*80}")
    print("📍 CONSULTA ESPECÍFICA - TUS COORDENADAS:")
    print(f"{'='*80}")
    resultado_especifico = consultar_riesgo_por_coordenadas(19.438157, -99.107078)
    print(resultado_especifico)
    
'''
import geopandas as gpd
import matplotlib.pyplot as plt
from langchain.tools import tool
from geopy.geocoders import Nominatim
import folium
import pandas as pd
from shapely.geometry import Point

# Cargar los datos
gdf = gpd.read_file('/home/leonardo/Escritorio/atlas_de_riesgo_inundaciones/atlas_de_riesgo_inundaciones.shp')

# Convertir a un CRS proyectado para cálculos de distancia correctos
gdf_projected = gdf.to_crs('EPSG:6369')  # CRS proyectado para México

# Inicializar el geocoder (gratuito)
geolocator = Nominatim(user_agent="inundaciones_cdmx")

def consultar_riesgo_por_direccion_simple(direccion: str, colonia: str = None, delegacion: str = None) -> str:
    """
    Versión simple sin decorador @tool para pruebas
    Ahora acepta dirección, colonia y delegación por separado para mayor precisión
    """
    try:
        # Construir la query de búsqueda
        query_parts = []
        if direccion:
            query_parts.append(direccion)
        if colonia:
            query_parts.append(colonia)
        if delegacion:
            query_parts.append(delegacion)
        query_parts.append("Ciudad de México")
        
        query = ", ".join(query_parts)
        print(f"📍 Buscando coordenadas para: {query}")
        
        location = geolocator.geocode(query)
        
        if not location:
            return f"No se pudo encontrar la ubicación: {query}"
        
        lat, lon = location.latitude, location.longitude
        print(f"✅ Coordenadas encontradas: {lat}, {lon}")
        print(f"✅ Dirección encontrada: {location.address}")
        
        # Crear punto y convertir a CRS proyectado
        punto = Point(lon, lat)
        punto_projected = gpd.GeoSeries([punto], crs='EPSG:4326').to_crs('EPSG:6369').iloc[0]
        
        # Encontrar el polígono más cercano en el CRS proyectado
        gdf_projected['distancia'] = gdf_projected.geometry.distance(punto_projected)
        riesgo_encontrado = gdf_projected.loc[gdf_projected['distancia'].idxmin()]
        
        # Obtener la fila correspondiente en el dataframe original
        riesgo_original = gdf.loc[riesgo_encontrado.name]
        
        distancia_km = riesgo_encontrado['distancia'] / 1000  # Convertir a km
        dentro_zona = distancia_km < 0.1  # Considerar "dentro" si está a menos de 100m
        
        # Preparar respuesta
        nivel = riesgo_original['int2']
        niveles = {1: "Muy Bajo", 2: "Bajo", 3: "Medio", 4: "Alto", 5: "Muy Alto"}
        
        response = f"📋 **Riesgo de inundación para:**\n"
        response += f"📍 **Ubicación:** {direccion}\n"
        response += f"🏘️ **Colonia:** {colonia}\n"
        response += f"🏙️ **Delegación:** {delegacion}\n"
        response += f"🌐 **Coordenadas:** {lat:.6f}, {lon:.6f}\n"
        response += f"🗺️ **Alcaldía en datos:** {riesgo_original['alcaldi']}\n\n"
        
        if dentro_zona:
            response += f"⚠️ **Nivel de riesgo:** {nivel} - {niveles.get(nivel, 'Desconocido')} (dentro de la zona de riesgo)\n"
        else:
            response += f"⚠️ **Nivel de riesgo más cercano:** {nivel} - {niveles.get(nivel, 'Desconocido')} (a {distancia_km:.2f} km)\n"
        
        response += f"📏 **Área de la zona:** {riesgo_original['area_m2']:,.0f} m²\n"
        
        # Información adicional si está disponible
        if 'descrpc' in riesgo_original and pd.notna(riesgo_original['descrpc']):
            response += f"📝 **Descripción:** {riesgo_original['descrpc']}\n"
        
        response += f"\n📫 **Dirección exacta encontrada:** {location.address}\n"
        
        # Crear mapa interactivo
        m = folium.Map(location=[lat, lon], zoom_start=16)
        
        # Marcador de la ubicación
        folium.Marker(
            [lat, lon],
            popup=f"""Ubicación consultada:
{direccion}
Colonia: {colonia}
Delegación: {delegacion}""",
            tooltip="Tu ubicación",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
        
        # Añadir el polígono de riesgo más cercano
        folium.GeoJson(
            riesgo_original.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': 'red' if nivel >= 4 else 'orange' if nivel == 3 else 'yellow',
                'color': 'black',
                'weight': 2,
                'fillOpacity': 0.5,
            },
            tooltip=f"Riesgo nivel {nivel} - {niveles.get(nivel, 'Desconocido')}"
        ).add_to(m)
        
        # Nombre del archivo descriptivo
        mapa_nombre = f"mapa_{colonia.replace(' ', '_')[:15]}_{delegacion.replace(' ', '_')[:10]}"
        mapa_path = f"{mapa_nombre}.html"
        m.save(mapa_path)
        
        response += f"\n🗺️ **Mapa generado:** {mapa_path}"
        
        # Interpretación del riesgo
        response += f"\n\n🔍 **Interpretación del riesgo nivel {nivel}:**\n"
        if nivel == 1:
            response += "Riesgo muy bajo. Inundaciones poco probables incluso con lluvias intensas."
        elif nivel == 2:
            response += "Riesgo bajo. Inundaciones ocasionales en temporada de lluvias."
        elif nivel == 3:
            response += "Riesgo medio. Puede haber inundaciones con lluvias fuertes."
        elif nivel == 4:
            response += "Riesgo alto. Inundaciones frecuentes durante la temporada de lluvias."
        else:
            response += "Riesgo muy alto. Zona con historial de inundaciones severas."
        
        return response
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Ejecutar para probar con tu ubicación exacta
if __name__ == "__main__":
    print("=" * 80)
    print("🔍 CONSULTA DE RIESGO DE INUNDACIÓN - UBICACIÓN ESPECÍFICA")
    print("=" * 80)
    
    # Tu ubicación exacta
    resultado = consultar_riesgo_por_direccion_simple(
        direccion="Calz. del Peñón",
        colonia="Azteca", 
        delegacion="Venustiano Carranza"
    )
    
    print(resultado)
    
    print("\n" + "=" * 80)
    print("💡 Para otras consultas, usa el formato:")
    print("consultar_riesgo_por_direccion_simple(direccion, colonia, delegacion)")
'''








'''
import geopandas as gpd
import matplotlib.pyplot as plt
from langchain.tools import tool
from geopy.geocoders import Nominatim
import folium
import pandas as pd
from shapely.geometry import Point

# Cargar los datos
gdf = gpd.read_file('/home/leonardo/Escritorio/atlas_de_riesgo_inundaciones/atlas_de_riesgo_inundaciones.shp')

# Convertir a un CRS proyectado para cálculos de distancia correctos
gdf_projected = gdf.to_crs('EPSG:6369')  # CRS proyectado para México

# Inicializar el geocoder (gratuito)
geolocator = Nominatim(user_agent="inundaciones_cdmx")

def consultar_riesgo_por_direccion_simple(direccion: str) -> str:
    """
    Versión simple sin decorador @tool para pruebas
    """
    try:
        print(f"📍 Buscando coordenadas para: {direccion}")
        location = geolocator.geocode(direccion + ", Ciudad de México")
        
        if not location:
            return f"No se pudo encontrar la dirección: {direccion}"
        
        lat, lon = location.latitude, location.longitude
        print(f"✅ Coordenadas encontradas: {lat}, {lon}")
        
        # Crear punto y convertir a CRS proyectado
        punto = Point(lon, lat)
        punto_projected = gpd.GeoSeries([punto], crs='EPSG:4326').to_crs('EPSG:6369').iloc[0]
        
        # Encontrar el polígono más cercano en el CRS proyectado
        gdf_projected['distancia'] = gdf_projected.geometry.distance(punto_projected)
        riesgo_encontrado = gdf_projected.loc[gdf_projected['distancia'].idxmin()]
        
        # Obtener la fila correspondiente en el dataframe original
        riesgo_original = gdf.loc[riesgo_encontrado.name]
        
        distancia_km = riesgo_encontrado['distancia'] / 1000  # Convertir a km
        dentro_zona = distancia_km < 0.1  # Considerar "dentro" si está a menos de 100m
        
        # Preparar respuesta
        nivel = riesgo_original['int2']
        niveles = {1: "Muy Bajo", 2: "Bajo", 3: "Medio", 4: "Alto", 5: "Muy Alto"}
        
        response = f"📋 **Riesgo de inundación para:** {direccion}\n\n"
        response += f"📍 **Coordenadas:** {lat:.6f}, {lon:.6f}\n"
        response += f"🏙️ **Alcaldía:** {riesgo_original['alcaldi']}\n"
        
        if dentro_zona:
            response += f"⚠️ **Nivel de riesgo:** {nivel} - {niveles.get(nivel, 'Desconocido')} (dentro de la zona de riesgo)\n"
        else:
            response += f"⚠️ **Nivel de riesgo más cercano:** {nivel} - {niveles.get(nivel, 'Desconocido')} (a {distancia_km:.2f} km)\n"
        
        response += f"📏 **Área de la zona:** {riesgo_original['area_m2']:,.0f} m²\n"
        
        # Crear mapa interactivo simplificado
        m = folium.Map(location=[lat, lon], zoom_start=15)
        
        # Marcador de la ubicación
        folium.Marker(
            [lat, lon],
            popup=f"Ubicación consultada: {direccion}",
            tooltip="Tu ubicación",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
        
        # Añadir el polígono de riesgo más cercano
        folium.GeoJson(
            riesgo_original.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': 'red' if nivel >= 4 else 'orange' if nivel == 3 else 'yellow',
                'color': 'black',
                'weight': 2,
                'fillOpacity': 0.5,
            },
            tooltip=f"Riesgo nivel {nivel} - {niveles.get(nivel, 'Desconocido')}"
        ).add_to(m)
        
        mapa_path = f"mapa_riesgo_{direccion.replace(' ', '_').replace(',', '')[:15]}.html"
        m.save(mapa_path)
        
        response += f"\n🗺️ **Mapa generado:** {mapa_path}"
        return response
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Función de prueba sin decorador
def mostrar_ejemplos_simple():
    """Versión simple sin decorador @tool"""
    ejemplos = [
        "Avenida Juárez 12, Cuauhtémoc",
        "Calle Madero, Centro Histórico",
        "Metro Candelaria, Venustiano Carranza",
        "Plaza de las Tres Culturas, Tlatelolco",
        "Estadio Azteca, Tlalpan"
    ]
    
    response = "Ejemplos de direcciones que puedes consultar:\n\n"
    for ejemplo in ejemplos:
        response += f"• '{ejemplo}'\n"
    
    response += "\n💡 **Tip:** Entre más específica la dirección, mejor será el resultado."
    return response

# Ejecutar para probar
if __name__ == "__main__":
    print("=" * 60)
    resultado = consultar_riesgo_por_direccion_simple("Calle Progreso, Venustiano Carranza")
    print(resultado)
    
    print("\n" + "=" * 60)
    print(mostrar_ejemplos_simple())
'''









"""
import geopandas as gpd
import matplotlib.pyplot as plt
import folium

# 1. Cargar el shapefile
# Asegúrate de que la ruta apunte al directorio donde están todos los archivos (.shp, .shx, .dbf, .prj)
gdf = gpd.read_file('/home/leonardo/Escritorio/atlas_de_riesgo_inundaciones/atlas_de_riesgo_inundaciones.shp')

# 2. Explorar los datos rápidamente
print(gdf.head()) # Ver las primeras filas de la tabla de atributos
print(gdf.columns) # Ver los nombres de las columnas disponibles (¡ crucial para saber qué datos tienes!)
print(gdf.crs) # Ver el sistema de coordenadas de referencia (del archivo .prj)

# 3. Ver los valores únicos en las columnas potenciales para entender los datos
print("\nValores únicos en int2:", sorted(gdf['int2'].unique()))
print("Valores únicos en intens_n:", sorted(gdf['intens_n'].unique()))
print("Valores únicos en taxonom:", gdf['taxonom'].unique()[:10])  # primeros 10

# 4. Visualización con la columna correcta - prueba con 'int2' primero
plt.figure(figsize=(12, 10))
gdf.plot(column='int2',  # Columna que parece indicar nivel de riesgo
         cmap='Reds', 
         legend=True,
         edgecolor='black',
         linewidth=0.3)
plt.title('Mapa de Riesgo de Inundaciones CDMX - por nivel int2')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.show()

# 5. También prueba con otras columnas potenciales
if 'intens_n' in gdf.columns:
    plt.figure(figsize=(12, 10))
    gdf.plot(column='intens_n',
             cmap='YlOrRd',
             legend=True,
             edgecolor='black',
             linewidth=0.3)
    plt.title('Mapa de Riesgo de Inundaciones CDMX - por intens_n')
    plt.show()

# 6. Mapa interactivo con Folium
x_center = gdf.geometry.centroid.x.mean()
y_center = gdf.geometry.centroid.y.mean()

m = folium.Map(location=[y_center, x_center], zoom_start=11)

# Función para determinar color basado en el nivel de riesgo
def get_color(feature):
    # Asumiendo que 'int2' es el nivel de riesgo (1-5, donde 5 es más alto)
    risk_level = feature['properties'].get('int2', 1)
    if risk_level == 5:
        return 'red'
    elif risk_level == 4:
        return 'orange'
    elif risk_level == 3:
        return 'yellow'
    elif risk_level == 2:
        return 'green'
    else:
        return 'blue'

# Añadir los datos al mapa
folium.GeoJson(gdf,
               style_function=lambda feature: {
                   'fillColor': get_color(feature),
                   'color': 'black',
                   'weight': 1,
                   'fillOpacity': 0.6,
               },
               tooltip=folium.GeoJsonTooltip(fields=['alcaldi', 'int2', 'intens_n', 'taxonom'],
                                            aliases=['Alcaldía:', 'Nivel riesgo:', 'Intensidad:', 'Tipo:']),
               popup=folium.GeoJsonPopup(fields=['alcaldi', 'int2', 'intens_n', 'descrpc', 'area_m2'],
                                        aliases=['Alcaldía:', 'Nivel:', 'Intensidad:', 'Descripción:', 'Área:'])
              ).add_to(m)

# Guardar el mapa
m.save('mapa_riesgo_inundacion_cdmx.html')
print("Mapa interactivo guardado como 'mapa_riesgo_inundacion_cdmx.html'")

# 7. Mostrar información estadística básica
print("\n=== ESTADÍSTICAS DEL DATASET ===")
print(f"Total de polígonos de riesgo: {len(gdf)}")
print(f"Alcaldías representadas: {gdf['alcaldi'].nunique()}")
print(f"Distribución de niveles de riesgo (int2):")
print(gdf['int2'].value_counts().sort_index())

"""