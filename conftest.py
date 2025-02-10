"""Служебный файл-конфигуратор Pytest."""

pytest_plugins = [
    'preconditions.config_preconditions',
    'preconditions.clients_preconditions',
    'preconditions.booking_preconditions',
    'preconditions.grpc_example_service_preconditions',
]
