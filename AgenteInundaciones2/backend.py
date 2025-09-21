from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium
from typing import Dict, Any
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="API de Riesgo de Inundaciones CDMX")

# Configurar CORS para permitir requests del frontend (PRIMERO)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/frontend")
async def serve_frontend():
    return FileResponse("templates/index.html")

# Cargar los datos | Cambiar a la ruta donde ustedes guarden los datos de las inundaciones
gdf = gpd.read_file('/home/leonardo/Escritorio/atlas_de_riesgo_inundaciones/atlas_de_riesgo_inundaciones.shp')
gdf_projected = gdf.to_crs('EPSG:6369')

class CoordenadasRequest(BaseModel):
    lat: float
    lon: float

class MapaResponse(BaseModel):
    mapa_html: str
    coordenadas: Dict[str, float]

'''
def consultar_riesgo_por_coordenadas(lat: float, lon: float) -> Dict[str, Any]:
    """Consulta el riesgo de inundación para coordenadas específicas"""
    try:
        # Crear punto y convertir a CRS proyectado
        punto = Point(float(lon), float(lat))
        punto_projected = gpd.GeoSeries([punto], crs='EPSG:4326').to_crs('EPSG:6369').iloc[0]
        
        # Encontrar el polígono más cercano
        gdf_projected['distancia'] = gdf_projected.geometry.distance(punto_projected)
        riesgo_encontrado = gdf_projected.loc[gdf_projected['distancia'].idxmin()]
        riesgo_original = gdf.loc[riesgo_encontrado.name]
        
        # CONVERSIÓN EXPLÍCITA DE TODOS LOS VALORES NUMPY
        distancia_km = float(riesgo_encontrado['distancia'] / 1000)
        dentro_zona = bool(distancia_km < 0.1)
        nivel = int(riesgo_original['int2'])
        area_m2 = float(riesgo_original['area_m2'])
        
        niveles = {1: "Muy Bajo", 2: "Bajo", 3: "Medio", 4: "Alto", 5: "Muy Alto"}
        
        return {
            "coordenadas": {"lat": float(lat), "lon": float(lon)},
            "alcaldia": str(riesgo_original['alcaldi']),
            "nivel_riesgo": nivel,
            "nivel_riesgo_texto": str(niveles.get(nivel, "Desconocido")),
            "dentro_zona": dentro_zona,
            "distancia_km": round(distancia_km, 2),
            "area_m2": area_m2,
            "descripcion": str(riesgo_original.get('descrpc', '')),
            "interpretacion": str(get_interpretacion_riesgo(nivel))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando coordenadas: {str(e)}")
'''

def consultar_riesgo_por_coordenadas(lat: float, lon: float) -> Dict[str, Any]:
    """Consulta el riesgo de inundación para coordenadas específicas"""
    try:
        # Validar que las coordenadas estén dentro de los límites aproximados de la CDMX
        # Límites aproximados de la CDMX: 
        # Lat: 19.0 a 19.6, Lon: -99.4 a -98.9
        if not (19.0 <= lat <= 19.6) or not (-99.4 <= lon <= -98.9):
            return {
                "coordenadas": {"lat": float(lat), "lon": float(lon)},
                "alcaldia": "Fuera de la CDMX",
                "nivel_riesgo": 0,
                "nivel_riesgo_texto": "No aplica",
                "dentro_zona": False,
                "distancia_km": 0.0,
                "area_m2": 0,
                "descripcion": "Las coordenadas están fuera del área de la Ciudad de México",
                "interpretacion": "Esta ubicación está fuera del área de estudio. El sistema solo contiene datos para la CDMX.",
                "fuera_de_cdmx": True
            }
            
        
        # Crear punto y convertir a CRS proyectado
        punto = Point(float(lon), float(lat))
        punto_projected = gpd.GeoSeries([punto], crs='EPSG:4326').to_crs('EPSG:6369').iloc[0]
        
        # Encontrar el polígono más cercano
        gdf_projected['distancia'] = gdf_projected.geometry.distance(punto_projected)
        riesgo_encontrado = gdf_projected.loc[gdf_projected['distancia'].idxmin()]
        riesgo_original = gdf.loc[riesgo_encontrado.name]
        
        # CONVERSIÓN EXPLÍCITA DE TODOS LOS VALORES NUMPY
        distancia_km = float(riesgo_encontrado['distancia'] / 1000)
        dentro_zona = bool(distancia_km < 0.1)
        nivel = int(riesgo_original['int2'])
        area_m2 = float(riesgo_original['area_m2'])
        
        niveles = {1: "Muy Bajo", 2: "Bajo", 3: "Medio", 4: "Alto", 5: "Muy Alto"}
        
        # Si está muy lejos (más de 50 km), considerar que está fuera de la CDMX | Ajustar valores
        if distancia_km > 50.0:
            return {
                "coordenadas": {"lat": float(lat), "lon": float(lon)},
                "alcaldia": "Fuera de la CDMX",
                "nivel_riesgo": 0,
                "nivel_riesgo_texto": "No aplica",
                "dentro_zona": False,
                "distancia_km": round(distancia_km, 2),
                "area_m2": 0,
                "descripcion": "Ubicación significativamente fuera del área metropolitana",
                "interpretacion": "Esta ubicación está muy lejos de la CDMX. El sistema solo contiene datos para el área metropolitana.",
                "fuera_de_cdmx": True
            }
        
        return {
            "coordenadas": {"lat": float(lat), "lon": float(lon)},
            "alcaldia": str(riesgo_original['alcaldi']),
            "nivel_riesgo": nivel,
            "nivel_riesgo_texto": str(niveles.get(nivel, "Desconocido")),
            "dentro_zona": dentro_zona,
            "distancia_km": round(distancia_km, 2),
            "area_m2": area_m2,
            "descripcion": str(riesgo_original.get('descrpc', '')),
            "interpretacion": str(get_interpretacion_riesgo(nivel)),
            "fuera_de_cdmx": False
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando coordenadas: {str(e)}")

# Funcion para visualizar los datos, eliminar despues de crear al agente o agregar al agente
def get_interpretacion_riesgo(nivel: int) -> str:
    """Obtiene la interpretación del nivel de riesgo"""
    interpretaciones = {
        1: "Riesgo muy bajo. Inundaciones poco probables incluso con lluvias intensas.",
        2: "Riesgo bajo. Inundaciones ocasionales en temporada de lluvias.",
        3: "Riesgo medio. Puede haber inundaciones con lluvias fuertes.",
        4: "Riesgo alto. Inundaciones frecuentes durante la temporada de lluvias.",
        5: "Riesgo muy alto. Zona con historial de inundaciones severas."
    }
    return interpretaciones.get(nivel, "Nivel de riesgo desconocido.")

def crear_mapa_interactivo(lat: float = 19.4326, lon: float = -99.1332) -> str:
    """Crea un mapa interactivo con las coordenadas seleccionadas"""
    m = folium.Map(location=[lat, lon], zoom_start=12)
    
    # Añadir capa de polígonos de riesgo
    for _, row in gdf.iterrows():
        color = 'red' if row['int2'] >= 4 else 'orange' if row['int2'] == 3 else 'green'
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x, color=color: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.3,
            },
            tooltip=f"Riesgo: {row['int2']} - {row['alcaldi']}"
        ).add_to(m)
    
    # Marcador inicial (Centro de CDMX)
    folium.Marker(
        [lat, lon],
        popup="Centro de CDMX",
        tooltip="Haz clic en el mapa para seleccionar una ubicación",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Añadir control de clic para coordenadas
    m.add_child(folium.LatLngPopup())
    
    return m._repr_html_()

@app.get("/")
async def root():
    return {"message": "API de Riesgo de Inundaciones CDMX"}

@app.get("/mapa", response_model=MapaResponse)
async def obtener_mapa():
    """Endpoint para obtener el mapa interactivo inicial"""
    mapa_html = crear_mapa_interactivo()
    return {
        "mapa_html": mapa_html,
        "coordenadas": {"lat": 19.4326, "lon": -99.1332}
    }

@app.post("/consultar-riesgo")
async def consultar_riesgo(coordenadas: CoordenadasRequest):
    """Endpoint para consultar el riesgo por coordenadas"""
    resultado = consultar_riesgo_por_coordenadas(coordenadas.lat, coordenadas.lon)
    return resultado

@app.get("/estadisticas")
async def obtener_estadisticas():
    """Endpoint para obtener estadísticas generales"""
    stats = gdf['int2'].value_counts().sort_index()
    
    # Convertir numpy types a Python native types
    distribucion = {}
    for key, value in stats.items():
        distribucion[int(key)] = int(value)  # Convertir numpy.int64 a int
    
    return {
        "total_poligonos": int(len(gdf)),
        "alcaldias": int(gdf['alcaldi'].nunique()),
        "distribucion_riesgo": distribucion
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)