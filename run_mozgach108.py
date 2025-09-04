#!/usr/bin/env python3
"""
Запуск системы mozgach108
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
    level=getattr(logging, config.get("system.log_level", "INFO")),
    format=config.get("logging.format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("mozgach108.log", encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска системы"""
    logger.info("🚀 Запуск системы mozgach108...")
    
    try:
        # Создаем систему
        system = Mozgach108System()
        
        # Ждем инициализации
        await asyncio.sleep(3)
        
        # Показываем статистику
        stats = system.get_system_stats()
        logger.info("📊 Статистика системы:")
        logger.info(f"   Загружено моделей: {stats['loaded_models']}")
        logger.info(f"   Активных доменов: {stats['active_domains']}")
        logger.info(f"   Сила запутанности: {stats['quantum_entanglement_strength']:.3f}")
        logger.info(f"   Использование памяти: {stats['memory_usage_mb']}MB")
        
        # Интерактивный режим
        logger.info("💬 Система готова к работе. Введите 'exit' для выхода.")
        
        while True:
            try:
                query = input("\n🔮 Ваш запрос: ").strip()
                
                if query.lower() in ['exit', 'quit', 'выход']:
                    break
                
                if not query:
                    continue
                
                logger.info(f"🔍 Обработка запроса: {query[:100]}...")
                response = await system.query(query)
                
                print(f"\n🔮 mozgach108: {response.content}")
                print(f"🎯 Уверенность: {response.confidence:.2f}")
                print(f"⏱️ Время обработки: {response.processing_time:.2f}с")
                print(f"📊 Домены: {list(response.domain_weights.keys())}")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"❌ Ошибка обработки запроса: {e}")
                print(f"❌ Ошибка: {e}")
        
        # Корректное завершение
        await system.shutdown()
        logger.info("✅ Система mozgach108 завершила работу")
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
