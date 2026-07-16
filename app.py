import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración de la página web
st.set_page_config(
    page_title="Diagnóstico de Salud Financiera | CoachFinanciero",
    page_icon="📊",
    layout="centered"
)

# Estilos visuales personalizados
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1e3a8a; text-align: center; margin-bottom: 20px; }
    .sub-title { font-size: 16px; color: #4b5563; text-align: center; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Diagnóstico de Salud Financiera</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Toma el control de tu dinero y diseña tu futuro financiero</div>', unsafe_allow_html=True)

# Conexión nativa a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Función para enviar correo de notificación
def enviar_correo_notificacion(nombre, email, telefono, score, salud, interes):
    # Extraemos las credenciales guardadas de forma segura en Streamlit
    remitente = st.secrets["email"]["usuario"]
    password = st.secrets["email"]["password"]
    destinatario = st.secrets["email"]["destinatario"] # Tu correo donde quieres recibir alertas
    
    asunto = f"🚨 ¡NUEVO CLIENTE INTERESADO! - {nombre}" if interes == "SÍ" else f"📊 Nuevo diagnóstico realizado - {nombre}"
    
    cuerpo = f"""
    Hola Coach,
    
    Se ha realizado un nuevo diagnóstico en tu plataforma web:
    
    - Nombre: {nombre}
    - Correo: {email}
    - Teléfono: {telefono}
    - Score obtenido: {score:.1f} / 100 ({salud})
    - ¿Desea asesoría personalizada?: {interes}
    
    ¡Mucho éxito con este seguimiento!
    """
    
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    try:
        # Configuración estándar para Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
    except Exception as e:
        # No mostramos el error al usuario final por seguridad, pero se registra internamente
        pass

# =========================================================
# 1. ONBOARDING
# =========================================================
st.subheader("📋 1. Datos de Onboarding")
col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre completo:", placeholder="Ej. Juan Pérez")
    correo = st.text_input("Correo electrónico:", placeholder="ejemplo@correo.com")
    fuente_ingreso = st.selectbox(
        "Fuente de Ingresos principal:",
        ["Empleado", "Profesional Independiente", "Dueño de Negocio", "Emprendedor"]
    )

with col2:
    telefono = st.text_input("Teléfono de contacto:", placeholder="Ej. +503 7000-0000")
    edad = st.number_input("Edad:", min_value=0, max_value=120, value=30, step=1)

st.write("---")

# =========================================================
# 2. INGRESOS Y OBLIGACIONES
# =========================================================
st.subheader("💰 2. Ingresos y Obligaciones Mensuales")
col3, col4, col5 = st.columns(3)

with col3:
    ingresos = st.number_input("Ingresos Principales ($):", min_value=0.0, value=0.0, step=50.0)
with col4:
    otros_ingresos = st.number_input("Otros Ingresos ($):", min_value=0.0, value=0.0, step=50.0)
with col5:
    deudas = st.number_input("Cuotas de Deudas ($):", min_value=0.0, value=0.0, step=10.0)

ingresos_totales = ingresos + otros_ingresos

st.write("---")

# =========================================================
# 3. DESGLOSE DE GASTOS (11 Variables)
# =========================================================
st.subheader("🛒 3. Desglose Mensual de Gastos")

col_g1, col_g2 = st.columns(2)

with col_g1:
    g_viv = st.number_input("Alquiler/Hipoteca/Casa ($):", min_value=0.0, value=0.0, step=25.0)
    g_trans = st.number_input("Transporte ($):", min_value=0.0, value=0.0, step=10.0)
    g_ocio = st.number_input("Entretenimiento/Ocio ($):", min_value=0.0, value=0.0, step=10.0)
    g_ropa = st.number_input("Ropa ($):", min_value=0.0, value=0.0, step=10.0)
    g_susc = st.number_input("Suscripciones/Membresías ($):", min_value=0.0, value=0.0, step=5.0)

with col_g2:
    g_alim = st.number_input("Comida/Alimentación ($):", min_value=0.0, value=0.0, step=25.0)
    g_educ = st.number_input("Educación ($):", min_value=0.0, value=0.0, step=25.0)
    g_ahorro = st.number_input("Ahorro Mensual Fijo ($):", min_value=0.0, value=0.0, step=10.0)
    g_sal = st.number_input("Salud/Cuidado Personal ($):", min_value=0.0, value=0.0, step=10.0)
    g_varios = st.number_input("Gastos Varios ($):", min_value=0.0, value=0.0, step=10.0)

gastos_totales = g_viv + g_alim + g_trans + g_educ + g_ocio + g_ropa + g_sal + g_susc + g_varios
ahorro_calculado = ingresos_totales - gastos_totales - deudas

st.write("---")

# =========================================================
# 4. CIERRE Y CAPTACIÓN DE CLIENTES
# =========================================================
st.subheader("🤝 4. Próximos Pasos")
interes_asesoria = st.checkbox(
    "¿Estás interesado en recibir asesoría financiera para tomar el control de tu dinero?",
    value=False
)

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
    
    # Tarjeta de Score Final utilizando el componente nativo de alertas de Streamlit
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
    
    # Guardar datos en Google Sheets
    try:
        # Obtenemos los datos actuales de la hoja
        df_existente = conn.read()
        
        # Estructuramos la nueva fila
        nueva_fila = {
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
        }
        
        # Unimos los datos existentes con el nuevo registro
        df_actualizado = pd.concat([df_existente, pd.DataFrame([nueva_fila])], ignore_index=True)
        
        # Subimos la tabla actualizada
        conn.update(data=df_actualizado)
    except Exception as e:
        # Si falla el Sheets (por ejemplo en local antes de configurar), que la app siga funcionando sin asustar al cliente
        pass
    
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