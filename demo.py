#!/usr/bin/env python3
"""
Демонстрация возможностей mozgach108
"""

import asyncio
import sys
import logging
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent))

from src.mozgach108_system import Mozgach108System
from config import config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def demo_spiritual_queries():
    """Демонстрация духовных запросов"""
    print("\n" + "="*60)
    print("🕉️ ДЕМОНСТРАЦИЯ ДУХОВНОЙ СФЕРЫ")
    print("="*60)
    
    spiritual_queries = [
        "Что такое медитация?",
        "Объясните принципы буддизма",
        "Как работает квантовая запутанность в духовном контексте?",
        "Что такое мантры и как их использовать?",
        "Расскажите о чакрах и энергетических центрах"
    ]
    
    system = Mozgach108System()
    await asyncio.sleep(2)  # Ждем инициализации
    
    for i, query in enumerate(spiritual_queries, 1):
        print(f"\n🔮 Запрос {i}: {query}")
        print("-" * 50)
        
        try:
            response = await system.query(query, domain_hint="spiritual")
            print(f"Ответ: {response.content[:200]}...")
            print(f"Уверенность: {response.confidence:.2f}")
            print(f"Время: {response.processing_time:.2f}с")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    await system.shutdown()


async def demo_material_queries():
    """Демонстрация материальных запросов"""
    print("\n" + "="*60)
    print("🔬 ДЕМОНСТРАЦИЯ МАТЕРИАЛЬНОЙ СФЕРЫ")
    print("="*60)
    
    material_queries = [
        "Объясните закон Ньютона",
        "Что такое квантовая механика?",
        "Как работает ДНК?",
        "Расскажите о теории относительности Эйнштейна",
        "Что такое машинное обучение?"
    ]
    
    system = Mozgach108System()
    await asyncio.sleep(2)
    
    for i, query in enumerate(material_queries, 1):
        print(f"\n🔮 Запрос {i}: {query}")
        print("-" * 50)
        
        try:
            response = await system.query(query, domain_hint="material")
            print(f"Ответ: {response.content[:200]}...")
            print(f"Уверенность: {response.confidence:.2f}")
            print(f"Время: {response.processing_time:.2f}с")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    await system.shutdown()


async def demo_programming_queries():
    """Демонстрация запросов программирования"""
    print("\n" + "="*60)
    print("💻 ДЕМОНСТРАЦИЯ СФЕРЫ ПРОГРАММИРОВАНИЯ")
    print("="*60)
    
    programming_queries = [
        "Как написать функцию на Python?",
        "Объясните алгоритм быстрой сортировки",
        "Что такое паттерн Singleton?",
        "Как работает React?",
        "Расскажите о машинном обучении в программировании"
    ]
    
    system = Mozgach108System()
    await asyncio.sleep(2)
    
    for i, query in enumerate(programming_queries, 1):
        print(f"\n🔮 Запрос {i}: {query}")
        print("-" * 50)
        
        try:
            response = await system.query(query, domain_hint="programming")
            print(f"Ответ: {response.content[:200]}...")
            print(f"Уверенность: {response.confidence:.2f}")
            print(f"Время: {response.processing_time:.2f}с")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    await system.shutdown()


async def demo_quantum_queries():
    """Демонстрация квантовых запросов"""
    print("\n" + "="*60)
    print("🔮 ДЕМОНСТРАЦИЯ КВАНТОВЫХ ТЕХНОЛОГИЙ")
    print("="*60)
    
    quantum_queries = [
        "Что такое квантовая запутанность?",
        "Объясните алгоритм Гровера",
        "Как работает квантовый компьютер?",
        "Что такое квантовая криптография?",
        "Расскажите о квантовой симуляции"
    ]
    
    system = Mozgach108System()
    await asyncio.sleep(2)
    
    for i, query in enumerate(quantum_queries, 1):
        print(f"\n🔮 Запрос {i}: {query}")
        print("-" * 50)
        
        try:
            response = await system.query(query, domain_hint="quantum")
            print(f"Ответ: {response.content[:200]}...")
            print(f"Уверенность: {response.confidence:.2f}")
            print(f"Время: {response.processing_time:.2f}с")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    await system.shutdown()


async def demo_batch_processing():
    """Демонстрация пакетной обработки"""
    print("\n" + "="*60)
    print("📦 ДЕМОНСТРАЦИЯ ПАКЕТНОЙ ОБРАБОТКИ")
    print("="*60)
    
    batch_queries = [
        "Что такое любовь?",
        "Как работает гравитация?",
        "Напишите код на Python",
        "Объясните квантовую суперпозицию"
    ]
    
    system = Mozgach108System()
    await asyncio.sleep(2)
    
    print(f"📦 Обработка {len(batch_queries)} запросов...")
    
    try:
        responses = await system.batch_query(batch_queries)
        
        for i, (query, response) in enumerate(zip(batch_queries, responses), 1):
            print(f"\n🔮 Запрос {i}: {query}")
            print(f"Ответ: {response.content[:150]}...")
            print(f"Уверенность: {response.confidence:.2f}")
            print(f"Время: {response.processing_time:.2f}с")
    
    except Exception as e:
        print(f"❌ Ошибка пакетной обработки: {e}")
    
    await system.shutdown()


async def demo_system_stats():
    """Демонстрация статистики системы"""
    print("\n" + "="*60)
    print("📊 ДЕМОНСТРАЦИЯ СТАТИСТИКИ СИСТЕМЫ")
    print("="*60)
    
    system = Mozgach108System()
    await asyncio.sleep(2)
    
    # Выполняем несколько запросов
    test_queries = [
        "Что такое mozgach108?",
        "Объясните квантовую запутанность",
        "Как работает машинное обучение?",
        "Что такое медитация?",
        "Расскажите о программировании"
    ]
    
    for query in test_queries:
        try:
            await system.query(query)
        except Exception as e:
            print(f"❌ Ошибка запроса '{query}': {e}")
    
    # Получаем статистику
    stats = system.get_system_stats()
    
    print(f"📊 Статистика системы mozgach108:")
    print(f"   Всего запросов: {stats['total_queries']}")
    print(f"   Среднее время обработки: {stats['average_processing_time']:.2f}с")
    print(f"   Успешность: {stats['success_rate']:.1%}")
    print(f"   Загружено моделей: {stats['loaded_models']}")
    print(f"   Активных доменов: {stats['active_domains']}")
    print(f"   Сила запутанности: {stats['quantum_entanglement_strength']:.3f}")
    print(f"   Использование памяти: {stats['memory_usage_mb']}MB")
    
    await system.shutdown()


async def main():
    """Главная функция демонстрации"""
    print("🚀 ДЕМОНСТРАЦИЯ СИСТЕМЫ MOZGACH108")
    print("Система из 108 квантово-запутанных языковых моделей")
    print("="*60)
    
    try:
        # Демонстрация по сферам
        await demo_spiritual_queries()
        await demo_material_queries()
        await demo_programming_queries()
        await demo_quantum_queries()
        
        # Демонстрация пакетной обработки
        await demo_batch_processing()
        
        # Демонстрация статистики
        await demo_system_stats()
        
        print("\n" + "="*60)
        print("✅ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
        print("🔮 mozgach108 - будущее ИИ уже здесь!")
        print("="*60)
        
    except Exception as e:
        logger.error(f"❌ Ошибка демонстрации: {e}")
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Демонстрация прервана пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
