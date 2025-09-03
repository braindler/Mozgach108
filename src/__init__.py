"""
Mozgach2 - Система квантово-запутанных языковых моделей
"""

__version__ = "2.0.0"
__author__ = "Mozgach2 Team"
__description__ = "Система из 108 специализированных языковых моделей с квантовой запутанностью"

from .mozgach2_system import (
    Mozgach2System,
    ModelManager,
    QuantumEntanglementManager,
    QueryRouter,
    QueryResult,
    SystemStatus,
    get_mozgach2_system,
    shutdown_mozgach2_system
)

__all__ = [
    "Mozgach2System",
    "ModelManager", 
    "QuantumEntanglementManager",
    "QueryRouter",
    "QueryResult",
    "SystemStatus",
    "get_mozgach2_system",
    "shutdown_mozgach2_system"
]
