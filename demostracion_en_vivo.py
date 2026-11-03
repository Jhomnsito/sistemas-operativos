"""Demostración breve y real del escenario E2, sin depender de logs anteriores."""
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
import io
import os
from pathlib import Path
import sys
import unittest

from algorithms import simulate_fcfs, simulate_round_robin, print_comparison_report
from models import Process


class ScreenAndLog:
    def __init__(self, screen, log):
        self.screen, self.log = screen, log

    def write(self, text):
        self.screen.write(text)
        self.log.write(text)
        self.flush()
        return len(text)

    def flush(self):
        self.screen.flush()
        self.log.flush()


def demo():
    print('DEMOSTRACION EN VIVO - PLANIFICACION DE CPU')
    print('Nueva ejecucion:', datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %z'))
    print('Ejemplo E2: un proceso largo llega antes que dos procesos cortos.')
    print('Entradas: P1 llega en 0 y requiere 12 de CPU.')
    print('          P2 llega en 1 y requiere 2 de CPU.')
    print('          P3 llega en 2 y requiere 4 de CPU.')
    print('Round Robin usa quantum 3. Todos los tiempos son simulados.')
    processes = [Process(1, 0, 12), Process(2, 1, 2), Process(3, 2, 4)]
    fcfs = simulate_fcfs(processes)
    rr = simulate_round_robin(processes, 3)
    print_comparison_report('FCFS - calculado en esta ejecucion', fcfs)
    print_comparison_report('Round Robin Q=3 - calculado en esta ejecucion', rr)
    print('\nCOMPROBACION DEL EJEMPLO')
    for result in (fcfs, rr):
        total = sum(s['end'] - s['start'] for s in result.timeline if s['pid'] is not None)
        if total != 18 or any(p.remaining_time != 0 for p in result):
            raise AssertionError('El ejemplo no conserva la CPU o deja procesos pendientes.')
        print(f'{result.algorithm}: CPU consumida = {total}; todos los procesos finalizaron.')
    print('\nPRUEBAS AUTOMATIZADAS - ejecutadas ahora')
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent), pattern='test_simulator.py')
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=1).run(suite)
    if not result.wasSuccessful():
        raise AssertionError('Hay pruebas fallidas.')
    print('\nDEMOSTRACION COMPLETADA CORRECTAMENTE')
    print('Esta ventana muestra una ejecucion nueva, no un archivo de resultados anterior.')


if __name__ == '__main__':
    destination = Path(os.environ.get('SO_OUTPUT_DIR', str(Path(__file__).resolve().parent / 'resultados_demo'))) / 'demostracion_en_vivo.txt'
    destination.parent.mkdir(exist_ok=True)
    with destination.open('w', encoding='utf-8') as log:
        out = ScreenAndLog(sys.stdout, log)
        with redirect_stdout(out), redirect_stderr(out):
            demo()
    print('\nPuedes mantener esta ventana abierta para revisar los resultados.')
