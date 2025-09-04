# mozgach108 - Система квантово-запутанных языковых моделей
"""
mozgach108 - Система из 108 квантово-запутанных языковых моделей

Этот модуль предоставляет базовую архитектуру для работы с системой
из 108 специализированных моделей, объединенных квантовой запутанностью.
"""

__version__ = "1.0.0"
__author__ = "Mozgach108 Team"
__license__ = "NativeMindNONC"

from .mozgach108_system import Mozgach108System
from .model_manager import ModelManager
from .quantum_entanglement import QuantumEntanglement
from .knowledge_domains import KnowledgeDomains

__all__ = [
    "Mozgach108System",
    "ModelManager", 
    "QuantumEntanglement",
    "KnowledgeDomains"
]
