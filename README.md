# Sistemas Operativos

**Esteban Peña y Andrés Gámez** · Gestión de procesos y planificación de CPU.

## Abrir

1. Extrae completamente el ZIP.
2. Haz doble clic en **ABRIR_APLICACION.cmd**.
3. El navegador abre la aplicación. Mantén abierta la ventana del servidor.
4. Para detenerla, vuelve a la ventana y pulsa Ctrl+C.

Requiere **Python 3.10 o posterior**. Sin paquetes externos ni conexión a Internet.
Verificado con Python 3.12.14 en Windows. El lanzador detecta Python instalado
o el incluido con Codex en este computador.

## Presentar

Elige E2, quantum 3, y pulsa **Ejecutar comparación**. P2 espera 11 con FCFS y 2
con Round Robin. Lleva el control a t=3 para mostrar quién usa la CPU.
Después abre E4 para explicar bloqueo por E/S y E5 para mostrar CPU ociosa.
En **Pruebas y evidencia**, pulsa **Ejecutar pruebas ahora**. La suite tiene 27
pruebas, con 800 comparaciones internas contra un modelo independiente.
Prueba también quantum cero: debe rechazarse. Descarga el JSON de cada caso.

## Qué entregar

| Carpeta o archivo | Contenido |
|---|---|
| `codigo/` | Simulador, aplicación visual y pruebas |
| `documentacion/informe_tecnico.pdf` | Informe conciso: problema, diseño, resultados, análisis y referencias |
| `documentacion/GUIA.md` | Conceptos y demostración en vivo |
| `documentacion/APORTES.md` | Participación observada, asistencia de IA y pendientes reales |
| `evidencias/` | Cinco escenarios, CSV, sensibilidad de quantum, pruebas, capturas y verificación |
| `MANIFIESTO_SHA256.json` | Huellas para comprobar la integridad de los archivos |

Las nuevas corridas se guardan en `resultados_en_vivo/`, separadas de la evidencia
incluida. No se suben automáticamente a GitHub.

## Terminal (alternativa)

Desde la raíz de esta carpeta, en PowerShell:

```powershell
.\ABRIR_APLICACION.cmd
```

Con Python disponible, desde `codigo/`:

```powershell
python app_visual.py
python -m unittest -v test_simulator test_app_visual
python main.py --output ../resultados_en_vivo/escenarios_manual
```

Si el puerto está ocupado, cierra la ejecución anterior o usa
`python app_visual.py --port 8766`.

## Alcance y requisitos

Se comparan FCFS y RR en cinco escenarios. Se modelan creación, listo, ejecución,
bloqueo y finalización; se calculan espera, respuesta, retorno, cambios de contexto
y utilización. El informe analiza equidad, inanición, riesgos y límites.
Una CPU simulada, tiempos enteros, E/S independiente y costo de contexto cero.
Los resultados **no miden el rendimiento real del computador**.

Repositorio privado: https://github.com/Jhomnsito/sistemas-operativos

La revisión, ampliación, ejecución automática y documentación se realizaron con
asistencia de IA (Codex). Los integrantes deben comprender y explicar el proyecto.
La constancia de semana 8, los aportes individuales no comprobados y el acceso del
profesor requieren información o acciones reales del equipo: no se inventan.
