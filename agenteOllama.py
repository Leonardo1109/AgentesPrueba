# agenteOllama.py
from langchain.agents import tool, AgentExecutor
from langchain.agents import create_react_agent
from langchain_community.chat_models import ChatOllama
from langchain import hub
import re

# 1. Configurar Ollama
llm = ChatOllama(
    model="llama3.2",
    temperature=0.1
)

# 2. Herramientas MEJORADAS
@tool
def multiplicar(numeros: str) -> str:
    """Multiplica dos números. Acepta: '3 por 4', '3*4', '3,4', '3 y 4'"""
    try:
        # Limpiamos y extraemos los números de cualquier formato
        numeros = numeros.replace('por', ',').replace('y', ',').replace('*', ',')
        numeros = re.sub(r'[^\d,\.]', '', numeros)  # Removemos todo excepto números, puntos y comas
        
        # Separamos por coma y convertimos a float
        partes = numeros.split(',')
        if len(partes) != 2:
            return "Error: Necesito exactamente dos números. Ejemplos: '3 por 4', '5,6', '7*8'"
        
        a = float(partes[0].strip())
        b = float(partes[1].strip())
        return f"El resultado de {a} * {b} es {a * b}"
        
    except ValueError:
        return "Error: Asegúrate de usar números válidos. Ejemplo: '3.5 por 2'"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

@tool  
def saludar(nombre: str) -> str:
    """Saluda a una persona. Ejemplo: 'Juan' -> 'Hola Juan!'"""
    # Extraer solo el nombre si viene con otras palabras
    if ' ' in nombre:
        nombre = nombre.split(' ')[-1]  # Toma la última palabra como nombre
    
    # FORMATO QUE NO ENLOQUECE AL JEFE:
    return f"Saludo completado para: {nombre}"

herramientas = [multiplicar, saludar]

# 3. Crear el agente CON LÍMITE
prompt = hub.pull("hwchase17/react")
agente = create_react_agent(llm, herramientas, prompt)
ejecutor = AgentExecutor(
    agent=agente, 
    tools=herramientas, 
    verbose=True, 
    handle_parsing_errors=True,
    max_iterations=3  # ← ¡LÍMITE DE 3 CICLOS MÁXIMO!
)

# 4. Probarlo
print("🤖 Agente con Ollama Activado (100% gratis!)")
print("💡 Prueba con: 'multiplica 8 por 5', '3*4', 'saluda a María'")
print("⚠️  Máximo 3 iteraciones - no se volverá loco")
print("-" * 50)

while True:
    user_input = input("\nTú: ")
    if user_input.lower() in ['salir', 'exit', 'quit']:
        break
        
    try:
        resultado = ejecutor.invoke({"input": user_input})
        print(f"\n🤖 Agente: {resultado['output']}")
    except Exception as e:
        print(f"❌ Error: {e}")