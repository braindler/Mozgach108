"""
Mozgach2 - Система квантово-запутанных языковых моделей

Революционная система из 108 специализированных языковых моделей,
построенных на принципе квантовой запутанности и обученных на едином датасете.
"""

__version__ = "2.0.0"
__author__ = "Mozgach2 Team"
__description__ = "Система из 108 специализированных языковых моделей с квантовой запутанностью"

# Импорты основных компонентов
from .config import (
    Mozgach2Config,
    ModelConfig,
    ModelType,
    DeviceClass,
    config
)

from .src.mozgach2_system import (
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
    # Конфигурация
    "Mozgach2Config",
    "ModelConfig", 
    "ModelType",
    "DeviceClass",
    "config",
    
    # Основная система
    "Mozgach2System",
    "ModelManager",
    "QuantumEntanglementManager", 
    "QueryRouter",
    "QueryResult",
    "SystemStatus",
    "get_mozgach2_system",
    "shutdown_mozgach2_system"
]

# Краткое описание при импорте
print(f"🚀 Mozgach2 v{__version__} - Система квантово-запутанных языковых моделей")
print(f"📚 Всего моделей: {config.TOTAL_MODELS}")
print(f"🌍 Поддерживаемые языки: {len(config.BRICS_LANGUAGES)}")
print(f"🧘 Духовные источники: {len(config.SPIRITUAL_SOURCES)}")
print(f"⚛️ Групп квантовой запутанности: {config.QUANTUM_ENTANGLEMENT_GROUPS}")
