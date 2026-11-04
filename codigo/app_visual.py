"""Aplicación local de demostración; usa el simulador y unittest existentes.

Python estándar. No necesita instalar paquetes ni conectarse a Internet.
"""
import argparse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
from threading import Timer
import webbrowser

from algorithms import simulate_fcfs, simulate_round_robin
from models import Process
from scenarios import scenarios

ROOT = Path(__file__).resolve().parent
MAX_BODY = 24000
MAX_CPU_UNITS = 2000


def scenario_data():
    """Devuelve los cinco escenarios como registros serializables a JSON."""
    return [dict(id=code, name=name, quantum=q, processes=[
        dict(pid=p.pid, arrival=p.arrival_time, cpu=p.burst_time, io=list(p.io_events))
        for p in ps]) for code, name, q, ps in scenarios()]


def save_evidence(kind, data):
    """Guarda una ejecución fechada y devuelve sus datos con la ruta de evidencia.

    Args: kind identifica la operación; data contiene entradas y resultados.
    Raises: OSError si la carpeta o el JSON no pueden escribirse.
    """
    directory = ROOT.parent / 'resultados_en_vivo' / (datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '_' + kind)
    directory.mkdir(parents=True)
    data['evidence'] = str(directory)
    (directory / 'resultado.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return data


def compare(payload):
    """Valida una carga, compara FCFS/RR y guarda métricas, procesos y trazas.

    payload contiene processes (pid, arrival, cpu, io) y quantum entero.
    Devuelve un diccionario JSON. Lanza ValueError ante una carga inválida.
    Los límites acotan el volumen de trazas representado por el navegador.
    """
    if not isinstance(payload, dict):
        raise ValueError('La entrada debe ser un objeto JSON.')
    rows, quantum = payload.get('processes'), payload.get('quantum')
    if not isinstance(rows, list) or not 1 <= len(rows) <= 30:
        raise ValueError('Introduce entre 1 y 30 procesos.')
    if type(quantum) is not int or not 1 <= quantum <= 1000:
        raise ValueError('El quantum debe ser un entero entre 1 y 1000.')
    ps = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Cada proceso debe tener PID, llegada y CPU.')
        for key in ('pid', 'arrival', 'cpu'):
            if type(row.get(key)) is not int or not 0 <= row[key] <= 1000:
                raise ValueError('PID, llegada y CPU deben ser enteros de hasta 1000.')
        io = row.get('io', [])
        if not isinstance(io, list) or len(io) > 20:
            raise ValueError('E/S debe ser una lista con hasta 20 pares.')
        for event in io:
            if not isinstance(event, (list, tuple)) or len(event) != 2 or any(type(v) is not int or not 1 <= v <= 1000 for v in event):
                raise ValueError('Cada E/S debe contener CPU acumulada y duración, enteros de 1 a 1000.')
        ps.append(Process(row['pid'], row['arrival'], row['cpu'], io_events=io))
    if sum(p.burst_time for p in ps) > MAX_CPU_UNITS:
        raise ValueError(f'La carga visual admite hasta {MAX_CPU_UNITS} unidades de CPU en total.')
    results = []
    for result in (simulate_fcfs(ps), simulate_round_robin(ps, quantum)):
        results.append(dict(algorithm=result.algorithm, metrics=result.metrics(), timeline=result.timeline,
            events=sorted(result.events, key=lambda e: e['time']), processes=[dict(
                pid=p.pid, arrival=p.arrival_time, cpu=p.burst_time, blocked=p.blocked_time,
                finish=p.completion_time, waiting=p.waiting_time, response=p.response_time,
                turnaround=p.turnaround_time) for p in sorted(result, key=lambda p: p.pid)]))
    return save_evidence('visual_comparacion', dict(kind='comparison', timestamp=datetime.now().astimezone().isoformat(),
        input=payload, results=results, units='Unidades de tiempo simulado; una CPU; costo de cambio de contexto cero.'))


def run_tests():
    """Ejecuta unittest con límite de 45 s y conserva salida y código de retorno.

    Devuelve evidencia de éxito, fallo o timeout; no interpreta salida antigua.
    """
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    command = [sys.executable, '-m', 'unittest', '-v', 'test_simulator', 'test_app_visual']
    try:
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', timeout=45)
        data = dict(kind='tests', timestamp=datetime.now().astimezone().isoformat(),
                    success=result.returncode == 0, exit_code=result.returncode,
                    output=result.stdout + result.stderr, command=command)
    except subprocess.TimeoutExpired:
        data = dict(kind='tests', success=False, exit_code=None, output='Las pruebas excedieron el límite de 45 segundos.')
    return save_evidence('visual_pruebas', data)


class Handler(BaseHTTPRequestHandler):
    """Atiende exclusivamente los recursos y operaciones de la aplicación local."""
    def reply(self, code, payload, content_type='application/json; charset=utf-8'):
        """Envía bytes o un objeto JSON con estado HTTP y longitud de contenido."""
        body = payload if isinstance(payload, bytes) else json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def local_request(self):
        """Comprueba que Host y Origin correspondan al puerto local del servidor."""
        expected = f'127.0.0.1:{self.server.server_port}'
        return self.headers.get('Host') == expected and self.headers.get('Origin', f'http://{expected}') == f'http://{expected}'

    def do_GET(self):
        """Sirve la interfaz y sus recursos explícitos o los escenarios iniciales."""
        if not self.local_request():
            return self.reply(403, {'error': 'Solicitud ajena a la aplicación local.'})
        resources = {
            '/': ('interfaz.html', 'text/html; charset=utf-8'),
            '/interfaz.js': ('interfaz.js', 'text/javascript; charset=utf-8'),
            '/estilos.css': ('estilos.css', 'text/css; charset=utf-8'),
        }
        if self.path in resources:
            filename, content_type = resources[self.path]
            try:
                return self.reply(200, (ROOT / filename).read_bytes(), content_type)
            except OSError:
                return self.reply(500, {'error': 'No se pudo leer un recurso de la interfaz.'})
        if self.path == '/api/scenarios':
            return self.reply(200, scenario_data())
        self.reply(404, {'error': 'Ruta inexistente.'})

    def do_POST(self):
        """Recibe JSON acotado para comparar o probar; devuelve errores legibles."""
        if not self.local_request():
            return self.reply(403, {'error': 'Solicitud ajena a la aplicación local.'})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= MAX_BODY:
                raise ValueError('Tamaño de solicitud inválido.')
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict):
                raise ValueError('La entrada debe ser un objeto JSON.')
            if self.path == '/api/compare':
                return self.reply(200, compare(payload))
            if self.path == '/api/tests':
                return self.reply(200, run_tests())
            self.reply(404, {'error': 'Ruta inexistente.'})
        except UnicodeDecodeError:
            self.reply(400, {'error': 'El cuerpo debe ser JSON codificado en UTF-8.'})
        except (ValueError, TypeError, KeyError) as error:
            self.reply(400, {'error': str(error)})
        except OSError:
            self.reply(500, {'error': 'No se pudo ejecutar o guardar la evidencia. Revisa los permisos de la carpeta.'})


def main():
    """Abre un servidor local, opcionalmente el navegador, y espera hasta Ctrl+C."""
    parser = argparse.ArgumentParser(description='Interfaz visual local de Sistemas Operativos')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error('El puerto debe estar entre 0 y 65535.')
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    except OSError as error:
        print(f'No se pudo abrir el servidor local: {error}. Cierra la instancia anterior o usa --port con otro puerto.')
        return 1
    url = f'http://127.0.0.1:{server.server_port}'
    print(f'SISTEMAS OPERATIVOS — aplicación visual\nAbre {url}\nMantén esta ventana abierta. Ctrl+C para detener.', flush=True)
    if not args.no_browser:
        Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nAplicación detenida.')
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
