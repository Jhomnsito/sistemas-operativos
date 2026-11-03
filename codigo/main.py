"""Ejecutar desde esta carpeta: python main.py --output evidencias"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys
from algorithms import simulate_fcfs, simulate_round_robin, print_comparison_report
from scenarios import scenarios


def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Comparar FCFS y Round Robin con tiempos simulados.')
    parser.add_argument('--output', type=Path, default=Path('evidencias'), help='Carpeta de resultados')
    args = parser.parse_args(argv)
    try:
        args.output.mkdir(parents=True, exist_ok=True)
        summaries, details, traces, states, inputs = [], [], [], [], []
        for key, name, quantum, processes in scenarios():
            print(f'\n[{key}] {name}')
            inputs.append({'scenario': key, 'name': name, 'quantum': quantum,
                           'processes': [{'pid': p.pid, 'arrival_time': p.arrival_time,
                                          'burst_time': p.burst_time, 'io_events': p.io_events}
                                         for p in processes]})
            for result in [simulate_fcfs(processes), simulate_round_robin(processes, quantum)]:
                print_comparison_report(result.algorithm, result)
                base = {'scenario': key, 'algorithm': result.algorithm}
                summaries.append(dict(base, **result.metrics()))
                details.extend(dict(base, pid=p.pid, arrival=p.arrival_time, cpu=p.burst_time,
                                    blocked=p.blocked_time, start=p.start_time, end=p.completion_time,
                                    waiting=p.waiting_time, turnaround=p.turnaround_time,
                                    response=p.response_time, remaining=p.remaining_time,
                                    state=p.state.value) for p in sorted(result, key=lambda p: p.pid))
                traces.extend(dict(base, **s) for s in result.timeline)
                states.extend(dict(base, **e) for e in result.events)
        sensitivity = []
        convoy = scenarios()[1][3]
        for quantum in (1, 3, 6, 12):
            result = simulate_round_robin(convoy, quantum)
            sensitivity.append(dict(scenario='E2', quantum=quantum, **result.metrics()))
        for name, rows in [('resumen.csv', summaries), ('procesos.csv', details),
                           ('cpu.csv', traces), ('estados.csv', states),
                           ('sensibilidad_quantum.csv', sensitivity)]:
            write_csv(args.output / name, rows)
        (args.output / 'entradas.json').write_text(json.dumps(inputs, indent=2, ensure_ascii=False), encoding='utf-8')
        folder = Path(__file__).resolve().parent
        manifest = {'python': sys.version, 'platform': platform.platform(),
                    'time_unit': 'unidad simulada; no equivale a segundos medidos',
                    'command': 'python main.py --output evidencias',
                    'sha256_sources': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                       for p in sorted(folder.glob('*.py'))}}
        (args.output / 'entorno.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f'\nEvidencias guardadas en: {args.output}')
    except (OSError, ValueError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
