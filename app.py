import os
import streamlit as st
import base64
from openai import OpenAI

# Configuración de la página con temática de vestier
st.set_page_config(page_title="SmartCloset — Gestor Inteligente", layout="centered", initial_sidebar_state="expanded")

# Función para codificar la imagen
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# ─────────────────────────────────────────────
# ESTILOS CSS: ESTÉTICA DE CLÓSET Y GEOMETRÍA
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Fondo simulando la madera texturada o interior de un vestier elegante */
    .stApp {
        background-color: #2b221e !important;
        background-image: linear-gradient(rgba(43, 34, 30, 0.9), rgba(30, 23, 20, 0.95)), 
                          repeating-linear-gradient(0deg, transparent, transparent 40px, rgba(255,255,255,0.02) 40px, rgba(255,255,255,0.02) 80px);
    }

    /* Sidebar estilo compartimento de accesorios */
    [data-testid="stSidebar"] {
        background-color: #3b2e29 !important;
        border-right: 3px solid #5c473f;
    }
    
    [data-testid="stSidebar"] * {
        color: #f4eee1 !important;
    }

    /* Tarjeta tipo "Estante de Armario" */
    .closet-shelf {
        background: #473731 !important;
        border: 2px solid #6b5349;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        color: #f4eee1 !important;
    }

    /* Títulos con tipografía elegante de moda */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #f4eee1 !important;
    }

    /* Formas geométricas decorativas que simulan camisas y pantalones estilizados */
    .hanger-bar {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 20px;
    }
    
    /* Forma geométrica de camisa (Trapezoide / Bloques) */
    .geo-shirt {
        width: 60px;
        height: 50px;
        background: #d4a373;
        clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%);
        border-radius: 4px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* Forma geométrica de pantalón (Dos bloques divididos) */
    .geo-pants {
        width: 45px;
        height: 60px;
        background: #ccd5ae;
        clip-path: polygon(10% 0%, 90% 0%, 100% 100%, 75% 100%, 50% 40%, 25% 100%, 0% 100%);
        border-radius: 4px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* Botones personalizados estilo boutique */
    .stButton button {
        background: #d4a373 !important;
        color: #2b221e !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: #faedcd !important;
        transform: translateY(-2px);
    }

    p, span, label {
        color: #d6ccc2 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BARRA LATERAL (ACCESO AL CLÓSET)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🗝️ Llave del Vestier")
    ke = st.text_input('Ingresa tu Clave OpenAI', type="password")
    if ke:
        os.environ['OPENAI_API_KEY'] = ke

    st.markdown("---")
    st.markdown("### 🧥 Estado del Clóset")
    st.info("Sube una foto de tu sección de ropa, lavandería o una prenda específica para que el asistente audite tu inventario.")

api_key = os.environ.get('OPENAI_API_KEY', '')
client = OpenAI(api_key=api_key) if api_key else None

# ─────────────────────────────────────────────
# INTERFAZ PRINCIPAL (SIMULANDO EL INTERIOR DEL ARMARIO)
# ─────────────────────────────────────────────

# Elementos geométricos visuales simulando ropa colgada en perchas
st.markdown("""
<div class="hanger-bar">
    <div class="geo-shirt" title="Camisa guardada"></div>
    <div class="geo-shirt" title="Camisa limpia"></div>
    <div class="geo-pants" title="Pantalón en uso"></div>
    <div class="geo-shirt" title="Blusa favorita"></div>
    <div class="geo-pants" title="Pantalón para lavar"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center;">
    <h1>🚪 SmartCloset AI</h1>
    <p style="font-size: 1.1rem; letter-spacing: 0.5px;">Tu asistente inteligente para saber qué lavar, qué reponer y qué dejar de comprar.</p>
</div>
<br>
""", unsafe_allow_html=True)

# Contenedor principal de estante para la carga
uploaded_file = st.file_uploader("📥 Sube la foto de tu clóset, lavandería o prenda", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("🖼️ Vista previa en el estante", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# Toggle para consultas específicas sobre la ropa
show_details = st.toggle("🔍 ¿Quieres agregar contexto o una pregunta específica sobre tu ropa?", value=False)

additional_details = ""
if show_details:
    additional_details = st.text_area(
        "Ej: ¿Tengo suficientes camisas blancas? ¿Esta prenda necesita lavado urgente?",
        disabled=not show_details
    )

# Botón de auditoría de prendas
analyze_button = st.button("✨ Auditar mi Clóset", type="primary", use_container_width=True)

# Lógica de análisis enfocada en el clóset
if uploaded_file is not None and api_key and analyze_button and client:
    with st.spinner("🔍 Analizando texturas, estado de lavado y conteo de prendas..."):
        base64_image = encode_image(uploaded_file)
        
        # Prompt especializado en gestión de clóset, lavado y compras
        prompt_text = (
            "Eres el asistente experto de un clóset inteligente. Analiza la imagen proporcionada y da tu diagnóstico en español estructurado en tres categorías claras:\n"
            "1. 🧺 ESTADO DE LAVADO: Identifica si hay ropa sucia, arrugada o que requiera lavado/mantenimiento.\n"
            "2. 🛒 RECOMENDACIÓN DE COMPRA: Indica si es necesario comprar más prendas similares (porque hay pocas o desgaste) o si por el contrario hay saturación.\n"
            "3. 🛑 DEJAR DE COMPRAR: Advierte si ya hay suficientes prendas de este tipo para evitar compras impulsivas.\n"
            "Sé muy práctico, moderno y directo."
        )
    
        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional aportado por el usuario:\n{additional_details}"
    
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ]
    
        try:
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o", messages=messages,   
                max_tokens=1200, stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(f"""
                    <div class="closet-shelf">
                        <h3>📋 Diagnóstico del Clóset:</h3>
                        {full_response}▌
                    </div>
                    """, unsafe_allow_html=True)
            
            message_placeholder.markdown(f"""
            <div class="closet-shelf">
                <h3>📋 Diagnóstico del Clóset:</h3>
                {full_response}
            </div>
            """, unsafe_allow_html=True)
    
        except Exception as e:
            st.error(f"Ocurrió un error en el vestier digital: {e}")

else:
    if not uploaded_file and analyze_button:
        st.warning("⚠️ Por favor sube una imagen para auditar tu clóset.")
    if not api_key and analyze_button:
        st.warning("🔑 Por favor ingresa tu Clave API en la barra lateral para activar el sistema.")
