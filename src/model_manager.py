"""
Менеджер моделей mozgach108 - управление 108 моделями
"""

import asyncio
import logging
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass
from pathlib import Path
import json
import hashlib

from .models.model_factory import model_factory

logger = logging.getLogger(__name__)


@dataclass
class ModelInfo:
    """Информация о модели"""
    model_id: str
    domain: str
    size_mb: int
    load_priority: int
    quantum_signature: str
    is_loaded: bool = False
    load_time: float = 0.0


class ModelManager:
    """
    Менеджер для управления 108 квантово-запутанными моделями
    
    Ответственен за загрузку, выгрузку и оптимизацию моделей
    в зависимости от текущих потребностей системы.
    """
    
    def __init__(self, models_dir: str = "models"):
        """
        Инициализация менеджера моделей
        
        Args:
            models_dir: Директория с моделями
        """
        self.models_dir = Path(models_dir)
        self.loaded_models: Dict[str, Any] = {}
        self.model_registry: Dict[str, ModelInfo] = {}
        self.max_memory_mb = 8192  # 8GB по умолчанию
        self.current_memory_usage = 0
        
        # Критические модели, которые загружаются первыми
        self.critical_models = [
            "mozgach108_general_01",
            "mozgach108_quantum_core", 
            "mozgach108_spiritual_01",
            "mozgach108_programming_01"
        ]
        
        # Инициализируем фабрику моделей
        self.model_factory = model_factory
        self.model_factory.create_all_models()
        
        self._initialize_registry()
    
    def _initialize_registry(self):
        """Инициализация реестра всех 108 моделей"""
        logger.info("📋 Инициализация реестра моделей...")
        
        # Домены знаний и их модели
        domains = {
            "programming": 38,  # Программирование и разработка
            "spiritual": 58,    # Духовная сфера  
            "material": 60,     # Материальная сфера
            "quantum": 12       # Квантовые технологии
        }
        
        total_models = 0
        for domain, count in domains.items():
            for i in range(1, count + 1):
                model_id = f"mozgach108_{domain}_{i:02d}"
                quantum_sig = self._generate_quantum_signature(model_id, domain)
                
                self.model_registry[model_id] = ModelInfo(
                    model_id=model_id,
                    domain=domain,
                    size_mb=self._estimate_model_size(domain),
                    load_priority=self._calculate_priority(model_id, domain),
                    quantum_signature=quantum_sig
                )
                total_models += 1
        
        # Дополняем до 108 моделей специальными
        special_models = [
            ("mozgach108_dune_harekrishna", "spiritual", 1),
            ("mozgach108_earth_harekrishna", "spiritual", 1), 
            ("mozgach108_3d_printing", "material", 1),
            ("mozgach108_slang_2025", "material", 1),
            ("mozgach108_education_spheres", "material", 1),
            ("mozgach108_personal_satellite", "material", 1),
            ("mozgach108_classical_geometry", "material", 1),
            ("mozgach108_fibonacci_math", "material", 1),
            ("mozgach108_classical_physics", "material", 1),
            ("mozgach108_fibonacci_physics", "material", 1)
        ]
        
        for model_id, domain, priority in special_models:
            if total_models < 108:
                quantum_sig = self._generate_quantum_signature(model_id, domain)
                self.model_registry[model_id] = ModelInfo(
                    model_id=model_id,
                    domain=domain,
                    size_mb=self._estimate_model_size(domain),
                    load_priority=priority,
                    quantum_signature=quantum_sig
                )
                total_models += 1
        
        logger.info(f"✅ Зарегистрировано {total_models} моделей")
    
    def _generate_quantum_signature(self, model_id: str, domain: str) -> str:
        """Генерация квантовой подписи модели"""
        signature_data = f"{model_id}:{domain}:quantum_entangled"
        return hashlib.sha256(signature_data.encode()).hexdigest()[:16]
    
    def _estimate_model_size(self, domain: str) -> int:
        """Оценка размера модели в MB"""
        size_map = {
            "programming": 150,
            "spiritual": 120,
            "material": 130,
            "quantum": 200
        }
        return size_map.get(domain, 140)
    
    def _calculate_priority(self, model_id: str, domain: str) -> int:
        """Расчет приоритета загрузки модели"""
        if model_id in self.critical_models:
            return 1
        
        priority_map = {
            "quantum": 2,
            "programming": 3,
            "spiritual": 4,
            "material": 5
        }
        return priority_map.get(domain, 10)
    
    async def load_critical_models(self):
        """Загрузка критических моделей для базовой работы"""
        logger.info("🚀 Загрузка критических моделей...")
        
        for model_id in self.critical_models:
            if model_id in self.model_registry:
                await self.load_model(model_id)
        
        logger.info("✅ Критические модели загружены")
    
    async def load_model(self, model_id: str) -> bool:
        """
        Загрузка конкретной модели
        
        Args:
            model_id: Идентификатор модели
            
        Returns:
            True если модель успешно загружена
        """
        if model_id in self.loaded_models:
            logger.debug(f"📦 Модель {model_id} уже загружена")
            return True
        
        if model_id not in self.model_registry:
            logger.error(f"❌ Модель {model_id} не найдена в реестре")
            return False
        
        model_info = self.model_registry[model_id]
        
        # Проверка доступной памяти
        if self.current_memory_usage + model_info.size_mb > self.max_memory_mb:
            await self._free_memory(model_info.size_mb)
        
        try:
            logger.info(f"📥 Загрузка модели {model_id}...")
            
            # Симуляция загрузки модели (в реальной реализации здесь будет загрузка из файла)
            await asyncio.sleep(0.1)  # Имитация времени загрузки
            
            # Создание "модели" (заглушка для демонстрации)
            mock_model = {
                "model_id": model_id,
                "domain": model_info.domain,
                "quantum_signature": model_info.quantum_signature,
                "parameters": f"Параметры модели {model_id}",
                "loaded_at": asyncio.get_event_loop().time()
            }
            
            self.loaded_models[model_id] = mock_model
            model_info.is_loaded = True
            self.current_memory_usage += model_info.size_mb
            
            logger.info(f"✅ Модель {model_id} загружена ({model_info.size_mb}MB)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки модели {model_id}: {e}")
            return False
    
    async def unload_model(self, model_id: str) -> bool:
        """Выгрузка модели из памяти"""
        if model_id not in self.loaded_models:
            return True
        
        try:
            model_info = self.model_registry[model_id]
            del self.loaded_models[model_id]
            model_info.is_loaded = False
            self.current_memory_usage -= model_info.size_mb
            
            logger.info(f"📤 Модель {model_id} выгружена")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка выгрузки модели {model_id}: {e}")
            return False
    
    async def get_models_for_domains(self, domain_weights: Dict[str, float]) -> Dict[str, Any]:
        """
        Получение моделей для указанных доменов
        
        Args:
            domain_weights: Веса доменов знаний
            
        Returns:
            Словарь загруженных моделей
        """
        required_models = {}
        
        for domain, weight in domain_weights.items():
            if weight > 0.1:  # Загружаем модели только для значимых доменов
                domain_models = [
                    model_id for model_id, info in self.model_registry.items()
                    if info.domain == domain and info.load_priority <= 5
                ]
                
                # Загружаем топ-3 модели для каждого домена
                for model_id in sorted(domain_models, 
                                     key=lambda x: self.model_registry[x].load_priority)[:3]:
                    if await self.load_model(model_id):
                        required_models[model_id] = self.loaded_models[model_id]
        
        return required_models
    
    async def _free_memory(self, required_mb: int):
        """Освобождение памяти путем выгрузки моделей с низким приоритетом"""
        logger.info(f"🧹 Освобождение {required_mb}MB памяти...")
        
        # Сортируем модели по приоритету (высокий приоритет = низкое число)
        loaded_models_by_priority = sorted(
            [(model_id, self.model_registry[model_id]) 
             for model_id in self.loaded_models.keys()],
            key=lambda x: x[1].load_priority,
            reverse=True  # Выгружаем сначала модели с низким приоритетом
        )
        
        freed_memory = 0
        for model_id, model_info in loaded_models_by_priority:
            if model_id not in self.critical_models and freed_memory < required_mb:
                await self.unload_model(model_id)
                freed_memory += model_info.size_mb
    
    async def optimize_models(self):
        """Оптимизация загруженных моделей"""
        logger.info("🔧 Оптимизация моделей...")
        
        # Выгружаем неиспользуемые модели
        current_time = asyncio.get_event_loop().time()
        for model_id, model in list(self.loaded_models.items()):
            if model_id not in self.critical_models:
                # Выгружаем модели, которые не использовались более 5 минут
                if current_time - model["loaded_at"] > 300:
                    await self.unload_model(model_id)
        
        logger.info("✅ Оптимизация моделей завершена")
    
    async def unload_all_models(self):
        """Выгрузка всех моделей"""
        logger.info("📤 Выгрузка всех моделей...")
        
        for model_id in list(self.loaded_models.keys()):
            await self.unload_model(model_id)
        
        logger.info("✅ Все модели выгружены")
    
    def get_loaded_models_info(self) -> Dict[str, Dict[str, Any]]:
        """Получить информацию о загруженных моделях"""
        return {
            model_id: {
                "domain": self.model_registry[model_id].domain,
                "size_mb": self.model_registry[model_id].size_mb,
                "priority": self.model_registry[model_id].load_priority,
                "quantum_signature": self.model_registry[model_id].quantum_signature
            }
            for model_id in self.loaded_models.keys()
        }
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Получить статистику использования памяти"""
        return {
            "total_models": len(self.model_registry),
            "loaded_models": len(self.loaded_models),
            "memory_usage_mb": self.current_memory_usage,
            "memory_limit_mb": self.max_memory_mb,
            "memory_usage_percent": (self.current_memory_usage / self.max_memory_mb) * 100
        }
