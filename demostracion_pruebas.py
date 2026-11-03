"""Ejecuta las pruebas existentes y muestra sus nombres en la demostración."""
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from pathlib import Path
import sys
import os
import unittest
from demostracion_en_vivo import ScreenAndLog


folder = Path(__file__).resolve().parent
destination = Path(os.environ.get('SO_OUTPUT_DIR', str(folder / 'resultados_demo'))) / 'pruebas_en_vivo.txt'
destination.parent.mkdir(parents=True, exist_ok=True)
with destination.open('w', encoding='utf-8') as log:
    output = ScreenAndLog(sys.stdout, log)
    with redirect_stdout(output), redirect_stderr(output):
        print('PRUEBAS EN VIVO DEL SIMULADOR')
        print('Nueva ejecucion:', datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %z'))
        print('Cada linea terminada en ok indica una prueba aprobada.')
        print('Casos clave: tiempos calculados a mano, quantum invalido, E/S y reutilizacion.')
        print('La prueba generada incluye 800 comparaciones con un segundo modelo.\n')
        suite = unittest.defaultTestLoader.discover(str(folder), pattern='test_simulator.py')
        result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
        print('\nRESULTADO:', 'TODAS APROBADAS' if result.wasSuccessful() else 'HAY FALLOS')
        print('Son 19 metodos de prueba; las 800 comparaciones son subcasos de uno de ellos.')
        print('Este resultado se calculo ahora; no se leyo un log anterior.')
if not result.wasSuccessful():
    raise SystemExit(1)
