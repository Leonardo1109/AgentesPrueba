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
import requests
import os
from datetime import datetime, timedelta

app = FastAPI(title="API de Riesgo de Inundaciones CDMX")

# Configurar CORS para permitir requests del frontend (PRIMERO)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Ingresen su api kei para tomorrow.io, se registran y la agregan
TOMORROW_IO_API_KEY = "cCtWlhpkwGta5JJdG0qgbnKGkl3PIBLt"

@app.get("/frontend")
async def serve_frontend():
    return FileResponse("templates/index.html")

# Cargar los datos | Cambiar a la ruta donde ustedes guarden los datos de las inundaciones
gdf = gpd.read_file('/home/leonardo/Escritorio/Universidad/2026-I/Inteligencia Artificial/AgentesPrueba/AgenteInundaciones3/atlas_de_riesgo_inundaciones/atlas_de_riesgo_inundaciones.shp')
gdf_projected = gdf.to_crs('EPSG:6369')

class CoordenadasRequest(BaseModel):
    lat: float
    lon: float

class MapaResponse(BaseModel):
    mapa_html: str
    coordenadas: Dict[str, float]

# Funcion para el clima usando Tomorrow.io
def obtener_pronostico_lluvia(lat: float, lon: float) -> Dict[str, Any]:
    """Obtiene el pronóstico de lluvia para las coordenadas dadas usando Tomorrow.io"""
    try:
        print(f"🔍 Intentando conectar a Tomorrow.io API con key: {TOMORROW_IO_API_KEY[:10]}...")
        
        # Construir la URL para la API de Tomorrow.io
        url = f"https://api.tomorrow.io/v4/weather/forecast"
        
        # Parámetros de la solicitud
        params = {
            "location": f"{lat},{lon}",
            "apikey": TOMORROW_IO_API_KEY,
            "units": "metric",
            "timesteps": "1h",
        }
        
        print(f"Realizando solicitud a: {url}")
        print(f"Parámetros: {params}")
        
        # Realizar la solicitud con timeout
        response = requests.get(url, params=params, timeout=10)
        print(f"Respuesta recibida. Status code: {response.status_code}")
        
        # Verificar si la respuesta fue exitosa
        response.raise_for_status()
        
        data = response.json()
        print("Datos recibidos correctamente de Tomorrow.io")
        
        # Procesar los datos para obtener información relevante
        timeline = data.get("timelines", {}).get("hourly", [])
        print(f"Timeline recibido con {len(timeline)} elementos")
        
        # Obtener pronóstico para las próximas 24 horas
        pronostico_24h = []
        for hora in timeline[:120]:
            timestamp = hora.get("time")
            valores = hora.get("values", {})
            probabilidad_lluvia = valores.get("precipitationProbability", 0)

            intensidad_lluvia = valores.get("rainIntensity", 0)       # mm/h de lluvia
            acumulado_lluvia = valores.get("rainAccumulation", 0)     # mm acumulados en esa hora
            temperatura = valores.get("temperature", 0)
            temperatura = valores.get("temperature", 0)
            
            pronostico_24h.append({
                "hora": datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%H:%M"),
                "probabilidad_lluvia": probabilidad_lluvia,
                "intensidad_lluvia": intensidad_lluvia,
                "acumulado_lluvia": acumulado_lluvia,
                "temperatura": temperatura
            })
        
        # Calcular promedios y máximos para las próximas 24 horas
        if pronostico_24h:
            prob_promedio = sum(h["probabilidad_lluvia"] for h in pronostico_24h) / len(pronostico_24h)
            prob_maxima = max(h["probabilidad_lluvia"] for h in pronostico_24h)
            intensidad_maxima = max(h["intensidad_lluvia"] for h in pronostico_24h)
            intensidad_total = sum(h["intensidad_lluvia"] for h in pronostico_24h)
            acumulado_total = sum(h["acumulado_lluvia"] for h in pronostico_24h)
        else:
            prob_promedio = prob_maxima = intensidad_maxima = intensidad_total = 0
        
        print(f"Pronóstico procesado: {prob_promedio:.1f}% promedio de lluvia")
        
        return {
            "pronostico_24h": pronostico_24h,
            "probabilidad_promedio": prob_promedio,
            "probabilidad_maxima": prob_maxima,
            "intensidad_maxima": intensidad_maxima,
            "intensidad_total": intensidad_total,
            "acumulado_total": acumulado_total,
            "exito": True
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con Tomorrow.io: {str(e)}")
        print(f"Detalles: {e.response.text if hasattr(e, 'response') and e.response else 'No hay respuesta'}")
        return {
            "exito": False,
            "error": f"Error de conexión: {str(e)}"
        }
    except Exception as e:
        print(f"Error inesperado obteniendo pronóstico: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "exito": False,
            "error": str(e)
        }


def consultar_riesgo_por_coordenadas(lat: float, lon: float) -> Dict[str, Any]:
    """Consulta el riesgo de inundación para coordenadas específicas"""
    try:
        print(f"Consultando coordenadas: {lat}, {lon}")
        
        # Validar que las coordenadas estén dentro de los límites aproximados de la CDMX
        if not (19.0 <= lat <= 19.6) or not (-99.4 <= lon <= -98.9):
            print("Coordenadas fuera de CDMX")
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
        
        # Si está muy lejos (más de 50 km), considerar que está fuera de la CDMX
        if distancia_km > 50.0:
            print("Coordenadas demasiado lejos de CDMX")
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
        
        # Obtener datos de pronóstico
        print("🌤️ Solicitando datos meteorológicos...")
        pronostico = obtener_pronostico_lluvia(lat, lon)
        print(f"Datos meteorológicos recibidos: {pronostico['exito'] if 'exito' in pronostico else 'N/A'}")
        
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
            "fuera_de_cdmx": False,
            "pronostico_lluvia": pronostico
        }
        
    except Exception as e:
        print(f"Error grave procesando coordenadas: {str(e)}")
        import traceback
        traceback.print_exc()
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
