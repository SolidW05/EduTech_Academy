# EduTech Academy Agent

Este proyecto implementa un asistente conversacional para EduTech Academy, una plataforma educativa online. El agente puede responder preguntas sobre políticas institucionales, documentación oficial y datos académicos estructurados, combinando recuperacion de informacion (RAG) con consultas a una base de datos SQL.

## Descripción general

La solución ofrece una interfaz de chat basada en Streamlit donde el usuario puede hacer preguntas en lenguaje natural y recibir respuestas contextualizadas. El sistema esta diseñado para:

- Responder preguntas sobre documentos oficiales como reglamentos, políticas, manuales y FAQ.
- Consultar informacion estructurada como precios de cursos, cupos, instructores, certificados y estados de inscripciones.
- Resolver consultas complejas que requieren combinar ambas fuentes de informacion.
- Pedir aclaraciones cuando la pregunta no tiene suficiente contexto.

## Arquitectura de la solución

La arquitectura esta organizada en capas para separar la interfaz, la orquestacion del flujo y las fuentes de conocimiento.

```text
Usuario -> Streamlit UI -> LangGraph workflow -> Router
                                      |-> RAG layer
                                      |-> SQL layer
                                      |-> Hybrid layer
                                      |-> Clarification node
```

### Componentes principales

- Frontend: interfaz conversacional en Streamlit.
- Orquestador: grafo de estados construido con LangGraph.
- Router: decide si la consulta debe ir a RAG, SQL, Hybrid o solicitar aclaracion.
- RAG: carga documentos markdown, los divide en fragmentos, genera embeddings y recupera informacion relevante desde FAISS.
- SQL: consulta una base de datos SQLite mediante modelos SQLAlchemy y cadenas de consulta generadas por LLM.
- Modelos LLM: se utilizan modelos de Google Gemini para el enrutamiento, la generacion de respuestas y la formulacion de preguntas de aclaracion.

## Tecnologías y herramientas utilizadas

- Python 3.10+
- Streamlit para la interfaz web
- LangGraph para la orquestacion del agente
- LangChain y LangChain Core para los pipelines de prompts y herramientas
- Google Gemini para procesamiento y respuesta generativa
- FAISS para indexacion y recuperacion vectorial
- SQLAlchemy para el acceso a la base de datos
- SQLite como base de datos local
- Python-dotenv para variables de entorno
- pydantic para validacion de estructuras

## Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener:

- Python instalado
- Una clave de API de Google para Gemini
- Acceso a internet para la ejecucion de los modelos de lenguaje

## Instrucciones para ejecutar el proyecto

1. Clona el repositorio y entra a la carpeta del proyecto.
2. Crea y activa un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` en la raiz del proyecto con la siguiente variable:

```env
GOOGLE_API_KEY=tu_clave_aqui
```

Opcionalmente puedes agregar estas variables si vas a extender la integracion a otros servicios:

```env
COHERE_API_KEY=tu_clave_aqui
PINECONE_API_KEY=tu_clave_aqui
```

5. Inicializa la base de datos de ejemplo:

```bash
python -c "from database.seed import seed; seed()"
```

6. Ejecuta la aplicacion:

```bash
streamlit run app.py
```

> Si la base documental aun no ha sido indexada, el sistema la construira automaticamente la primera vez que se ejecute.

## Ejemplos de preguntas que puede responder el agente

- ¿Cuál es la política de reembolsos?
- ¿Cómo solicito una beca?
- ¿Cuánto cuesta el curso de Python desde cero?
- ¿Quién imparte el curso de Machine Learning Aplicado?
- ¿Cuántos cupos quedan en el curso de Data Science?
- ¿Cómo puedo verificar si un certificado es válido?
- ¿Qué cursos ofrece la plataforma sobre inteligencia artificial?

## Ejemplos de respuestas generadas por el agente

Ejemplo 1:

> La politica de reembolsos permite solicitar devolucion dentro de los 7 dias naturales posteriores a la compra, siempre que se cumplan las condiciones establecidas en la normativa de la plataforma.

Ejemplo 2:

> El curso Python desde Cero tiene un precio de 59.99 y cuenta con 70 cupos disponibles.

Ejemplo 3:

> El curso de Machine Learning Aplicado es impartido por Laura Gómez y Carlos Ramírez, especialistas en Machine Learning y Deep Learning.

## Estructura del proyecto

```text
app.py                  # interfaz principal de Streamlit
config/                 # configuraciones y variables de entorno
graph/                  # grafo LangGraph y nodos del agente
rag/                    # cargador, splitter, retriever y vectorstore RAG
database/              # modelos SQLAlchemy, seed y acceso a datos
docs/                   # documentos usados para RAG
tools/                  # herramientas para consultar documentos y base de datos
prompts/                # prompts del router, aclaracion y reformulacion
```

## Notas adicionales

- El agente puede usar diferentes rutas segun la naturaleza de la pregunta.
- Para consultas relacionadas con documentos, prioriza la recuperacion semantica.
- Para consultas de datos numericos o estructurados, utiliza la base de datos.
- Cuando falta informacion, hace preguntas de aclaracion antes de responder.
