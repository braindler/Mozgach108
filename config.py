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
    knowledge_domain: str  # Домен знаний для данной модели


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
    
    # Языки РФ+СНГ
    RF_CIS_LANGUAGES = [
        "ru",  # Русский (Россия)
        "be",  # Белорусский (Беларусь)
        "kk",  # Казахский (Казахстан)
        "uk",  # Украинский (Украина)
        "uz",  # Узбекский (Узбекистан)
        "ky",  # Кыргызский (Кыргызстан)
        "tg",  # Таджикский (Таджикистан)
        "tk",  # Туркменский (Туркменистан)
        "az",  # Азербайджанский (Азербайджан)
        "hy",  # Армянский (Армения)
        "ka",  # Грузинский (Грузия)
        "mo",  # Молдавский (Молдова)
        "en",  # Английский (международный)
        "de",  # Немецкий (для взаимодействия с ЕС)
        "zh",  # Китайский (для взаимодействия с Китаем)
        "ar"   # Арабский (для взаимодействия с Ближним Востоком)
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
    
    # 108 доменов знаний
    KNOWLEDGE_DOMAINS = [
        # Общие знания (16 доменов)
        "general_knowledge", "common_sense", "everyday_life", "social_norms",
        "human_behavior", "communication", "relationships", "family",
        "education", "learning", "memory", "cognition", "psychology",
        "sociology", "anthropology", "cultural_studies",
        
        # Технические знания (20 доменов)
        "mathematics", "physics", "chemistry", "biology", "astronomy",
        "geology", "meteorology", "oceanography", "computer_science",
        "engineering", "architecture", "robotics", "artificial_intelligence",
        "data_science", "cybersecurity", "blockchain", "quantum_computing",
        "nanotechnology", "biotechnology", "renewable_energy",
        
        # Духовные знания (18 доменов)
        "buddhism_philosophy", "hinduism_philosophy", "islam_philosophy",
        "christianity_philosophy", "judaism_philosophy", "taoism_philosophy",
        "confucianism_philosophy", "zen_philosophy", "sufism_philosophy",
        "kabbalah_philosophy", "meditation_practices", "yoga_practices",
        "mindfulness", "spiritual_healing", "energy_work", "chakras",
        "astral_projection", "consciousness_studies",
        
        # Разговорные знания (22 домена)
        "russian_culture", "belarusian_culture", "kazakh_culture",
        "ukrainian_culture", "uzbek_culture", "kyrgyz_culture",
        "tajik_culture", "turkmen_culture", "azerbaijani_culture",
        "armenian_culture", "georgian_culture", "moldovan_culture",
        "slavic_languages", "turkic_languages", "caucasian_languages",
        "baltic_languages", "eastern_european_culture", "central_asian_culture",
        "eurasian_culture", "post_soviet_culture", "multicultural_dialogue",
        "cross_cultural_communication",
        
        # Бизнес знания (12 доменов)
        "economics", "finance", "accounting", "marketing", "management",
        "strategy", "operations", "human_resources", "entrepreneurship",
        "investment", "international_trade", "business_ethics",
        
        # Творческие знания (12 доменов)
        "visual_arts", "music", "literature", "theater", "cinema",
        "dance", "design", "photography", "sculpture", "architecture",
        "creative_writing", "art_history",
        
        # Специализированные знания (8 доменов)
        "medicine", "law", "military", "agriculture", "transportation",
        "tourism", "sports", "entertainment"
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
                
                # Определяем домен знаний для данной модели
                knowledge_domain = cls.KNOWLEDGE_DOMAINS[model_id]
                
                config = ModelConfig(
                    name=f"mozgach2_{model_type.value}_{i+1:02d}",
                    type=model_type,
                    device_class=device_class,
                    max_context_length=cls.MAX_CONTEXT_LENGTH,
                    model_size_mb=cls._get_model_size(model_type, device_class),
                    languages=cls._get_languages_for_model(model_type),
                    specializations=cls._get_specializations_for_model(model_type),
                    quantum_entanglement_group=quantum_group,
                    knowledge_domain=knowledge_domain
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
            return cls.RF_CIS_LANGUAGES
        elif model_type == ModelType.SPIRITUAL:
            return ["ru", "en", "hi", "zh", "sa"]  # Основные языки духовных текстов
        else:
            return ["ru", "en"]  # Базовые языки
    
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
    print(f"Доменов знаний: {len(config.KNOWLEDGE_DOMAINS)}")
    
    # Генерируем конфигурации моделей
    model_configs = config.get_model_configs()
    print(f"\nСгенерировано конфигураций: {len(model_configs)}")
    
    # Показываем примеры
    print(f"\nПримеры конфигураций:")
    for i, model_config in enumerate(model_configs[:3]):
        print(f"  {i+1}. {model_config.name} ({model_config.type.value}) - {model_config.device_class.value}")
        print(f"     Домен знаний: {model_config.knowledge_domain}")
