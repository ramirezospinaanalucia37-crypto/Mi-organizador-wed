from datetime import date
import pandas as pd
import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="Academic Planner & Organizer", page_icon="✨", layout="wide"
)

# 2. Aplicar colores personalizados (Rosado, Magenta y Blanco)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #faf4f7;
        color: #2d2a2e;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #e65c9c, #a81173) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
        color: #a81173 !important;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Encabezado Principal
st.title("✨ Planner & Academic Organizer")
st.caption(
    "Gestión inteligente de tareas, exámenes y prioridades de estudio diario."
)

# 4. Datos iniciales de la agenda
if "tareas" not in st.session_state:
  st.session_state.tareas = [
      {
          "Actividad": "Examen Parcial de Física",
          "Tipo": "Examen",
          "Prioridad": "Urgente",
          "Días Restantes": 2,
          "Horas Estimadas": 4.5,
      },
      {
          "Actividad": "Ensayo de Inglés",
          "Tipo": "Tarea",
          "Prioridad": "Alta",
          "Días Restantes": 4,
          "Horas Estimadas": 3.0,
      },
      {
          "Actividad": "Proyecto de Logística SENA",
          "Tipo": "Proyecto",
          "Prioridad": "Media",
          "Días Restantes": 6,
          "Horas Estimadas": 5.0,
      },
      {
          "Actividad": "Ejercicios de Derivadas",
          "Tipo": "Tarea",
          "Prioridad": "Media",
          "Días Restantes": 7,
          "Horas Estimadas": 2.0,
      },
  ]

# 5. Estructura visual en dos columnas
col_formulario, col_agenda = st.columns([1, 2])

with col_formulario:
  st.subheader("➕ Registrar Nueva Actividad")

  with st.form("nuevo_registro", clear_on_submit=True):
    titulo = st.text_input("Nombre de la actividad:")
    tipo = st.selectbox(
        "Categoría:", ["Examen", "Tarea", "Proyecto", "Revisión"]
    )
    prioridad = st.select_slider(
        "Prioridad / Peso en la Nota:",
        options=["Baja", "Media", "Alta", "Urgente"],
    )
    fecha_entrega = st.date_input("Fecha Límite:", min_value=date.today())
    horas = st.number_input(
        "Horas Estimadas de Estudio:", min_value=0.5, step=0.5, value=2.0
    )

    guardar = st.form_submit_button("💖 Guardar en mi Agenda")

    if guardar and titulo:
      dias_faltantes = (fecha_entrega - date.today()).days
      st.session_state.tareas.append({
          "Actividad": titulo,
          "Tipo": tipo,
          "Prioridad": prioridad,
          "Días Restantes": dias_faltantes,
          "Horas Estimadas": horas,
      })
      st.success(f"¡'{titulo}' se ha guardado correctamente!")

with col_agenda:
  st.subheader("📅 Plan Semanal de Trabajo")

  df = pd.DataFrame(st.session_state.tareas)

  m1, m2, m3 = st.columns(3)
  m1.metric(label="Tareas Activas", value=len(df))
  m2.metric(
      label="Tiempo Total Requerido", value=f"{df['Horas Estimadas'].sum()} hrs"
  )

  examenes = df[df["Tipo"] == "Examen"]
  proximo = (
      f"{examenes['Días Restantes'].min()} días"
      if not examenes.empty
      else "Sin exámenes"
  )
  m3.metric(label="Próximo Examen", value=proximo)

  st.dataframe(df, use_container_width=True)

  st.info(
      "💡 **Recomendación Personalizada:** El *Examen Parcial de Física* vence"
      " en 2 días. Te recomendamos estudiar hoy 2.25 horas para avanzar el 50%"
      " del temario con tranquilidad."
  )
