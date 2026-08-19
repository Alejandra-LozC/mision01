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
    {
        "name": "Cumplimiento del rol",
        "weight": 0.25,
        "descriptors": {
            4: "Cumple de manera constante y autónoma las responsabilidades asignadas. Se anticipa a las necesidades del equipo y contribuye a que la misión avance.",
            3: "Cumple adecuadamente las responsabilidades asignadas y realiza las tareas requeridas dentro del tiempo establecido.",
            2: "Cumple solo parte de las responsabilidades o requiere recordatorios y seguimiento para completar sus tareas.",
            1: "No cumple las responsabilidades asignadas o su falta de participación afecta el avance del equipo.",
        },
    },
    {
        "name": "Aporte al producto",
        "weight": 0.20,
        "descriptors": {
            4: "Realiza aportaciones sustanciales que mejoran la calidad, precisión o utilidad del producto final. Sus contribuciones son claramente identificables.",
            3: "Realiza aportaciones pertinentes que contribuyen de manera directa a completar el producto solicitado.",
            2: "Realiza aportaciones ocasionales, incompletas o que requieren ser corregidas o complementadas por otros integrantes.",
            1: "Su aportación es mínima, poco pertinente o no contribuye de manera significativa al producto final.",
        },
    },
    {
        "name": "Razonamiento anatómico",
        "weight": 0.20,
        "descriptors": {
            4: "Utiliza conocimientos anatómicos para interpretar información, establecer relaciones y justificar sus decisiones con precisión. Puede explicar el porqué de sus conclusiones.",
            3: "Aplica correctamente conceptos anatómicos para resolver la tarea y proporciona explicaciones adecuadas de sus conclusiones.",
            2: "Reconoce algunos conceptos anatómicos, pero presenta dificultades para relacionarlos, justificarlos o aplicarlos al problema planteado.",
            1: "Presenta dificultades importantes para aplicar los conceptos anatómicos o sus conclusiones carecen de fundamento anatómico.",
        },
    },
    {
        "name": "Colaboración y comunicación",
        "weight": 0.20,
        "descriptors": {
            4: "Escucha, comunica sus ideas con claridad, integra las aportaciones de los demás y favorece activamente el trabajo del equipo. Ayuda a resolver desacuerdos de manera constructiva.",
            3: "Se comunica de manera clara y respetuosa, participa en las discusiones y considera las aportaciones de sus compañeros.",
            2: "Participa de manera irregular, comunica sus ideas de forma poco clara o tiene dificultades para integrar las aportaciones de otros.",
            1: "Presenta poca disposición para colaborar, dificulta la comunicación o no favorece el trabajo conjunto.",
        },
    },
    {
        "name": "Responsabilidad y profesionalismo",
        "weight": 0.15,
        "descriptors": {
            4: "Cumple acuerdos y tiempos, mantiene una actitud responsable y demuestra iniciativa, respeto y compromiso con el trabajo del equipo.",
            3: "Cumple los acuerdos y tiempos establecidos y mantiene una actitud respetuosa y responsable durante la misión.",
            2: "Presenta incumplimientos ocasionales de acuerdos o tiempos y requiere recordatorios para mantener su participación y compromiso.",
            1: "Incumple repetidamente acuerdos o tiempos, muestra poca responsabilidad o afecta negativamente el funcionamiento del equipo.",
        },
    },
]


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

st.markdown(
    '<div class="case-card"><strong>Instrucción:</strong> '
    'Evalúa el desempeño observado durante la misión, no la personalidad o afinidad '
    'que tengas con la persona. Basa tu valoración en conductas y aportaciones que '
    'hayas podido observar.</div>',
    unsafe_allow_html=True,
)

with st.form("coevaluation_form"):
    all_results = []
    for _, person in classmates.iterrows():
        st.subheader(person["nombre_completo"])
        values = {}
        for criterion in CRITERIA:
            criterion_name = criterion["name"]
            weight = criterion["weight"]
            options = [4, 3, 2, 1]

            st.markdown(
                f"**{criterion_name} — {int(weight * 100)} %**"
            )

            values[criterion_name] = st.radio(
                "Selecciona el nivel que mejor describe el desempeño observado:",
                options,
                format_func=lambda x, d=criterion["descriptors"]: (
                    f"{x} — {d[x]}"
                ),
                key=f"{person['id']}_{criterion_name}",
                label_visibility="collapsed",
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
        weighted = sum(values[c["name"]] * c["weight"] for c in CRITERIA)
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
        for criterion in CRITERIA:
            row[criterion["name"]] = values[criterion["name"]]
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
