# PROMETHEUS · Coevaluación Misión 01

Aplicación web para coevaluación de equipos.

- El estudiante ingresa únicamente su ID.
- El sistema identifica automáticamente su equipo.
- Solo aparecen sus compañeros de la Misión 01.
- No puede evaluarse a sí mismo.
- La rúbrica conserva los pesos 25/20/20/20/15 % y cada nivel incluye una descripción conductual específica.
- Se solicitan evidencias y una mejora opcional.
- Se indica explícitamente que la evaluación debe basarse en conductas y aportaciones observables, no en afinidad personal.
- Los resultados se almacenan en CSV en modo local.

## Datos y privacidad

`estudiantes.csv` contiene nombres e IDs. Mantén el repositorio **privado** si contiene estos datos.

## Despliegue

El proyecto está preparado para GitHub + Streamlit Community Cloud.

Importante: el `results.csv` local sirve para pruebas, pero el almacenamiento local de Streamlit Cloud no es persistente. Para usarlo con una clase real, conviene conectar los resultados a una base persistente (por ejemplo Supabase/PostgreSQL o Google Sheets) y después ofrecer el botón de exportación CSV.

El siguiente paso recomendado es configurar ese backend antes de entregar el enlace a los estudiantes.
