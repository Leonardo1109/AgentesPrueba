from langchain.agents import tool, AgentExecutor
from langchain.agents import create_react_agent
from langchain_deepseek import ChatDeepSeek  # ← Cambio importante
from langchain import hub
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# OBTENER LA API KEY
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    print("❌ ERROR: No se encontró DEEPSEEK_API_KEY en el archivo .env")
    exit(1)

# 1. Configurar DeepSeek CORREGIDO
llm = ChatDeepSeek(  # ← Usamos ChatDeepSeek en lugar de DeepSeek
    model="deepseek-chat",
    api_key=api_key,
    temperature=0.1
)

# 2. Herramientas (las mismas que antes)
@tool
def multiplicar(numeros: str) -> str:
    """Multiplica dos números. Ejemplo: '5, 3' -> 15"""
    try:
        a, b = map(float, numeros.split(','))
        return f"Resultado: {a * b}"
    except:
        return "Error: Usa formato 'numero1, numero2'"

@tool  
def saludar(nombre: str) -> str:
    """Saluda a una persona. Ejemplo: 'Juan' -> 'Hola Juan!'"""
    return f"¡Hola {nombre}! ¿Cómo estás?"

herramientas = [multiplicar, saludar]

# 3. Crear el agente
prompt = hub.pull("hwchase17/react")
agente = create_react_agent(llm, herramientas, prompt)
ejecutor = AgentExecutor(agent=agente, tools=herramientas, verbose=True, handle_parsing_errors=True)

# 4. Probarlo
print("🤖 Agente de Prueba Activado (escribe 'salir' para terminar)")
print("💡 Prueba con: 'multiplica 8 por 5' o 'saluda a Ana'")
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