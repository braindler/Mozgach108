"""
Конфигурация проекта Mozgach2
Система квантово-запутанных языковых моделей
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ModelType(Enum):
    """Типы специализированных моделей"""
    GENERAL = "general"
    TECHNICAL = "technical"
    SPIRITUAL = "spiritual"
    CONVERSATIONAL = "conversational"
    BUSINESS = "business"
    CREATIVE = "creative"
    SPECIALIZED = "specialized"


class DeviceClass(Enum):
    """Классы устройств по объему памяти"""
    MOBILE = "mobile"      # 1-4GB RAM
    TABLET = "tablet"      # 4-8GB RAM
    DESKTOP = "desktop"    # 8-16GB RAM
    SERVER = "server"      # 16GB+ RAM


@dataclass
class ModelConfig:
    """Конфигурация отдельной модели"""
    name: str
    type: ModelType
    device_class: DeviceClass
    max_context_length: int
    model_size_mb: int
    languages: List[str]
    specializations: List[str]
    quantum_entanglement_group: int


class Mozgach2Config:
    """Основная конфигурация системы Mozgach2"""
    
    # Общие настройки
    PROJECT_NAME = "Mozgach2"
    VERSION = "2.0.0"
    TOTAL_MODELS = 108
    
    # Пути к файлам
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    CACHE_DIR = os.path.join(BASE_DIR, "cache")
    
    # Настройки моделей по типам
    MODEL_DISTRIBUTION = {
        ModelType.GENERAL: 16,
        ModelType.TECHNICAL: 20,
        ModelType.SPIRITUAL: 18,
        ModelType.CONVERSATIONAL: 22,
        ModelType.BUSINESS: 12,
        ModelType.CREATIVE: 12,
        ModelType.SPECIALIZED: 8
    }
    
    # Распределение по классам устройств
    DEVICE_DISTRIBUTION = {
        DeviceClass.MOBILE: 24,
        DeviceClass.TABLET: 36,
        DeviceClass.DESKTOP: 32,
        DeviceClass.SERVER: 16
    }
    
    # Языки БРИКС
    BRICS_LANGUAGES = [
        "pt",  # Португальский (Бразилия)
        "ru",  # Русский (Россия)
        "hi",  # Хинди (Индия)
        "zh",  # Китайский (Китай)
        "en",  # Английский (ЮАР)
        "af",  # Африкаанс (ЮАР)
        "zu",  # Зулу (ЮАР)
        "bn",  # Бенгальский (Индия)
        "te",  # Телугу (Индия)
        "ta"   # Тамильский (Индия)
    ]
    
    # Духовные источники
    SPIRITUAL_SOURCES = [
        "buddhism",      # Буддизм
        "hinduism",      # Индуизм
        "islam",         # Ислам
        "christianity",  # Христианство
        "judaism",       # Иудаизм
        "taoism",        # Даосизм
        "confucianism",  # Конфуцианство
        "zen",           # Дзен
        "sufism",        # Суфизм
        "kabbalah"       # Каббала
    ]
    
    # Настройки квантовой запутанности
    QUANTUM_ENTANGLEMENT_GROUPS = 12  # 108 моделей / 9 моделей в группе
    MODELS_PER_GROUP = 9
    
    # Настройки производительности
    MAX_CONTEXT_LENGTH = 32768  # 32K токенов
    MIN_MODEL_SIZE_MB = 50
    MAX_MODEL_SIZE_MB = 500
    
    # Настройки кэширования
    CACHE_SIZE_GB = 10
    MODEL_CACHE_TTL_HOURS = 24
    
    # Настройки логирования
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # API настройки
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    API_WORKERS = 4
    
    # Настройки мониторинга
    ENABLE_METRICS = True
    METRICS_PORT = 9090
    HEALTH_CHECK_INTERVAL = 30
    
    @classmethod
    def get_model_configs(cls) -> List[ModelConfig]:
        """Генерирует конфигурации для всех 108 моделей"""
        configs = []
        model_id = 0
        
        for model_type, count in cls.MODEL_DISTRIBUTION.items():
            for i in range(count):
                # Определяем класс устройства на основе ID модели
                device_class = cls._get_device_class(model_id)
                
                # Определяем группу квантовой запутанности
                quantum_group = model_id // cls.MODELS_PER_GROUP
                
                config = ModelConfig(
                    name=f"mozgach2_{model_type.value}_{i+1:02d}",
                    type=model_type,
                    device_class=device_class,
                    max_context_length=cls.MAX_CONTEXT_LENGTH,
                    model_size_mb=cls._get_model_size(model_type, device_class),
                    languages=cls._get_languages_for_model(model_type),
                    specializations=cls._get_specializations_for_model(model_type),
                    quantum_entanglement_group=quantum_group
                )
                configs.append(config)
                model_id += 1
        
        return configs
    
    @classmethod
    def _get_device_class(cls, model_id: int) -> DeviceClass:
        """Определяет класс устройства для модели по её ID"""
        if model_id < 24:
            return DeviceClass.MOBILE
        elif model_id < 60:
            return DeviceClass.TABLET
        elif model_id < 92:
            return DeviceClass.DESKTOP
        else:
            return DeviceClass.SERVER
    
    @classmethod
    def _get_model_size(cls, model_type: ModelType, device_class: DeviceClass) -> int:
        """Определяет размер модели на основе типа и класса устройства"""
        base_sizes = {
            ModelType.GENERAL: 100,
            ModelType.TECHNICAL: 150,
            ModelType.SPIRITUAL: 120,
            ModelType.CONVERSATIONAL: 130,
            ModelType.BUSINESS: 110,
            ModelType.CREATIVE: 140,
            ModelType.SPECIALIZED: 200
        }
        
        device_multipliers = {
            DeviceClass.MOBILE: 0.6,
            DeviceClass.TABLET: 0.8,
            DeviceClass.DESKTOP: 1.0,
            DeviceClass.SERVER: 1.2
        }
        
        base_size = base_sizes[model_type]
        multiplier = device_multipliers[device_class]
        
        return int(base_size * multiplier)
    
    @classmethod
    def _get_languages_for_model(cls, model_type: ModelType) -> List[str]:
        """Определяет языки для модели на основе её типа"""
        if model_type == ModelType.CONVERSATIONAL:
            return cls.BRICS_LANGUAGES
        elif model_type == ModelType.SPIRITUAL:
            return ["en", "ru", "hi", "zh", "sa"]  # Основные языки духовных текстов
        else:
            return ["en", "ru"]  # Базовые языки
    
    @classmethod
    def _get_specializations_for_model(cls, model_type: ModelType) -> List[str]:
        """Определяет специализации для модели на основе её типа"""
        specializations = {
            ModelType.GENERAL: ["common_knowledge", "general_qa", "conversation"],
            ModelType.TECHNICAL: ["science", "technology", "engineering", "mathematics"],
            ModelType.SPIRITUAL: ["philosophy", "religion", "meditation", "ethics"],
            ModelType.CONVERSATIONAL: ["dialogue", "culture", "idioms", "social_interaction"],
            ModelType.BUSINESS: ["economics", "finance", "management", "strategy"],
            ModelType.CREATIVE: ["art", "literature", "music", "design"],
            ModelType.SPECIALIZED: ["medicine", "law", "education", "research"]
        }
        return specializations.get(model_type, [])


# Создаем экземпляр конфигурации
config = Mozgach2Config()

if __name__ == "__main__":
    # Выводим информацию о конфигурации
    print(f"Проект: {config.PROJECT_NAME} v{config.VERSION}")
    print(f"Всего моделей: {config.TOTAL_MODELS}")
    print(f"Распределение по типам:")
    for model_type, count in config.MODEL_DISTRIBUTION.items():
        print(f"  {model_type.value}: {count}")
    print(f"Распределение по устройствам:")
    for device_class, count in config.DEVICE_DISTRIBUTION.items():
        print(f"  {device_class.value}: {count}")
    
    # Генерируем конфигурации моделей
    model_configs = config.get_model_configs()
    print(f"\nСгенерировано конфигураций: {len(model_configs)}")
    
    # Показываем примеры
    print(f"\nПримеры конфигураций:")
    for i, model_config in enumerate(model_configs[:3]):
        print(f"  {i+1}. {model_config.name} ({model_config.type.value}) - {model_config.device_class.value}")
