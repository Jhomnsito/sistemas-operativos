"""Escenarios originales 1 a 3 y dos escenarios añadidos para cubrir estados."""
from models import Process


def scenarios():
    """Construye cargas nuevas (id, descripción, quantum RR, lista Process).

    E1-E3 conservan las cargas originales; E4 cubre E/S y E5 tiempos ociosos.
    """
    return [
        ('E1', 'Carga escalonada', 3,
         [Process(1, 0, 5), Process(2, 1, 3), Process(3, 2, 8), Process(4, 3, 6)]),
        ('E2', 'Efecto convoy', 3,
         [Process(1, 0, 12), Process(2, 1, 2), Process(3, 2, 4)]),
        ('E3', 'Llegadas simultáneas', 4,
         [Process(1, 0, 4), Process(2, 0, 6), Process(3, 0, 8)]),
        ('E4', 'Bloqueo y reactivación por E/S', 2,
         [Process(1, 0, 6, io_events=[(2, 4)]), Process(2, 1, 5), Process(3, 2, 3)]),
        ('E5', 'CPU ociosa y llegada tardía', 2,
         [Process(1, 3, 2), Process(2, 10, 3)]),
    ]
