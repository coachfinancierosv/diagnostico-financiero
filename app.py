import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración inicial de la página web
st.set_page_config(
    page_title="Diagnóstico de Salud Financiera | Coach Financiero",
    page_icon="📊",
    layout="centered"
)

# Inicializar la conexión con Google Sheets usando Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Función para enviar notificaciones por correo electrónico de fondo
def enviar_correo_notificacion(nombre, email, telefono, score, salud, interes):
    try:
        usuario_envio = st.secrets["email"]["usuario"]
        password_envio = st.secrets["email"]["password"]
        destinatario = st.secrets["email"]["destinatario"]
        
        msg = MIMEMultipart()
        msg['From'] = usuario_envio
        msg['To'] = destinatario
        msg['Subject'] = f"🚀 NUEVO DIAGNÓSTICO: {nombre} ({salud})"
        
        cuerpo_mensaje = f"""
        Se ha registrado un nuevo diagnóstico financiero en la plataforma web.
        
        DATOS DEL PROSPECTO:
        - Nombre completo: {nombre}
        - Correo electrónico: {email}
        - Teléfono de contacto: {telefono}
        - ¿Desea una asesoría personalizada?: {interes}
        
        RESULTADO DEL DIAGNÓSTICO:
        - Score Obtenido: {score:.1f} / 100 puntos
        - Nivel de Salud Financiera: {salud}
        
        Inicia sesión en tu Google Sheets para ver el desglose completo de sus ingresos y gastos.
        """
        msg.attach(MIMEText(cuerpo_mensaje, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(usuario_envio, password_envio)
        server.sendmail(usuario_envio, destinatario, msg.as_string())
        server.quit()
    except Exception:
        pass  # Evita que un fallo en el correo trabe la pantalla del usuario

# INTERFAZ GRÁFICA DE LA APLICACIÓN
st.image("https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?q=80&w=600", use_container_width=True)
st.title("📊 Diagnóstico Instantáneo de Salud Financiera")
st.write("Completa este breve formulario y recibe en tiempo real tu score de salud financiera y recomendaciones clave basadas en tu nivel de ingresos, gastos y endeudamiento.")

st.markdown("---")

# SECCIÓN 1: DATOS PERSONALES
st.subheader("👤 1. Información General")
col1, col2 = st.columns(2)
with col1:
    nombre = st.text_input("Nombre Completo:", placeholder="Ej. Juan Pérez")
    correo = st.text_input("Correo Electrónico:", placeholder="ejemplo@correo.com")
with col2:
    telefono = st.text_input("Número de Teléfono / WhatsApp:", placeholder="Ej. +503 7000-0000")
    edad = st.number_input("Edad:", min_value=18, max_value=100, value=30, step=1)

# SECCIÓN 2: FLUJO DE DINERO
st.subheader("💰 2. Ingresos y Egresos Mensuales")
fuente_ingreso = st.selectbox("Tu principal fuente de ingresos es:", ["Empleado asalariado", "Empresario / Comerciante", "Freelancer / Servicios Profesionales", "Remesas / Otros"])

c1, c2 = st.columns(2)
with c1:
    ingresos = st.number_input("Tus ingresos mensuales principales ($):", min_value=0.0, value=500.0, step=50.0)
    otros_ingresos = st.number_input("Otros ingresos mensuales ($):", min_value=0.0, value=0.0, step=50.0)
with c2:
    g_vivienda = st.number_input("Vivienda (Alquiler o Hipoteca) ($):", min_value=0.0, value=150.0, step=25.0)
    g_vida = st.number_input("Gastos de Vida (Comida, Servicios, Transporte) ($):", min_value=0.0, value=200.0, step=25.0)

c3, c4 = st.columns(2)
with c3:
    g_educacion = st.number_input("Educación y Seguros ($):", min_value=0.0, value=0.0, step=25.0)
    g_entretenimiento = st.number_input("Entretenimiento, salidas o lujos ($):", min_value=0.0, value=25.0, step=5.0)
with c4:
    g_ahorro = st.number_input("Ahorro o Inversión activa actual ($):", min_value=0.0, value=0.0, step=10.0)
    deudas = st.number_input("Pago mensual total en deudas (Tarjetas, Créditos) ($):", min_value=0.0, value=50.0, step=10.0)

# Cálculos automáticos internos
ingresos_totales = ingresos + otros_ingresos
gastos_totales = g_vivienda + g_vida + g_educacion + g_entretenimiento
ahorro_calculado = ingresos_totales - gastos_totales - deudas

st.markdown("---")

# SECCIÓN 3: LLAMADO A LA ACCIÓN
st.subheader("🎯 3. ¿Cómo puedo ayudarte?")
interes_asesoria = st.checkbox("Sí, me interesa recibir una sesión estratégica de planificación financiera para optimizar mi dinero.")

st.markdown("<br>", unsafe_allow_html=True)

# Botón para procesar todo
if st.button("Generar Mi Diagnóstico Financiero", type="primary", use_container_width=True):
    
    # Cálculos de proporciones
    if ingresos_totales > 0:
        pct_gasto = gastos_totales / ingresos_totales
        pct_deuda = deudas / ingresos_totales
        pct_ahorro = (g_ahorro + max(0, ahorro_calculado)) / ingresos_totales
    else:
        pct_gasto = pct_deuda = pct_ahorro = 0.0

    puntos_gasto = 100 if pct_gasto <= 0.6 else (80 if pct_gasto <= 0.7 else (60 if pct_gasto <= 0.8 else (40 if pct_gasto <= 0.9 else 20)))
    puntos_deuda = 100 if pct_deuda <= 0.2 else (80 if pct_deuda <= 0.3 else (60 if pct_deuda <= 0.4 else (40 if pct_deuda <= 0.5 else 20)))
    puntos_ahorro = 100 if pct_ahorro >= 0.2 else (80 if pct_ahorro >= 0.15 else (60 if pct_ahorro >= 0.1 else (40 if pct_ahorro >= 0.05 else 20)))

    score_final = (puntos_gasto + puntos_deuda + puntos_ahorro) / 3
    
    if ahorro_calculado < 0:
        score_final = min(score_final, 45.0)

    # Definir niveles de salud
    if score_final >= 85:
        nivel_salud, color, recomendacion = "EXCELENTE", "success", "Tu estructura financiera es sólida. Enfócate en inversión y crecimiento patrimonial."
    elif score_final >= 70:
        nivel_salud, color, recomendacion = "BUENA", "info", "Tienes una buena base, con excelentes oportunidades de optimización."
    elif score_final >= 50:
        nivel_salud, color, recomendacion = "RIESGO MODERADO", "warning", "Hay desbalances que pueden comprometer tu estabilidad futura. Un presupuesto guiado te ayudará."
    else:
        nivel_salud, color, recomendacion = "CRÍTICA", "error", "Tus gastos mensuales o deudas superan tus ingresos reales. Requiere un plan de choque urgente."

    st.write("## 📊 Tu Resultado de Diagnóstico")
    
    # Tarjeta de Score Final
    mensaje_score = f"**SCORE LOGRADO: {score_final:.1f} / 100 puntos (Salud Financiera: {nivel_salud})**"
    if color == "success":
        st.success(mensaje_score)
    elif color == "info":
        st.info(mensaje_score)
    elif color == "warning":
        st.warning(mensaje_score)
    else:
        st.error(mensaje_score)

    # Mostrar métricas clave en 3 columnas
    st.markdown("### Indicadores Básicos de Distribución:")
    m1, m2, m3 = st.columns(3)
    m1.metric("Gastos Mensuales", f"${gastos_totales:,.2f}", f"{pct_gasto*100:.1f}% de tus ingresos")
    m2.metric("Pago de Deudas", f"${deudas:,.2f}", f"{pct_deuda*100:.1f}% de tus ingresos")
    m3.metric("Flujo Neto Estimado", f"${ahorro_calculado:,.2f}", f"{pct_ahorro*100:.1f}% de capacidad de ahorro")

    st.markdown(f"**Consejo del Coach:** {recomendacion}")
    
    # =========================================================
    # GUARDAR EN GOOGLE SHEETS Y ENVIAR CORREO
    # =========================================================
    interes_texto = "SÍ" if interes_asesoria else "NO"
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Guardar datos en Google Sheets de forma segura
    try:
        nuevo_registro = pd.DataFrame([{
            "Fecha": fecha_actual,
            "Nombre": nombre if nombre else "Anónimo",
            "Telefono": telefono,
            "Correo": correo,
            "Edad": edad,
            "Fuente_Ingreso": fuente_ingreso,
            "Ingresos_Totales": ingresos_totales,
            "Gastos_Totales": gastos_totales,
            "Deudas": deudas,
            "Ahorro_Calculado": ahorro_calculado,
            "Score": round(score_final, 1),
            "Salud_Financiera": nivel_salud,
            "Interes_Asesoria": interes_texto
        }])
        
        df_existente = conn.read()
        df_completo = pd.concat([df_existente, nuevo_registro], ignore_index=True)
        conn.update(data=df_completo)
        
    except Exception as e:
        st.error(f"Error al registrar en la base de datos: {e}")
    
    # Enviar correo de notificación de fondo
    enviar_correo_notificacion(
        nombre=nombre if nombre else "Anónimo",
        email=correo,
        telefono=telefono,
        score=score_final,
        salud=nivel_salud,
        interes=interes_texto
    )

    # Generar Reporte de Texto para Descargar
    reporte_txt = f"""==================================================
        DIAGNÓSTICO DE SALUD FINANCIERA           
             COACH FINANCIERO SV                  
==================================================

CLIENTE: {nombre if nombre else 'Cliente Anónimo'}
TELÉFONO: {telefono}   |   CORREO: {correo}
EDAD: {edad} años  |   FUENTE: {fuente_ingreso}
INTERESADO EN ASESORÍA PERSONALIZADA: {interes_texto}
--------------------------------------------------

1. RESUMEN DE FLUJO DE CAJA:
   (+) Ingresos Principales:          ${ingresos:,.2f}
   (+) Otros Ingresos:                ${otros_ingresos:,.2f}
   (=) INGRESOS TOTALES:              ${ingresos_totales:,.2f}
   (-) Gastos Operativos Totales:     ${gastos_totales:,.2f} ({pct_gasto*100:.1f}%)
   (-) Cuotas de Deudas:              ${deudas:,.2f} ({pct_deuda*100:.1f}%)
   (=) Flujo Neto Disponible:         ${ahorro_calculado:,.2f}

2. EVALUACIÓN MAESTRA:
   SCORE LOGRADO: {score_final:.1f} / 100 puntos
   NIVEL DE SALUD FINANCIERA: {nivel_salud}

3. RECOMENDACIÓN:
   • {recomendacion}

==================================================
"""
    
    # Botón de Descarga Web
    st.download_button(
        label="Descargar mi Diagnóstico en PDF/Texto",
        data=reporte_txt,
        file_name=f"Diagnostico_{nombre.replace(' ', '_') if nombre else 'Cliente'}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    if interes_asesoria:
        st.balloons()
        st.success("¡Excelente decisión! Me pondré en contacto contigo pronto para agendar tu sesión estratégica.")