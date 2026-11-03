"""Lanzador portable. Se copia como ejecutar.py a la entrega final."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description='Ejecutar una demostración nueva del proyecto de Sistemas Operativos.')
    parser.add_argument('accion', choices=('simulacion', 'ejemplo', 'pruebas'))
    parser.add_argument('--sin-pausa', action='store_true', help='Opción usada por los accesos CMD durante la verificación.')
    args = parser.parse_args(argv)
    if sys.version_info < (3, 10):
        parser.error('Se requiere Python 3.10 o posterior.')
    folder = Path(__file__).resolve().parent
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    output = folder / 'resultados_en_vivo' / (stamp + '_' + args.accion)
    output.mkdir(parents=True)
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1', SO_OUTPUT_DIR=str(output))
    commands = {
        'simulacion': [sys.executable, '-u', 'main.py', '--output', str(output)],
        'ejemplo': [sys.executable, '-u', 'demostracion_en_vivo.py'],
        'pruebas': [sys.executable, '-u', 'demostracion_pruebas.py'],
    }
    command = commands[args.accion]
    print('SISTEMAS OPERATIVOS - Esteban Pena y Andres Gamez', flush=True)
    print('Ejecucion nueva:', args.accion, flush=True)
    print('Python:', sys.version.split()[0], flush=True)
    print('Resultados:', output, flush=True)
    (output / 'comando.json').write_text(json.dumps({
        'action': args.accion, 'command': command, 'python': sys.version,
        'description': 'Ejecución nueva realizada con este lanzador.'
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    try:
        with (output / 'consola.txt').open('w', encoding='utf-8') as log:
            run = subprocess.Popen(command, cwd=folder, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            for line in run.stdout:
                print(line, end='', flush=True)
                log.write(line)
            status = run.wait()
        (output / 'estado.json').write_text(json.dumps({'exit_code': status}, indent=2), encoding='utf-8')
        print('\nResultado:', 'CORRECTO' if status == 0 else 'ERROR', flush=True)
        print('Evidencias guardadas en:', output, flush=True)
        return status
    except OSError as error:
        print('No se pudo completar la ejecucion:', error, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
