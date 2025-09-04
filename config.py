"""
Конфигурация системы mozgach108
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import json

class Mozgach108Config:
    """Конфигурация системы mozgach108"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Инициализация конфигурации
        
        Args:
            config_path: Путь к файлу конфигурации
        """
        self.config_path = config_path or "config/mozgach108.json"
        self.config = self._load_default_config()
        
        if os.path.exists(self.config_path):
            self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации по умолчанию"""
        return {
            # Основные настройки системы
            "system": {
                "name": "mozgach108",
                "version": "1.0.0",
                "debug": False,
                "log_level": "INFO",
                "max_concurrent_queries": 10,
                "query_timeout": 30.0,
                "auto_optimize_interval": 3600,  # 1 час
            },
            
            # Настройки моделей
            "models": {
                "models_dir": "models",
                "max_memory_mb": 8192,  # 8GB
                "auto_load_critical": True,
                "load_on_demand": True,
                "cache_size": 100,
                "model_timeout": 60.0,
                "quantum_entanglement_strength": 0.8,
            },
            
            # Настройки квантовой запутанности
            "quantum": {
                "entanglement_strength": 0.8,
                "coherence_time": 1000.0,  # мс
                "decoherence_rate": 0.001,
                "measurement_basis": "computational",
                "quantum_noise_level": 0.1,
                "superposition_depth": 108,
            },
            
            # Настройки доменов знаний
            "knowledge_domains": {
                "auto_analyze_queries": True,
                "domain_threshold": 0.1,
                "max_domains_per_query": 5,
                "semantic_analysis_weight": 0.4,
                "keyword_analysis_weight": 0.6,
                "enable_domain_hints": True,
            },
            
            # Настройки квантовой памяти
            "quantum_memory": {
                "memory_dir": "quantum_memory",
                "max_entries": 10000,
                "context_window": 100,
                "cleanup_threshold": 0.1,
                "auto_save_interval": 300,  # 5 минут
                "enable_pattern_analysis": True,
                "memory_optimization_interval": 1800,  # 30 минут
            },
            
            # Настройки API
            "api": {
                "host": "0.0.0.0",
                "port": 8000,
                "workers": 4,
                "max_request_size": 10485760,  # 10MB
                "cors_enabled": True,
                "rate_limit": 100,  # запросов в минуту
                "enable_metrics": True,
            },
            
            # Настройки логирования
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "logs/mozgach108.log",
                "max_file_size": 10485760,  # 10MB
                "backup_count": 5,
                "enable_console": True,
                "enable_file": True,
            },
            
            # Настройки производительности
            "performance": {
                "enable_gpu": True,
                "gpu_memory_fraction": 0.8,
                "enable_mixed_precision": True,
                "batch_size": 32,
                "max_sequence_length": 2048,
                "enable_caching": True,
                "cache_ttl": 3600,  # 1 час
            },
            
            # Настройки безопасности
            "security": {
                "enable_encryption": True,
                "encryption_key": None,  # Будет сгенерирован автоматически
                "enable_authentication": False,
                "api_key_required": False,
                "allowed_origins": ["*"],
                "max_query_length": 10000,
            },
            
            # Настройки мониторинга
            "monitoring": {
                "enable_metrics": True,
                "metrics_port": 9090,
                "health_check_interval": 30,
                "enable_profiling": False,
                "profiling_output": "profiles/",
                "enable_tracing": False,
            },
            
            # Специальные настройки для духовной сферы
            "spiritual": {
                "enable_sanskrit_processing": True,
                "enable_mantra_recognition": True,
                "enable_chakra_analysis": True,
                "sacred_geometry_precision": 0.001,
                "enable_quantum_meditation": True,
            },
            
            # Настройки для материальной сферы
            "material": {
                "enable_scientific_notation": True,
                "enable_3d_visualization": True,
                "enable_fibonacci_analysis": True,
                "enable_classical_physics": True,
                "enable_modern_physics": True,
            },
            
            # Настройки для программирования
            "programming": {
                "enable_code_analysis": True,
                "enable_syntax_highlighting": True,
                "enable_auto_completion": True,
                "supported_languages": [
                    "python", "javascript", "java", "c++", "c#", "go", "rust",
                    "swift", "kotlin", "typescript", "php", "ruby", "scala"
                ],
                "enable_ai_assistance": True,
            },
            
            # Настройки для квантовых технологий
            "quantum_tech": {
                "enable_quantum_simulation": True,
                "quantum_circuit_depth": 1000,
                "enable_quantum_optimization": True,
                "quantum_annealing_enabled": True,
                "enable_quantum_machine_learning": True,
            }
        }
    
    def _load_config(self):
        """Загрузка конфигурации из файла"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
            
            # Рекурсивное обновление конфигурации
            self._update_config(self.config, file_config)
            
        except Exception as e:
            print(f"⚠️ Ошибка загрузки конфигурации: {e}")
            print("Используется конфигурация по умолчанию")
    
    def _update_config(self, base_config: Dict[str, Any], update_config: Dict[str, Any]):
        """Рекурсивное обновление конфигурации"""
        for key, value in update_config.items():
            if key in base_config and isinstance(base_config[key], dict) and isinstance(value, dict):
                self._update_config(base_config[key], value)
            else:
                base_config[key] = value
    
    def save_config(self):
        """Сохранение конфигурации в файл"""
        try:
            # Создаем директорию если не существует
            config_dir = Path(self.config_path).parent
            config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Ошибка сохранения конфигурации: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Получение значения конфигурации по пути
        
        Args:
            key_path: Путь к значению (например, "system.debug")
            default: Значение по умолчанию
            
        Returns:
            Значение конфигурации
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """
        Установка значения конфигурации
        
        Args:
            key_path: Путь к значению
            value: Новое значение
        """
        keys = key_path.split('.')
        config = self.config
        
        # Создаем вложенные словари если нужно
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Получение секции конфигурации"""
        return self.config.get(section, {})
    
    def update_section(self, section: str, updates: Dict[str, Any]):
        """Обновление секции конфигурации"""
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section].update(updates)
    
    def validate_config(self) -> bool:
        """Валидация конфигурации"""
        try:
            # Проверяем обязательные поля
            required_sections = ["system", "models", "quantum", "knowledge_domains"]
            for section in required_sections:
                if section not in self.config:
                    print(f"❌ Отсутствует обязательная секция: {section}")
                    return False
            
            # Проверяем значения
            if self.get("system.max_concurrent_queries", 0) <= 0:
                print("❌ max_concurrent_queries должно быть больше 0")
                return False
            
            if self.get("models.max_memory_mb", 0) <= 0:
                print("❌ max_memory_mb должно быть больше 0")
                return False
            
            if not 0 <= self.get("quantum.entanglement_strength", -1) <= 1:
                print("❌ entanglement_strength должно быть между 0 и 1")
                return False
            
            print("✅ Конфигурация валидна")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка валидации конфигурации: {e}")
            return False
    
    def get_environment_overrides(self):
        """Получение переопределений из переменных окружения"""
        overrides = {}
        
        # Системные настройки
        if os.getenv("MOZGACH108_DEBUG"):
            overrides["system.debug"] = os.getenv("MOZGACH108_DEBUG").lower() == "true"
        
        if os.getenv("MOZGACH108_LOG_LEVEL"):
            overrides["system.log_level"] = os.getenv("MOZGACH108_LOG_LEVEL")
        
        if os.getenv("MOZGACH108_MAX_MEMORY_MB"):
            overrides["models.max_memory_mb"] = int(os.getenv("MOZGACH108_MAX_MEMORY_MB"))
        
        # API настройки
        if os.getenv("MOZGACH108_HOST"):
            overrides["api.host"] = os.getenv("MOZGACH108_HOST")
        
        if os.getenv("MOZGACH108_PORT"):
            overrides["api.port"] = int(os.getenv("MOZGACH108_PORT"))
        
        # Применяем переопределения
        for key_path, value in overrides.items():
            self.set(key_path, value)
        
        return overrides
    
    def __str__(self) -> str:
        """Строковое представление конфигурации"""
        return f"Mozgach108Config(version={self.get('system.version')}, debug={self.get('system.debug')})"


# Глобальная конфигурация
config = Mozgach108Config()

# Применяем переопределения из переменных окружения
config.get_environment_overrides()
