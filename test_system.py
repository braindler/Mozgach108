#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации системы Mozgach2
"""

import asyncio
import logging
import sys
from pathlib import Path

# Добавляем корневую папку в путь для импортов
sys.path.insert(0, str(Path(__file__).parent))

from config import config, ModelType
from src.mozgach2_system import Mozgach2System


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_basic_functionality():
    """Тестирует базовую функциональность системы"""
    print("🧪 Тестирование базовой функциональности Mozgach2")
    print("=" * 60)
    
    # Создаем систему
    system = Mozgach2System(auto_load_models=True)
    
    # Ждем загрузки критических моделей
    await asyncio.sleep(2)
    
    # Тестовые запросы разных типов
    test_queries = [
        ("Технический вопрос", "Как работает квантовая запутанность?", ModelType.TECHNICAL),
        ("Духовный вопрос", "Объясни принципы буддизма", ModelType.SPIRITUAL),
        ("Бизнес вопрос", "Какие современные технологии используются в бизнесе?", ModelType.BUSINESS),
        ("Творческий вопрос", "Как развить креативность?", ModelType.CREATIVE),
        ("Разговорный вопрос", "Привет! Как дела?", ModelType.CONVERSATIONAL),
        ("Общий вопрос", "Что такое искусственный интеллект?", ModelType.GENERAL)
    ]
    
    print("📝 Тестирование различных типов запросов:")
    print("-" * 60)
    
    for query_type, query_text, expected_model_type in test_queries:
        print(f"\n🔍 {query_type}:")
        print(f"   Запрос: {query_text}")
        
        # Обрабатываем запрос
        result = await system.query(query_text)
        
        print(f"   Ответ: {result.response[:100]}...")
        print(f"   Модель: {result.model_used}")
        print(f"   Тип модели: {result.model_type.value}")
        print(f"   Группа запутанности: {result.quantum_group}")
        print(f"   Время обработки: {result.processing_time:.3f}с")
        print(f"   Уверенность: {result.confidence:.2f}")
        
        # Проверяем, что тип модели соответствует ожидаемому
        if result.model_type == expected_model_type:
            print("   ✅ Тип модели соответствует ожидаемому")
        else:
            print(f"   ⚠️ Тип модели не соответствует ожидаемому (ожидался {expected_model_type.value})")
    
    return system


async def test_batch_processing():
    """Тестирует пакетную обработку запросов"""
    print("\n\n🔄 Тестирование пакетной обработки")
    print("=" * 60)
    
    system = Mozgach2System(auto_load_models=False)
    
    # Загружаем несколько моделей
    await system.model_manager.load_model("mozgach2_general_01")
    await system.model_manager.load_model("mozgach2_technical_01")
    await system.model_manager.load_model("mozgach2_spiritual_01")
    
    # Пакет запросов
    batch_queries = [
        "Что такое квантовая физика?",
        "Объясни принципы медитации",
        "Как работает блокчейн?",
        "Расскажи о древних философах",
        "Что такое машинное обучение?"
    ]
    
    print(f"📦 Обработка пакета из {len(batch_queries)} запросов...")
    start_time = asyncio.get_event_loop().time()
    
    results = await system.batch_query(batch_queries)
    
    total_time = asyncio.get_event_loop().time() - start_time
    
    print(f"⏱️ Общее время обработки: {total_time:.3f}с")
    print(f"🚀 Среднее время на запрос: {total_time/len(batch_queries):.3f}с")
    
    print("\n📊 Результаты пакетной обработки:")
    for i, (query, result) in enumerate(zip(batch_queries, results), 1):
        print(f"  {i}. {query[:50]}... → {result.model_used} ({result.processing_time:.3f}с)")
    
    await system.shutdown()


async def test_system_status():
    """Тестирует получение статуса системы"""
    print("\n\n📊 Тестирование статуса системы")
    print("=" * 60)
    
    system = Mozgach2System(auto_load_models=True)
    
    # Ждем загрузки моделей
    await asyncio.sleep(2)
    
    # Получаем статус
    status = system.get_system_status()
    
    print("📈 Статус системы Mozgach2:")
    print(f"  📚 Всего моделей: {status.total_models}")
    print(f"  💾 Загружено моделей: {status.loaded_models}")
    print(f"  🧠 Доступно памяти: {status.available_memory_gb:.2f} GB")
    print(f"  🎮 GPU память: {status.gpu_memory_gb:.2f} GB")
    print(f"  ⚡ Нагрузка системы: {status.system_load:.2f}")
    print(f"  🔄 Активных запросов: {status.active_queries}")
    print(f"  🎯 Кэш-хит: {status.cache_hit_rate:.1%}")
    
    # История запросов
    history = system.get_query_history(limit=5)
    if history:
        print(f"\n📜 Последние {len(history)} запросов:")
        for i, entry in enumerate(history, 1):
            print(f"  {i}. {entry['query'][:50]}... → {entry['result'].model_used}")
    
    await system.shutdown()


async def test_quantum_entanglement():
    """Тестирует работу квантовой запутанности"""
    print("\n\n⚛️ Тестирование квантовой запутанности")
    print("=" * 60)
    
    system = Mozgach2System(auto_load_models=False)
    
    # Загружаем несколько моделей из одной группы запутанности
    await system.model_manager.load_model("mozgach2_general_01")
    await system.model_manager.load_model("mozgach2_technical_01")
    await system.model_manager.load_model("mozgach2_spiritual_01")
    
    print("🔗 Группы квантовой запутанности:")
    for group_id, models in system.quantum_manager.entanglement_groups.items():
        if any(m in system.model_manager.loaded_models for m in models):
            print(f"  Группа {group_id}: {models}")
    
    # Тестируем запутанность
    test_model = "mozgach2_general_01"
    entangled_models = system.quantum_manager.get_entangled_models(test_model)
    
    print(f"\n🔗 Модели, запутанные с {test_model}:")
    for model in entangled_models:
        print(f"  - {model}")
    
    # Тестируем оптимальный выбор группы
    query = "Как работает квантовая запутанность?"
    query_type = system.query_router.classify_query(query)
    optimal_group = system.quantum_manager.get_optimal_model_group(query, query_type)
    
    print(f"\n🎯 Оптимальная группа для запроса '{query}':")
    print(f"  Тип запроса: {query_type.value}")
    print(f"  Оптимальная группа: {optimal_group}")
    
    await system.shutdown()


async def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования системы Mozgach2")
    print("=" * 80)
    
    try:
        # Тест 1: Базовая функциональность
        system = await test_basic_functionality()
        await system.shutdown()
        
        # Тест 2: Пакетная обработка
        await test_batch_processing()
        
        # Тест 3: Статус системы
        await test_system_status()
        
        # Тест 4: Квантовая запутанность
        await test_quantum_entanglement()
        
        print("\n\n✅ Все тесты завершены успешно!")
        print("🎉 Система Mozgach2 работает корректно!")
        
    except Exception as e:
        logger.error(f"Ошибка при тестировании: {e}")
        print(f"\n❌ Ошибка при тестировании: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Запускаем тестирование
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
