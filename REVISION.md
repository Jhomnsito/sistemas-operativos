# Revisión del ZIP recibido

## Dictamen

El ZIP original sirve como avance funcional de la opción 1, planificación de CPU.
No era una entrega final completa. Contenía solamente `models.py`, `algorithms.py`
y `main.py`. No había informe, instrucciones, evidencias guardadas ni registro de
aportes. No se observó código que accediera a Internet, ejecutara comandos del
sistema o modificara archivos. Esto es una revisión del código recibido, no una
certificación universal de seguridad ni de autoría.

La ejecución de sus tres escenarios terminó con código 0. Sus tiempos de espera,
retorno y respuesta coinciden exactamente con la versión corregida en las seis
ejecuciones comparadas. Los tres ejemplos no eran resultados inventados: salen del
código. El ZIP no contenía un informe con afirmaciones o referencias que contrastar.
No es posible certificar la autoría o la historia de trabajo a partir de tres archivos.

## Fallos comprobados y corrección

1. **Quantum cero o negativo.** La ejecución no terminó dentro del límite de un
   segundo y se interrumpió. La lógica confirma el problema: con cero no disminuye
   la CPU pendiente; con valor negativo aumenta. Ahora se exige un entero positivo.
2. **Reporte vacío.** Produjo `ZeroDivisionError`. Ahora imprime que no hay procesos
   y define los promedios como cero por convención.
3. **FCFS no actualizaba CPU restante.** Un proceso de CPU 5 terminó como
   `FINALIZADO` conservando `remaining_time=5`. Ahora todos finalizan con cero.
4. **Reutilización de entradas.** Repetir RR con el mismo proceso de CPU 3 produjo
   retorno cero en la segunda ejecución, porque el objeto ya estaba agotado.
   Ahora cada algoritmo crea copias nuevas a partir de los datos originales.
5. **Entradas negativas.** Una CPU -3 produjo finalización y retorno -3. La llegada
   negativa también fue aceptada. Ahora se validan tipos, rangos, PID únicos y E/S.
6. **Bloqueo solo declarado.** `BLOCKED` no se utilizaba. Se implementaron E/S de
   duración fija, bloqueo, reactivación y trazas con instantes y motivos.
7. **Análisis incompleto.** Se añadieron cambios de contexto y despachos separados,
   utilización, máximos de espera/respuesta, sensibilidad al quantum, riesgos y límites.
8. **Faltaban entregables.** Se añadieron README, PDF técnico, versión editable del
   informe, CSV, logs, pruebas y una guía de sustentación.

Los puntos 6 a 8 amplían el alcance para cubrir la consigna; no representan
funcionalidades ni documentos presentes en la entrega original. `APORTES.md` deja
constancia de la asistencia recibida sin atribuirla a integrantes desconocidos.

## Contraste con las indicaciones del profesor

| Requisito | ZIP recibido | Versión revisada |
|---|---|---|
| Creación y finalización simuladas | Sí; FCFS con dato restante inconsistente | Sí, con dato restante coherente |
| Listo, ejecución, bloqueado, finalizado | Bloqueado sin implementar; sin historial | Implementados y registrados |
| Dos algoritmos | FCFS y RR | Conservados |
| Mínimo tres escenarios | Tres | Cinco más sensibilidad al quantum |
| Espera, respuesta, retorno | Calculados para los tres ejemplos | Conservados y verificados |
| Contexto, equidad e inanición | Sin análisis | Métricas y análisis en informe |
| Errores básicos | Sin validación suficiente | Validaciones y errores de archivo |
| Evidencias reproducibles | Solo consola al ejecutar | CSV, entradas, trazas y logs |
| Informe técnico PDF | Ausente | Incluido |
| Limitaciones, riesgos y referencias | Ausentes | Incluidos |
| Repositorio o carpeta compartida | No acreditado | Debe aportarlo el equipo |
| Historial de aportes | Ausente | Formato pendiente de completar con hechos |
| Revisión de semana 8 | Sin evidencia en el ZIP | No verificable aquí |
| Sustentación individual | No verificable | Guía de preparación incluida |

## Verificación ejecutada

- Python 3.12.14 en Windows. Código original: ejecución normal con salida 0.
- Versión corregida: cinco escenarios con ambos algoritmos y cuatro quantum en E2.
- 19 métodos de prueba aprobados; 200 cargas generadas con semilla 2620,
  cada una con FCFS y RR de quantum 1, 2 y 5: 800 comparaciones contra un
  segundo modelo por ticks que no usa las clases ni el motor del simulador.
- Casos manuales, bloqueo múltiple, empates, CPU ociosa, errores, reutilización de
  entrada y equivalencia entre FCFS y RR con quantum suficientemente grande.
- Recálculo independiente de los promedios y de la CPU consumida usando los CSV.
- Prueba de salida cuyo destino era un archivo: error legible y código de salida 1.

Estos resultados respaldan los casos evaluados; no prueban que cualquier extensión
futura o cualquier carga de tamaño arbitrario sea correcta. Los tiempos simulados
no se presentaron como mediciones del procesador real.

## Lo que el equipo todavía debe completar

Los nombres y aportes reales de hasta cuatro integrantes, el historial o evidencias
de colaboración, el enlace real del repositorio/carpeta y la constancia de semana 8
no se pueden reconstruir honestamente. Completa esos datos sin fabricar commits,
fechas, asistentes, capturas ni validaciones del profesor. Si no existe un historial
previo, reconoce esa limitación y empieza a registrar los cambios reales actuales.

Actualización del 3 de noviembre de 2026: el usuario confirmó un equipo de dos,
Esteban Peña y Andrés Gámez. Sus nombres ya se incorporaron al informe y al
registro de aportes. Las contribuciones individuales y sus evidencias siguen
pendientes. El guion de exposición es una propuesta, no un historial de trabajo.

La versión corregida incluye asistencia de IA en revisión, código, pruebas y
documentación. El equipo debe verificarla, comprenderla y poder explicarla,
como indica el apartado 8 de la consigna.
