"""Разные константы которые не заслужили отдельного модуля."""

from dataclasses import dataclass
from os.path import abspath
from pathlib import Path

ROOT_PROJECT_PATH = abspath(Path(__file__).parent.parent.parent)


@dataclass
class GRPCMethodType:
    """Типы GRPC запросов."""

    UNARY = 'UNARY'
    SERVER_STREAM = 'SERVER_STREAM'
    CLIENT_STREAM = 'CLIENT_STREAM'
    BIDIRECTIONAL = 'BIDIRECTIONAL'

