"""
Базовый класс для всех 108 моделей mozgach108
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json

logger = logging.getLogger(__name__)


@dataclass
class ModelResponse:
    """Ответ модели"""
    content: str
    confidence: float
    domain: str
    model_id: str
    processing_time: float
    metadata: Dict[str, Any]
    timestamp: datetime


@dataclass
class ModelCapabilities:
    """Возможности модели"""
    max_context_length: int
    supported_languages: List[str]
    specializations: List[str]
    quantum_signature: str
    memory_requirements_mb: int


class BaseModel(ABC):
    """
    Базовый класс для всех 108 моделей mozgach108
    
    Определяет общий интерфейс и функциональность
    для всех специализированных моделей системы.
    """
    
    def __init__(self, model_id: str, domain: str, capabilities: ModelCapabilities):
        """
        Инициализация базовой модели
        
        Args:
            model_id: Уникальный идентификатор модели
            domain: Домен знаний модели
            capabilities: Возможности модели
        """
        self.model_id = model_id
        self.domain = domain
        self.capabilities = capabilities
        self.is_loaded = False
        self.load_time = 0.0
        self.query_count = 0
        self.total_processing_time = 0.0
        
        # Квантовые характеристики
        self.quantum_signature = capabilities.quantum_signature
        self.entanglement_strength = 0.0
        self.coherence_level = 1.0
        
        # Кэш для оптимизации
        self.response_cache: Dict[str, ModelResponse] = {}
        self.cache_size_limit = 100
        
        logger.debug(f"🔧 Инициализация модели {model_id}")
    
    @abstractmethod
    async def load_model(self) -> bool:
        """
        Загрузка модели
        
        Returns:
            True если модель успешно загружена
        """
        pass
    
    @abstractmethod
    async def unload_model(self) -> bool:
        """
        Выгрузка модели
        
        Returns:
            True если модель успешно выгружена
        """
        pass
    
    @abstractmethod
    async def process_query(self, query: str, context: Optional[str] = None) -> ModelResponse:
        """
        Обработка запроса
        
        Args:
            query: Запрос пользователя
            context: Дополнительный контекст
            
        Returns:
            Ответ модели
        """
        pass
    
    async def initialize(self) -> bool:
        """Инициализация модели"""
        try:
            logger.info(f"🚀 Инициализация модели {self.model_id}...")
            
            # Загружаем модель
            if not await self.load_model():
                logger.error(f"❌ Ошибка загрузки модели {self.model_id}")
                return False
            
            # Инициализируем квантовые характеристики
            await self._initialize_quantum_properties()
            
            # Настраиваем кэш
            await self._setup_cache()
            
            self.is_loaded = True
            self.load_time = asyncio.get_event_loop().time()
            
            logger.info(f"✅ Модель {self.model_id} инициализирована")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации модели {self.model_id}: {e}")
            return False
    
    async def _initialize_quantum_properties(self):
        """Инициализация квантовых свойств модели"""
        # Генерируем квантовую подпись на основе характеристик модели
        signature_data = f"{self.model_id}:{self.domain}:{self.capabilities.specializations}"
        self.quantum_signature = hashlib.sha256(signature_data.encode()).hexdigest()[:16]
        
        # Устанавливаем начальную силу запутанности
        self.entanglement_strength = 0.5 + (hash(self.model_id) % 50) / 100.0
        
        # Устанавливаем уровень когерентности
        self.coherence_level = 0.8 + (hash(self.domain) % 20) / 100.0
    
    async def _setup_cache(self):
        """Настройка кэша модели"""
        self.response_cache.clear()
        logger.debug(f"📦 Кэш настроен для модели {self.model_id}")
    
    async def query(self, query: str, context: Optional[str] = None, 
                   use_cache: bool = True) -> ModelResponse:
        """
        Выполнение запроса к модели
        
        Args:
            query: Запрос пользователя
            context: Дополнительный контекст
            use_cache: Использовать кэш
            
        Returns:
            Ответ модели
        """
        if not self.is_loaded:
            raise RuntimeError(f"Модель {self.model_id} не загружена")
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Проверяем кэш
            cache_key = self._generate_cache_key(query, context)
            if use_cache and cache_key in self.response_cache:
                cached_response = self.response_cache[cache_key]
                logger.debug(f"📦 Использован кэш для модели {self.model_id}")
                return cached_response
            
            # Обрабатываем запрос
            response = await self.process_query(query, context)
            
            # Обновляем статистику
            self.query_count += 1
            processing_time = asyncio.get_event_loop().time() - start_time
            self.total_processing_time += processing_time
            
            # Сохраняем в кэш
            if use_cache and len(self.response_cache) < self.cache_size_limit:
                self.response_cache[cache_key] = response
            
            logger.debug(f"✅ Запрос обработан моделью {self.model_id} за {processing_time:.3f}с")
            return response
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки запроса моделью {self.model_id}: {e}")
            raise
    
    def _generate_cache_key(self, query: str, context: Optional[str] = None) -> str:
        """Генерация ключа кэша"""
        cache_data = f"{query}:{context or ''}:{self.model_id}"
        return hashlib.md5(cache_data.encode()).hexdigest()
    
    async def optimize(self):
        """Оптимизация модели"""
        logger.info(f"🔧 Оптимизация модели {self.model_id}...")
        
        try:
            # Очищаем старые записи кэша
            await self._cleanup_cache()
            
            # Оптимизируем квантовые свойства
            await self._optimize_quantum_properties()
            
            logger.info(f"✅ Модель {self.model_id} оптимизирована")
            
        except Exception as e:
            logger.error(f"❌ Ошибка оптимизации модели {self.model_id}: {e}")
    
    async def _cleanup_cache(self):
        """Очистка кэша"""
        if len(self.response_cache) > self.cache_size_limit * 0.8:
            # Удаляем самые старые записи
            cache_items = list(self.response_cache.items())
            cache_items.sort(key=lambda x: x[1].timestamp)
            
            # Оставляем только 80% записей
            keep_count = int(self.cache_size_limit * 0.8)
            self.response_cache = dict(cache_items[-keep_count:])
            
            logger.debug(f"🧹 Кэш очищен для модели {self.model_id}")
    
    async def _optimize_quantum_properties(self):
        """Оптимизация квантовых свойств"""
        # Восстанавливаем когерентность
        self.coherence_level = min(1.0, self.coherence_level + 0.1)
        
        # Корректируем силу запутанности
        if self.query_count > 0:
            avg_processing_time = self.total_processing_time / self.query_count
            # Увеличиваем запутанность для быстрых моделей
            if avg_processing_time < 1.0:
                self.entanglement_strength = min(1.0, self.entanglement_strength + 0.05)
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику модели"""
        avg_processing_time = (
            self.total_processing_time / self.query_count 
            if self.query_count > 0 else 0
        )
        
        return {
            "model_id": self.model_id,
            "domain": self.domain,
            "is_loaded": self.is_loaded,
            "load_time": self.load_time,
            "query_count": self.query_count,
            "total_processing_time": self.total_processing_time,
            "average_processing_time": avg_processing_time,
            "cache_size": len(self.response_cache),
            "quantum_signature": self.quantum_signature,
            "entanglement_strength": self.entanglement_strength,
            "coherence_level": self.coherence_level,
            "capabilities": {
                "max_context_length": self.capabilities.max_context_length,
                "supported_languages": self.capabilities.supported_languages,
                "specializations": self.capabilities.specializations,
                "memory_requirements_mb": self.capabilities.memory_requirements_mb
            }
        }
    
    def get_capabilities(self) -> ModelCapabilities:
        """Получить возможности модели"""
        return self.capabilities
    
    async def shutdown(self):
        """Корректное завершение работы модели"""
        logger.info(f"🛑 Завершение работы модели {self.model_id}...")
        
        try:
            # Выгружаем модель
            await self.unload_model()
            
            # Очищаем кэш
            self.response_cache.clear()
            
            # Сбрасываем статистику
            self.is_loaded = False
            self.query_count = 0
            self.total_processing_time = 0.0
            
            logger.info(f"✅ Модель {self.model_id} завершила работу")
            
        except Exception as e:
            logger.error(f"❌ Ошибка завершения работы модели {self.model_id}: {e}")
    
    def __str__(self) -> str:
        """Строковое представление модели"""
        return f"Model({self.model_id}, domain={self.domain}, loaded={self.is_loaded})"
    
    def __repr__(self) -> str:
        """Представление модели для отладки"""
        return (f"BaseModel(model_id='{self.model_id}', domain='{self.domain}', "
                f"is_loaded={self.is_loaded}, query_count={self.query_count})")
