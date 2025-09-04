"""
Главная система mozgach108 - ядро квантово-запутанных моделей
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime

from .model_manager import ModelManager
from .quantum_entanglement import QuantumEntanglement
from .knowledge_domains import KnowledgeDomains
from .quantum_memory import QuantumMemory

logger = logging.getLogger(__name__)


@dataclass
class QueryResponse:
    """Ответ системы на запрос"""
    content: str
    confidence: float
    domain_weights: Dict[str, float]
    quantum_state: Dict[str, Any]
    processing_time: float
    timestamp: datetime


class Mozgach108System:
    """
    Главная система mozgach108
    
    Координирует работу 108 квантово-запутанных моделей для получения
    оптимальных ответов на запросы пользователя.
    """
    
    def __init__(self, auto_load_models: bool = True, config_path: Optional[str] = None):
        """
        Инициализация системы mozgach108
        
        Args:
            auto_load_models: Автоматически загружать критические модели
            config_path: Путь к файлу конфигурации
        """
        logger.info("🚀 Инициализация системы mozgach108...")
        
        self.model_manager = ModelManager()
        self.quantum_entanglement = QuantumEntanglement()
        self.knowledge_domains = KnowledgeDomains()
        self.quantum_memory = QuantumMemory()
        
        self._initialized = False
        self._auto_load = auto_load_models
        self._config_path = config_path
        
        # Статистика работы системы
        self._query_count = 0
        self._total_processing_time = 0.0
        self._success_rate = 0.0
        
        if auto_load_models:
            asyncio.create_task(self._initialize_system())
    
    async def _initialize_system(self):
        """Инициализация всех компонентов системы"""
        try:
            logger.info("🔧 Загрузка критических моделей...")
            await self.model_manager.load_critical_models()
            
            logger.info("🔮 Инициализация квантовой запутанности...")
            await self.quantum_entanglement.initialize()
            
            logger.info("📚 Загрузка доменов знаний...")
            await self.knowledge_domains.load_domains()
            
            logger.info("🧠 Инициализация квантовой памяти...")
            await self.quantum_memory.initialize()
            
            self._initialized = True
            logger.info("✅ Система mozgach108 готова к работе!")
            
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации системы: {e}")
            raise
    
    async def query(self, prompt: str, domain_hint: Optional[str] = None) -> QueryResponse:
        """
        Основной метод для получения ответа от системы
        
        Args:
            prompt: Запрос пользователя
            domain_hint: Подсказка о предполагаемом домене знаний
            
        Returns:
            QueryResponse: Ответ системы с метаданными
        """
        if not self._initialized:
            await self._initialize_system()
        
        start_time = datetime.now()
        self._query_count += 1
        
        try:
            logger.info(f"🔍 Обработка запроса #{self._query_count}: {prompt[:50]}...")
            
            # Определение релевантных доменов знаний
            relevant_domains = await self.knowledge_domains.analyze_query(prompt, domain_hint)
            logger.debug(f"📊 Релевантные домены: {list(relevant_domains.keys())}")
            
            # Загрузка необходимых моделей
            required_models = await self.model_manager.get_models_for_domains(relevant_domains)
            
            # Квантовая обработка запроса
            quantum_response = await self.quantum_entanglement.process_query(
                prompt, required_models, relevant_domains
            )
            
            # Обогащение ответа через квантовую память
            enhanced_response = await self.quantum_memory.enhance_response(
                quantum_response, prompt
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            self._total_processing_time += processing_time
            
            response = QueryResponse(
                content=enhanced_response["content"],
                confidence=enhanced_response["confidence"],
                domain_weights=relevant_domains,
                quantum_state=quantum_response["quantum_state"],
                processing_time=processing_time,
                timestamp=datetime.now()
            )
            
            logger.info(f"✅ Запрос обработан за {processing_time:.2f}с")
            return response
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки запроса: {e}")
            raise
    
    async def batch_query(self, prompts: List[str]) -> List[QueryResponse]:
        """
        Пакетная обработка нескольких запросов
        
        Args:
            prompts: Список запросов для обработки
            
        Returns:
            Список ответов системы
        """
        logger.info(f"📦 Пакетная обработка {len(prompts)} запросов...")
        
        tasks = [self.query(prompt) for prompt in prompts]
        responses = await asyncio.gather(*tasks)
        
        logger.info(f"✅ Пакетная обработка завершена")
        return responses
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Получить статистику работы системы"""
        avg_processing_time = (
            self._total_processing_time / self._query_count 
            if self._query_count > 0 else 0
        )
        
        return {
            "total_queries": self._query_count,
            "total_processing_time": self._total_processing_time,
            "average_processing_time": avg_processing_time,
            "success_rate": self._success_rate,
            "loaded_models": len(self.model_manager.loaded_models),
            "active_domains": len(self.knowledge_domains.active_domains),
            "quantum_entanglement_strength": self.quantum_entanglement.entanglement_strength,
            "memory_usage_mb": self.quantum_memory.get_memory_usage()
        }
    
    async def optimize_system(self):
        """Оптимизация системы для улучшения производительности"""
        logger.info("🔧 Запуск оптимизации системы...")
        
        # Оптимизация загруженных моделей
        await self.model_manager.optimize_models()
        
        # Оптимизация квантовой запутанности
        await self.quantum_entanglement.optimize()
        
        # Очистка квантовой памяти
        await self.quantum_memory.cleanup()
        
        logger.info("✅ Оптимизация системы завершена")
    
    async def shutdown(self):
        """Корректное завершение работы системы"""
        logger.info("🛑 Завершение работы системы mozgach108...")
        
        await self.model_manager.unload_all_models()
        await self.quantum_entanglement.shutdown()
        await self.quantum_memory.save_state()
        
        logger.info("✅ Система mozgach108 корректно завершила работу")


# Глобальная инстанция системы для удобного использования
mozgach = Mozgach108System()
