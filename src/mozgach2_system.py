"""
Основная система Mozgach2
Управление 108 квантово-запутанными языковыми моделями
Модели обучались параллельно на едином датасете, разбитом на 108 различных доменов знаний
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import time
import psutil
import GPUtil

from ..config import (
    Mozgach2Config, ModelConfig, ModelType, DeviceClass, config
)


@dataclass
class QueryResult:
    """Результат запроса к системе"""
    response: str
    model_used: str
    confidence: float
    processing_time: float
    model_type: ModelType
    quantum_group: int
    knowledge_domain: str  # Домен знаний, использованный для ответа


@dataclass
class SystemStatus:
    """Статус системы Mozgach2"""
    total_models: int
    loaded_models: int
    available_memory_gb: float
    gpu_memory_gb: float
    system_load: float
    active_queries: int
    cache_hit_rate: float


class ModelManager:
    """Менеджер моделей для загрузки и выгрузки"""
    
    def __init__(self):
        self.loaded_models: Dict[str, Any] = {}
        self.model_configs = config.get_model_configs()
        self.model_cache = {}
        self.logger = logging.getLogger(__name__)
    
    async def load_model(self, model_name: str) -> bool:
        """Загружает модель в память"""
        try:
            if model_name in self.loaded_models:
                return True
            
            # Находим конфигурацию модели
            model_config = next(
                (cfg for cfg in self.model_configs if cfg.name == model_name), 
                None
            )
            
            if not model_config:
                self.logger.error(f"Модель {model_name} не найдена в конфигурации")
                return False
            
            # Проверяем доступную память
            if not self._check_memory_availability(model_config):
                self.logger.warning(f"Недостаточно памяти для загрузки модели {model_name}")
                return False
            
            # Имитируем загрузку модели (в реальности здесь будет загрузка PyTorch/ONNX)
            self.loaded_models[model_name] = {
                "config": model_config,
                "loaded_at": time.time(),
                "memory_usage": model_config.model_size_mb / 1024,  # GB
                "status": "loaded",
                "knowledge_domain": model_config.knowledge_domain
            }
            
            self.logger.info(f"Модель {model_name} успешно загружена (домен: {model_config.knowledge_domain})")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке модели {model_name}: {e}")
            return False
    
    async def unload_model(self, model_name: str) -> bool:
        """Выгружает модель из памяти"""
        try:
            if model_name in self.loaded_models:
                model_info = self.loaded_models[model_name]
                memory_freed = model_info["memory_usage"]
                
                del self.loaded_models[model_name]
                
                self.logger.info(f"Модель {model_name} выгружена, освобождено {memory_freed:.2f} GB")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Ошибка при выгрузке модели {model_name}: {e}")
            return False
    
    def _check_memory_availability(self, model_config: ModelConfig) -> bool:
        """Проверяет доступность памяти для загрузки модели"""
        available_memory = psutil.virtual_memory().available / (1024**3)  # GB
        required_memory = model_config.model_size_mb / 1024  # GB
        
        # Оставляем запас в 20%
        return available_memory > required_memory * 1.2
    
    def get_loaded_models_count(self) -> int:
        """Возвращает количество загруженных моделей"""
        return len(self.loaded_models)
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """Возвращает информацию о модели"""
        return self.loaded_models.get(model_name)


class QuantumEntanglementManager:
    """Менеджер квантовой запутанности моделей"""
    
    def __init__(self):
        self.entanglement_groups: Dict[int, List[str]] = {}
        self.model_configs = config.get_model_configs()
        self.logger = logging.getLogger(__name__)
        self._build_entanglement_groups()
    
    def _build_entanglement_groups(self):
        """Строит группы квантовой запутанности"""
        for model_config in self.model_configs:
            group_id = model_config.quantum_entanglement_group
            if group_id not in self.entanglement_groups:
                self.entanglement_groups[group_id] = []
            self.entanglement_groups[group_id].append(model_config.name)
    
    def get_entangled_models(self, model_name: str) -> List[str]:
        """Возвращает список запутанных с данной моделью моделей"""
        for group_id, models in self.entanglement_groups.items():
            if model_name in models:
                return [m for m in models if m != model_name]
        return []
    
    def get_optimal_model_group(self, query: str, query_type: ModelType) -> List[str]:
        """Возвращает оптимальную группу моделей для запроса"""
        # Находим группу с наибольшим количеством моделей нужного типа
        best_group = None
        max_count = 0
        
        for group_id, models in self.entanglement_groups.items():
            count = sum(1 for m in models if self._get_model_type_by_name(m) == query_type)
            if count > max_count:
                max_count = count
                best_group = group_id
        
        return self.entanglement_groups.get(best_group, []) if best_group else []
    
    def _get_model_type_by_name(self, model_name: str) -> Optional[ModelType]:
        """Получает тип модели по имени"""
        for model_config in self.model_configs:
            if model_config.name == model_name:
                return model_config.type
        return None


class QueryRouter:
    """Маршрутизатор запросов к оптимальным моделям по доменам знаний"""
    
    def __init__(self, model_manager: ModelManager, quantum_manager: QuantumEntanglementManager):
        self.model_manager = model_manager
        self.quantum_manager = quantum_manager
        self.logger = logging.getLogger(__name__)
        
        # Классификатор типов запросов по доменам знаний
        self.query_classifiers = {
            ModelType.TECHNICAL: [
                "как работает", "технология", "наука", "инженерия", "математика",
                "физика", "химия", "биология", "программирование", "алгоритм",
                "астрономия", "геология", "робототехника", "искусственный интеллект"
            ],
            ModelType.SPIRITUAL: [
                "душа", "бог", "медитация", "философия", "религия", "буддизм",
                "индуизм", "ислам", "христианство", "карма", "реинкарнация",
                "дзен", "суфизм", "каббала", "чакры", "энергетическая работа"
            ],
            ModelType.BUSINESS: [
                "бизнес", "экономика", "финансы", "инвестиции", "стратегия",
                "маркетинг", "менеджмент", "прибыль", "рынок", "конкуренция",
                "бухгалтерия", "операции", "человеческие ресурсы", "предпринимательство"
            ],
            ModelType.CREATIVE: [
                "искусство", "творчество", "поэзия", "музыка", "живопись",
                "дизайн", "вдохновение", "креативность", "эстетика",
                "театр", "кино", "танец", "фотография", "скульптура"
            ],
            ModelType.CONVERSATIONAL: [
                "привет", "как дела", "поговорим", "расскажи", "история",
                "анекдот", "шутка", "разговор", "общение", "культура",
                "традиции", "обычаи", "язык", "диалект", "идиомы"
            ]
        }
        
        # Классификатор доменов знаний
        self.domain_classifiers = {
            # Технические домены
            "mathematics": ["математика", "числа", "формула", "уравнение", "геометрия"],
            "physics": ["физика", "механика", "электричество", "магнетизм", "квантовая"],
            "computer_science": ["программирование", "алгоритм", "код", "программа", "компьютер"],
            "engineering": ["инженерия", "конструкция", "проект", "технический", "механизм"],
            
            # Духовные домены
            "buddhism_philosophy": ["буддизм", "дхарма", "сансара", "нирвана", "карма"],
            "meditation_practices": ["медитация", "дыхание", "осознанность", "дзен", "самадхи"],
            "spiritual_healing": ["исцеление", "энергия", "чакры", "аура", "биоэнергетика"],
            
            # Культурные домены
            "russian_culture": ["русская культура", "традиции", "обычаи", "фольклор", "русский"],
            "slavic_languages": ["славянские языки", "славянская культура", "славяне"],
            "eurasian_culture": ["евразийская культура", "евразия", "евразийство"],
            
            # Бизнес домены
            "economics": ["экономика", "рынок", "спрос", "предложение", "цена"],
            "finance": ["финансы", "деньги", "банк", "кредит", "инвестиции"],
            
            # Творческие домены
            "visual_arts": ["изобразительное искусство", "живопись", "рисунок", "картина"],
            "music": ["музыка", "мелодия", "ритм", "гармония", "инструмент"],
            "literature": ["литература", "книга", "роман", "поэзия", "проза"]
        }
    
    def classify_query(self, query: str) -> ModelType:
        """Классифицирует тип запроса по доменам знаний"""
        query_lower = query.lower()
        
        # Подсчитываем баллы для каждого типа
        scores = {model_type: 0 for model_type in ModelType}
        
        for model_type, keywords in self.query_classifiers.items():
            for keyword in keywords:
                if keyword in query_lower:
                    scores[model_type] += 1
        
        # Если нет явных признаков, используем общий тип
        if max(scores.values()) == 0:
            return ModelType.GENERAL
        
        return max(scores, key=scores.get)
    
    def classify_knowledge_domain(self, query: str) -> str:
        """Классифицирует запрос по конкретному домену знаний"""
        query_lower = query.lower()
        
        # Подсчитываем баллы для каждого домена
        domain_scores = {}
        
        for domain, keywords in self.domain_classifiers.items():
            score = 0
            for keyword in keywords:
                if keyword in query_lower:
                    score += 1
            if score > 0:
                domain_scores[domain] = score
        
        # Возвращаем домен с наивысшим баллом
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        
        # Если не удалось определить, возвращаем общий домен
        return "general_knowledge"
    
    def select_optimal_model(self, query: str, query_type: ModelType) -> str:
        """Выбирает оптимальную модель для запроса по домену знаний"""
        # Определяем конкретный домен знаний
        knowledge_domain = self.classify_knowledge_domain(query)
        
        # Получаем группу запутанных моделей
        optimal_group = self.quantum_manager.get_optimal_model_group(query, query_type)
        
        # Ищем модель с наиболее подходящим доменом знаний
        best_model = None
        best_domain_match = 0
        
        for model_name in optimal_group:
            model_config = next(
                (cfg for cfg in config.get_model_configs() if cfg.name == model_name), 
                None
            )
            if model_config and model_config.knowledge_domain == knowledge_domain:
                best_model = model_name
                break
            elif model_config and model_config.knowledge_domain in knowledge_domain:
                # Частичное совпадение домена
                if len(model_config.knowledge_domain) > best_domain_match:
                    best_domain_match = len(model_config.knowledge_domain)
                    best_model = model_name
        
        if best_model:
            return best_model
        
        if not optimal_group:
            # Если группа пуста, ищем любую доступную модель нужного типа
            for model_config in config.get_model_configs():
                if model_config.type == query_type:
                    return model_config.name
        
        # Выбираем первую доступную модель из группы
        for model_name in optimal_group:
            if model_name in self.model_manager.loaded_models:
                return model_name
        
        # Если ни одна модель не загружена, возвращаем первую из группы
        return optimal_group[0] if optimal_group else "mozgach2_general_01"


class Mozgach2System:
    """Основная система Mozgach2"""
    
    def __init__(self, auto_load_models: bool = True):
        self.logger = logging.getLogger(__name__)
        self.model_manager = ModelManager()
        self.quantum_manager = QuantumEntanglementManager()
        self.query_router = QueryRouter(self.model_manager, self.quantum_manager)
        
        self.active_queries = 0
        self.query_history = []
        
        if auto_load_models:
            asyncio.create_task(self._preload_critical_models())
    
    async def _preload_critical_models(self):
        """Предзагружает критические модели"""
        critical_models = [
            "mozgach2_general_01",
            "mozgach2_technical_01",
            "mozgach2_spiritual_01",
            "mozgach2_conversational_01"
        ]
        
        for model_name in critical_models:
            await self.model_manager.load_model(model_name)
            await asyncio.sleep(0.1)  # Небольшая задержка между загрузками
    
    async def query(self, query_text: str, model_type: Optional[ModelType] = None) -> QueryResult:
        """Обрабатывает запрос пользователя по доменам знаний"""
        start_time = time.time()
        self.active_queries += 1
        
        try:
            # Классифицируем запрос, если тип не указан
            if model_type is None:
                model_type = self.query_router.classify_query(query_text)
            
            # Определяем домен знаний для запроса
            knowledge_domain = self.query_router.classify_knowledge_domain(query_text)
            
            # Выбираем оптимальную модель по домену знаний
            model_name = self.query_router.select_optimal_model(query_text, model_type)
            
            # Загружаем модель, если она не загружена
            if not await self.model_manager.load_model(model_name):
                # Если не удалось загрузить, используем резервную модель
                model_name = "mozgach2_general_01"
                await self.model_manager.load_model(model_name)
            
            # Получаем конфигурацию модели
            model_config = next(
                (cfg for cfg in config.get_model_configs() if cfg.name == model_name), 
                None
            )
            
            # Имитируем обработку запроса (в реальности здесь будет вызов модели)
            response = await self._process_query_with_model(query_text, model_name, model_config)
            
            processing_time = time.time() - start_time
            
            # Создаем результат
            result = QueryResult(
                response=response,
                model_used=model_name,
                confidence=0.95,  # В реальности это будет вычисляться моделью
                processing_time=processing_time,
                model_type=model_config.type if model_config else ModelType.GENERAL,
                quantum_group=model_config.quantum_entanglement_group if model_config else 0,
                knowledge_domain=knowledge_domain
            )
            
            # Сохраняем в историю
            self.query_history.append({
                "query": query_text,
                "result": result,
                "timestamp": time.time()
            })
            
            self.logger.info(f"Запрос обработан моделью {model_name} (домен: {knowledge_domain}) за {processing_time:.3f}с")
            return result
            
        except Exception as e:
            self.logger.error(f"Ошибка при обработке запроса: {e}")
            # Возвращаем ошибку
            return QueryResult(
                response=f"Произошла ошибка при обработке запроса: {str(e)}",
                model_used="error",
                confidence=0.0,
                processing_time=time.time() - start_time,
                model_type=ModelType.GENERAL,
                quantum_group=0,
                knowledge_domain="unknown"
            )
        finally:
            self.active_queries -= 1
    
    async def _process_query_with_model(self, query: str, model_name: str, model_config: ModelConfig) -> str:
        """Обрабатывает запрос с конкретной моделью по домену знаний"""
        # Имитация обработки запроса
        await asyncio.sleep(0.1)  # Имитация времени обработки
        
        # Получаем домен знаний модели
        knowledge_domain = model_config.knowledge_domain
        
        # Генерируем ответ на основе типа модели и домена знаний
        if model_config.type == ModelType.TECHNICAL:
            if "mathematics" in knowledge_domain:
                return f"Математический ответ от {model_name} (домен: {knowledge_domain}): {query} - это математическая задача, которая решается с помощью..."
            elif "physics" in knowledge_domain:
                return f"Физический ответ от {model_name} (домен: {knowledge_domain}): {query} - это физическое явление, которое объясняется законами..."
            elif "computer_science" in knowledge_domain:
                return f"Компьютерный ответ от {model_name} (домен: {knowledge_domain}): {query} - это вопрос программирования, который решается алгоритмом..."
            else:
                return f"Технический ответ от {model_name} (домен: {knowledge_domain}): {query} - это интересный технический вопрос, который требует детального анализа..."
        elif model_config.type == ModelType.SPIRITUAL:
            if "buddhism" in knowledge_domain:
                return f"Буддийский ответ от {model_name} (домен: {knowledge_domain}): {query} - согласно буддийскому учению, это понимается как..."
            elif "meditation" in knowledge_domain:
                return f"Медитативный ответ от {model_name} (домен: {knowledge_domain}): {query} - в практике медитации это достигается через..."
            else:
                return f"Духовный ответ от {model_name} (домен: {knowledge_domain}): {query} - это глубокий вопрос, который затрагивает суть человеческого существования..."
        elif model_config.type == ModelType.BUSINESS:
            if "economics" in knowledge_domain:
                return f"Экономический ответ от {model_name} (домен: {knowledge_domain}): {query} - с экономической точки зрения, это анализируется через..."
            elif "finance" in knowledge_domain:
                return f"Финансовый ответ от {model_name} (домен: {knowledge_domain}): {query} - в финансовом аспекте, это рассматривается как..."
            else:
                return f"Бизнес ответ от {model_name} (домен: {knowledge_domain}): {query} - с точки зрения бизнеса, это можно рассмотреть следующим образом..."
        elif model_config.type == ModelType.CREATIVE:
            if "visual_arts" in knowledge_domain:
                return f"Художественный ответ от {model_name} (домен: {knowledge_domain}): {query} - в изобразительном искусстве это выражается через..."
            elif "music" in knowledge_domain:
                return f"Музыкальный ответ от {model_name} (домен: {knowledge_domain}): {query} - в музыке это проявляется как..."
            else:
                return f"Творческий ответ от {model_name} (домен: {knowledge_domain}): {query} - это вдохновляет на творческое осмысление..."
        elif model_config.type == ModelType.CONVERSATIONAL:
            if "russian_culture" in knowledge_domain:
                return f"Русско-культурный ответ от {model_name} (домен: {knowledge_domain}): {query} - в русской культуре это традиционно понимается как..."
            elif "slavic" in knowledge_domain:
                return f"Славянский ответ от {model_name} (домен: {knowledge_domain}): {query} - в славянской традиции это означает..."
            else:
                return f"Разговорный ответ от {model_name} (домен: {knowledge_domain}): {query} - давайте обсудим это в непринужденной беседе..."
        else:
            return f"Общий ответ от {model_name} (домен: {knowledge_domain}): {query} - это интересный вопрос, который можно рассмотреть с разных сторон..."
    
    async def batch_query(self, queries: List[str]) -> List[QueryResult]:
        """Обрабатывает несколько запросов параллельно"""
        tasks = [self.query(query) for query in queries]
        return await asyncio.gather(*tasks)
    
    def get_system_status(self) -> SystemStatus:
        """Возвращает статус системы"""
        memory = psutil.virtual_memory()
        gpu_memory = 0
        
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_memory = sum(gpu.memoryTotal for gpu in gpus) / 1024  # GB
        except:
            pass
        
        return SystemStatus(
            total_models=config.TOTAL_MODELS,
            loaded_models=self.model_manager.get_loaded_models_count(),
            available_memory_gb=memory.available / (1024**3),
            gpu_memory_gb=gpu_memory,
            system_load=psutil.getloadavg()[0],
            active_queries=self.active_queries,
            cache_hit_rate=0.85  # В реальности это будет вычисляться
        )
    
    def get_query_history(self, limit: int = 100) -> List[Dict]:
        """Возвращает историю запросов"""
        return self.query_history[-limit:] if limit > 0 else self.query_history
    
    async def shutdown(self):
        """Завершает работу системы"""
        self.logger.info("Завершение работы системы Mozgach2...")
        
        # Выгружаем все модели
        for model_name in list(self.model_manager.loaded_models.keys()):
            await self.model_manager.unload_model(model_name)
        
        self.logger.info("Система Mozgach2 успешно завершена")


# Создаем глобальный экземпляр системы
mozgach2_system = None


async def get_mozgach2_system() -> Mozgach2System:
    """Возвращает глобальный экземпляр системы Mozgach2"""
    global mozgach2_system
    if mozgach2_system is None:
        mozgach2_system = Mozgach2System()
    return mozgach2_system


async def shutdown_mozgach2_system():
    """Завершает работу глобальной системы Mozgach2"""
    global mozgach2_system
    if mozgach2_system:
        await mozgach2_system.shutdown()
        mozgach2_system = None


if __name__ == "__main__":
    # Пример использования
    async def main():
        system = Mozgach2System()
        
        # Тестовые запросы по различным доменам знаний
        queries = [
            "Как работает квантовая запутанность?",
            "Объясни принципы буддизма",
            "Расскажи о современных технологиях в бизнесе",
            "Что такое славянская культура?",
            "Как решить квадратное уравнение?",
            "Расскажи о русских традициях"
        ]
        
        for query in queries:
            result = await system.query(query)
            print(f"Запрос: {query}")
            print(f"Ответ: {result.response}")
            print(f"Модель: {result.model_used}")
            print(f"Домен знаний: {result.knowledge_domain}")
            print(f"Время: {result.processing_time:.3f}с")
            print("-" * 50)
        
        # Статус системы
        status = system.get_system_status()
        print(f"Статус системы:")
        print(f"  Загружено моделей: {status.loaded_models}/{status.total_models}")
        print(f"  Доступно памяти: {status.available_memory_gb:.2f} GB")
        print(f"  Активных запросов: {status.active_queries}")
        
        await system.shutdown()
    
    asyncio.run(main())
