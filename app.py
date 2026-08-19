import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="PROMETHEUS · Coevaluación", page_icon="◈", layout="wide")

DATA_FILE = Path(__file__).parent / "estudiantes.csv"
students = pd.read_csv(DATA_FILE, dtype={"id": str})
students["id"] = students["id"].str.strip()
students["mision01"] = students["mision01"].astype(int)

CRITERIA = [
    ("Cumplimiento del rol", 0.25),
    ("Aporte al producto", 0.20),
    ("Razonamiento anatómico", 0.20),
    ("Colaboración y comunicación", 0.20),
    ("Responsabilidad y profesionalismo", 0.15),
]
LEVELS = {4:"Desempeño destacado", 3:"Desempeño competente",
          2:"Desempeño en desarrollo", 1:"Desempeño insuficiente"}

st.markdown("""
<style>
.stApp { background:#071018; color:#EAF7FF; }
.block-container { max-width:1150px; padding-top:2rem; }
h1,h2,h3 { color:#5CE1FF; }
.case-card { border:1px solid #16485C; border-radius:14px; padding:18px;
background:linear-gradient(135deg,#09151F,#071018); margin-bottom:14px; }
</style>
""", unsafe_allow_html=True)

st.title("PROMETHEUS")
st.caption("COEVALUACIÓN · MISIÓN 01")

if "evaluator" not in st.session_state:
    st.session_state.evaluator = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

with st.sidebar:
    st.header("Acceso")
    entered_id = st.text_input("ID institucional", max_chars=20, type="password")
    if st.button("Ingresar", use_container_width=True):
        match = students[students["id"] == entered_id.strip()]
        if match.empty:
            st.error("ID no encontrado.")
        else:
            st.session_state.evaluator = match.iloc[0].to_dict()
            st.session_state.submitted = False
            st.rerun()

    if st.session_state.evaluator:
        ev = st.session_state.evaluator
        st.divider()
        st.write(f"**Equipo {int(ev['mision01'])}**")
        st.write(ev["nombre_completo"])
        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state.evaluator = None
            st.session_state.submitted = False
            st.rerun()

if not st.session_state.evaluator:
    st.info("Ingresa tu ID institucional desde el panel lateral para comenzar.")
    st.stop()

ev = st.session_state.evaluator
group = int(ev["mision01"])
classmates = students[(students["mision01"] == group) & (students["id"] != ev["id"])].sort_values("nombre_completo")

st.markdown(f'<div class="case-card"><h3>Equipo {group}</h3>'
            '<div>Evalúa a cada integrante de tu equipo excepto a ti mismo.</div></div>',
            unsafe_allow_html=True)

with st.form("coevaluation_form"):
    all_results = []
    for _, person in classmates.iterrows():
        st.subheader(person["nombre_completo"])
        values = {}
        for criterion, weight in CRITERIA:
            values[criterion] = st.radio(
                f"{criterion} · {int(weight*100)} %",
                [4,3,2,1],
                format_func=lambda x: f"{x} — {LEVELS[x]}",
                horizontal=True,
                key=f"{person['id']}_{criterion}",
            )
        comment = st.text_area(
            "Aportación concreta que justifica tu evaluación",
            key=f"{person['id']}_comment",
            placeholder="Describe una aportación, conducta o evidencia observable."
        )
        improvement = st.text_area(
            "¿Qué podría mejorar en próximas misiones? (opcional)",
            key=f"{person['id']}_improvement"
        )
        all_results.append((person, values, comment, improvement))
        st.divider()

    submitted = st.form_submit_button("ENVIAR COEVALUACIÓN", use_container_width=True)

if submitted:
    rows = []
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    for person, values, comment, improvement in all_results:
        weighted = sum(values[c] * w for c,w in CRITERIA)
        row = {
            "timestamp": timestamp,
            "evaluador_id": ev["id"],
            "evaluador_nombre": ev["nombre_completo"],
            "equipo": group,
            "evaluado_id": person["id"],
            "evaluado_nombre": person["nombre_completo"],
            "puntuacion_ponderada_4": round(weighted,3),
            "puntuacion_porcentaje": round(weighted/4*100,2),
            "comentario": comment.strip(),
            "mejora": improvement.strip(),
        }
        for criterion,_ in CRITERIA:
            row[criterion] = values[criterion]
        rows.append(row)

    result_df = pd.DataFrame(rows)
    results_file = Path(__file__).parent / "results.csv"
    if results_file.exists():
        old = pd.read_csv(results_file)
        old = old[~((old["evaluador_id"].astype(str) == str(ev["id"])) &
                    (old["equipo"] == group))]
        result_df = pd.concat([old, result_df], ignore_index=True)
    result_df.to_csv(results_file, index=False, encoding="utf-8-sig")
    st.session_state.submitted = True
    st.success("Coevaluación registrada.")

if st.session_state.submitted:
    st.info("Coevaluación enviada. Puedes cerrar sesión.")
