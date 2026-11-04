# Sistemas Operativos - ejecución

Integrantes: Esteban Peña y Andrés Gámez.

1. Extraer completamente el ZIP.
2. Abrir **ABRIR_APLICACION.cmd** y mantener abierta la ventana del servidor.
3. Elegir un escenario y pulsar **Ejecutar comparación**.
4. En **Pruebas y evidencia**, pulsar **Ejecutar pruebas ahora**.
5. Para cerrar, volver a la ventana del servidor y pulsar Ctrl+C.

Requiere Python 3.10 o posterior. Sin paquetes externos. Verificado en Windows
con Python 3.12.14. El lanzador admite el Python incluido con Codex en este equipo.
Si el puerto está ocupado, cerrar la ejecución anterior.

Alternativa desde PowerShell, en `codigo/`:

```powershell
python app_visual.py
python -m unittest -v test_simulator test_app_visual
python main.py --output ../resultados_en_vivo/escenarios_manual
```

Para otro puerto: `python app_visual.py --port 8766`.
Las corridas nuevas se guardan en `resultados_en_vivo/`, separadas de la evidencia
incluida. Descargas JSON desde la aplicación conservan entradas, métricas y trazas.

La carpeta `codigo/` contiene implementación y pruebas; `documentacion/`, el
informe y la descripción de funciones; `evidencias/`, registros y capturas.
`MANIFIESTO_SHA256.json` permite comprobar integridad de la entrega.

Repositorio: https://github.com/Jhomnsito/sistemas-operativos
