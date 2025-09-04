"""
Фабрика моделей mozgach108 - создание всех 108 моделей
"""

import logging
from typing import Dict, List, Any, Optional
from .base_model import BaseModel
from .spiritual_models import create_spiritual_models
from .material_models import create_material_models
from .programming_models import create_programming_models
from .quantum_models import create_quantum_models

logger = logging.getLogger(__name__)


class ModelFactory:
    """
    Фабрика для создания и управления всеми 108 моделями mozgach108
    
    Создает и координирует работу всех специализированных моделей
    в системе квантово-запутанных языковых моделей.
    """
    
    def __init__(self):
        """Инициализация фабрики моделей"""
        self.models: Dict[str, BaseModel] = {}
        self.model_categories = {
            "spiritual": [],
            "material": [],
            "programming": [],
            "quantum": []
        }
        self.total_models = 0
        
        logger.info("🏭 Инициализация фабрики моделей mozgach108...")
    
    def create_all_models(self) -> Dict[str, BaseModel]:
        """
        Создание всех 108 моделей
        
        Returns:
            Словарь всех созданных моделей
        """
        logger.info("🚀 Создание всех 108 моделей mozgach108...")
        
        try:
            # Создаем духовные модели (58)
            logger.info("🕉️ Создание духовных моделей...")
            spiritual_models = create_spiritual_models()
            for model in spiritual_models:
                self.models[model.model_id] = model
                self.model_categories["spiritual"].append(model.model_id)
            
            # Создаем материальные модели (60)
            logger.info("🔬 Создание материальных моделей...")
            material_models = create_material_models()
            for model in material_models:
                self.models[model.model_id] = model
                self.model_categories["material"].append(model.model_id)
            
            # Создаем модели программирования (38)
            logger.info("💻 Создание моделей программирования...")
            programming_models = create_programming_models()
            for model in programming_models:
                self.models[model.model_id] = model
                self.model_categories["programming"].append(model.model_id)
            
            # Создаем квантовые модели (12)
            logger.info("🔮 Создание квантовых моделей...")
            quantum_models = create_quantum_models()
            for model in quantum_models:
                self.models[model.model_id] = model
                self.model_categories["quantum"].append(model.model_id)
            
            # Проверяем количество моделей
            self.total_models = len(self.models)
            
            if self.total_models == 108:
                logger.info(f"✅ Создано {self.total_models} моделей mozgach108")
                logger.info(f"📊 Распределение по категориям:")
                for category, model_ids in self.model_categories.items():
                    logger.info(f"   {category}: {len(model_ids)} моделей")
            else:
                logger.warning(f"⚠️ Создано {self.total_models} моделей вместо 108")
            
            return self.models
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания моделей: {e}")
            raise
    
    def get_model(self, model_id: str) -> Optional[BaseModel]:
        """
        Получение модели по ID
        
        Args:
            model_id: Идентификатор модели
            
        Returns:
            Модель или None если не найдена
        """
        return self.models.get(model_id)
    
    def get_models_by_category(self, category: str) -> List[BaseModel]:
        """
        Получение моделей по категории
        
        Args:
            category: Категория моделей
            
        Returns:
            Список моделей в категории
        """
        model_ids = self.model_categories.get(category, [])
        return [self.models[model_id] for model_id in model_ids if model_id in self.models]
    
    def get_models_by_domain(self, domain: str) -> List[BaseModel]:
        """
        Получение моделей по домену
        
        Args:
            domain: Домен знаний
            
        Returns:
            Список моделей в домене
        """
        return [model for model in self.models.values() if model.domain == domain]
    
    def get_model_statistics(self) -> Dict[str, Any]:
        """
        Получение статистики моделей
        
        Returns:
            Статистика по моделям
        """
        stats = {
            "total_models": len(self.models),
            "categories": {},
            "domains": {},
            "loaded_models": 0,
            "total_queries": 0,
            "total_processing_time": 0.0
        }
        
        # Статистика по категориям
        for category, model_ids in self.model_categories.items():
            stats["categories"][category] = len(model_ids)
        
        # Статистика по доменам
        for model in self.models.values():
            domain = model.domain
            if domain not in stats["domains"]:
                stats["domains"][domain] = 0
            stats["domains"][domain] += 1
            
            if model.is_loaded:
                stats["loaded_models"] += 1
            
            stats["total_queries"] += model.query_count
            stats["total_processing_time"] += model.total_processing_time
        
        # Средние значения
        if stats["total_models"] > 0:
            stats["average_queries_per_model"] = stats["total_queries"] / stats["total_models"]
            stats["average_processing_time_per_model"] = stats["total_processing_time"] / stats["total_models"]
        
        return stats
    
    def get_model_capabilities_summary(self) -> Dict[str, Any]:
        """
        Получение сводки возможностей моделей
        
        Returns:
            Сводка возможностей
        """
        capabilities = {
            "total_languages": set(),
            "total_specializations": set(),
            "max_context_length": 0,
            "total_memory_requirements": 0,
            "quantum_signatures": []
        }
        
        for model in self.models.values():
            model_caps = model.get_capabilities()
            
            # Языки
            capabilities["total_languages"].update(model_caps.supported_languages)
            
            # Специализации
            capabilities["total_specializations"].update(model_caps.specializations)
            
            # Максимальная длина контекста
            capabilities["max_context_length"] = max(
                capabilities["max_context_length"], 
                model_caps.max_context_length
            )
            
            # Требования к памяти
            capabilities["total_memory_requirements"] += model_caps.memory_requirements_mb
            
            # Квантовые подписи
            capabilities["quantum_signatures"].append(model_caps.quantum_signature)
        
        # Преобразуем множества в списки для JSON сериализации
        capabilities["total_languages"] = list(capabilities["total_languages"])
        capabilities["total_specializations"] = list(capabilities["total_specializations"])
        
        return capabilities
    
    def find_models_for_query(self, query: str, domain_hints: Optional[List[str]] = None) -> List[BaseModel]:
        """
        Поиск подходящих моделей для запроса
        
        Args:
            query: Запрос пользователя
            domain_hints: Подсказки о доменах
            
        Returns:
            Список подходящих моделей
        """
        query_lower = query.lower()
        suitable_models = []
        
        # Если есть подсказки о доменах, используем их
        if domain_hints:
            for domain in domain_hints:
                domain_models = self.get_models_by_domain(domain)
                suitable_models.extend(domain_models)
        else:
            # Анализируем запрос для определения подходящих моделей
            for model in self.models.values():
                model_caps = model.get_capabilities()
                
                # Проверяем специализации модели
                for specialization in model_caps.specializations:
                    if specialization.lower() in query_lower:
                        suitable_models.append(model)
                        break
        
        # Если не нашли подходящих моделей, возвращаем общие модели
        if not suitable_models:
            # Возвращаем по одной модели из каждой категории
            for category in ["spiritual", "material", "programming", "quantum"]:
                category_models = self.get_models_by_category(category)
                if category_models:
                    suitable_models.append(category_models[0])
        
        return suitable_models[:5]  # Ограничиваем до 5 моделей
    
    def get_model_performance_ranking(self) -> List[Dict[str, Any]]:
        """
        Получение рейтинга производительности моделей
        
        Returns:
            Список моделей, отсортированный по производительности
        """
        model_performance = []
        
        for model in self.models.values():
            if model.query_count > 0:
                avg_processing_time = model.total_processing_time / model.query_count
                performance_score = model.query_count / (avg_processing_time + 0.001)  # Избегаем деления на 0
                
                model_performance.append({
                    "model_id": model.model_id,
                    "domain": model.domain,
                    "query_count": model.query_count,
                    "average_processing_time": avg_processing_time,
                    "performance_score": performance_score,
                    "is_loaded": model.is_loaded
                })
        
        # Сортируем по производительности (больше запросов, меньше времени)
        model_performance.sort(key=lambda x: x["performance_score"], reverse=True)
        
        return model_performance
    
    def optimize_model_selection(self, query: str) -> List[BaseModel]:
        """
        Оптимизированный выбор моделей для запроса
        
        Args:
            query: Запрос пользователя
            
        Returns:
            Список оптимальных моделей
        """
        # Получаем подходящие модели
        suitable_models = self.find_models_for_query(query)
        
        # Получаем рейтинг производительности
        performance_ranking = self.get_model_performance_ranking()
        performance_dict = {item["model_id"]: item["performance_score"] for item in performance_ranking}
        
        # Сортируем подходящие модели по производительности
        suitable_models.sort(
            key=lambda model: performance_dict.get(model.model_id, 0), 
            reverse=True
        )
        
        # Возвращаем топ-3 модели
        return suitable_models[:3]
    
    def get_model_health_status(self) -> Dict[str, Any]:
        """
        Получение статуса здоровья моделей
        
        Returns:
            Статус здоровья моделей
        """
        health_status = {
            "healthy_models": 0,
            "warning_models": 0,
            "error_models": 0,
            "total_models": len(self.models),
            "model_details": []
        }
        
        for model in self.models.values():
            model_health = {
                "model_id": model.model_id,
                "domain": model.domain,
                "is_loaded": model.is_loaded,
                "query_count": model.query_count,
                "status": "healthy"
            }
            
            # Определяем статус модели
            if not model.is_loaded:
                model_health["status"] = "error"
                health_status["error_models"] += 1
            elif model.query_count == 0:
                model_health["status"] = "warning"
                health_status["warning_models"] += 1
            else:
                health_status["healthy_models"] += 1
            
            health_status["model_details"].append(model_health)
        
        return health_status
    
    def __str__(self) -> str:
        """Строковое представление фабрики"""
        return f"ModelFactory(total_models={self.total_models}, categories={len(self.model_categories)})"
    
    def __repr__(self) -> str:
        """Представление фабрики для отладки"""
        return (f"ModelFactory(models={len(self.models)}, "
                f"spiritual={len(self.model_categories['spiritual'])}, "
                f"material={len(self.model_categories['material'])}, "
                f"programming={len(self.model_categories['programming'])}, "
                f"quantum={len(self.model_categories['quantum'])})")


# Глобальная фабрика моделей
model_factory = ModelFactory()
