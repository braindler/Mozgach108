"""
Тестирование системы mozgach108
"""

import asyncio
import logging
import time
from typing import List, Dict, Any

from src.mozgach108_system import Mozgach108System
from config import config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Mozgach108Tester:
    """Тестер системы mozgach108"""
    
    def __init__(self):
        self.system = None
        self.test_results = []
    
    async def initialize_system(self):
        """Инициализация системы для тестирования"""
        logger.info("🚀 Инициализация системы для тестирования...")
        
        self.system = Mozgach108System()
        
        # Ждем полной инициализации
        await asyncio.sleep(3)
        
        logger.info("✅ Система инициализирована")
    
    async def test_basic_query(self) -> Dict[str, Any]:
        """Тест базового запроса"""
        logger.info("🧪 Тест базового запроса...")
        
        test_query = "Что такое квантовая запутанность?"
        start_time = time.time()
        
        try:
            response = await self.system.query(test_query)
            end_time = time.time()
            
            result = {
                "test_name": "basic_query",
                "status": "passed",
                "query": test_query,
                "response_length": len(response.content),
                "confidence": response.confidence,
                "processing_time": response.processing_time,
                "total_time": end_time - start_time,
                "domains_used": list(response.domain_weights.keys())
            }
            
            logger.info(f"✅ Базовый запрос: {response.confidence:.2f} уверенности")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка базового запроса: {e}")
            return {
                "test_name": "basic_query",
                "status": "failed",
                "error": str(e)
            }
    
    async def test_domain_specific_queries(self) -> List[Dict[str, Any]]:
        """Тест запросов по доменам"""
        logger.info("🧪 Тест запросов по доменам...")
        
        test_queries = [
            ("Как написать функцию на Python?", "programming"),
            ("Объясните принципы буддизма", "spiritual"),
            ("Что такое квантовые вычисления?", "quantum"),
            ("Как работает гравитация?", "material")
        ]
        
        results = []
        
        for query, domain_hint in test_queries:
            try:
                start_time = time.time()
                response = await self.system.query(query, domain_hint)
                end_time = time.time()
                
                result = {
                    "test_name": f"domain_query_{domain_hint}",
                    "status": "passed",
                    "query": query,
                    "domain_hint": domain_hint,
                    "confidence": response.confidence,
                    "processing_time": response.processing_time,
                    "total_time": end_time - start_time,
                    "primary_domain": max(response.domain_weights.items(), key=lambda x: x[1])[0] if response.domain_weights else None
                }
                
                logger.info(f"✅ {domain_hint} запрос: {response.confidence:.2f} уверенности")
                results.append(result)
                
            except Exception as e:
                logger.error(f"❌ Ошибка {domain_hint} запроса: {e}")
                results.append({
                    "test_name": f"domain_query_{domain_hint}",
                    "status": "failed",
                    "error": str(e)
                })
        
        return results
    
    async def test_batch_queries(self) -> Dict[str, Any]:
        """Тест пакетных запросов"""
        logger.info("🧪 Тест пакетных запросов...")
        
        batch_queries = [
            "Что такое машинное обучение?",
            "Объясните принципы йоги",
            "Как работает блокчейн?",
            "Что такое квантовая суперпозиция?",
            "Как создать веб-приложение?"
        ]
        
        try:
            start_time = time.time()
            responses = await self.system.batch_query(batch_queries)
            end_time = time.time()
            
            total_confidence = sum(r.confidence for r in responses)
            avg_confidence = total_confidence / len(responses)
            
            result = {
                "test_name": "batch_queries",
                "status": "passed",
                "query_count": len(batch_queries),
                "response_count": len(responses),
                "average_confidence": avg_confidence,
                "total_processing_time": sum(r.processing_time for r in responses),
                "total_time": end_time - start_time,
                "success_rate": len(responses) / len(batch_queries)
            }
            
            logger.info(f"✅ Пакетные запросы: {avg_confidence:.2f} средняя уверенность")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка пакетных запросов: {e}")
            return {
                "test_name": "batch_queries",
                "status": "failed",
                "error": str(e)
            }
    
    async def test_quantum_entanglement(self) -> Dict[str, Any]:
        """Тест квантовой запутанности"""
        logger.info("🧪 Тест квантовой запутанности...")
        
        try:
            # Получаем статистику системы
            stats = self.system.get_system_stats()
            
            result = {
                "test_name": "quantum_entanglement",
                "status": "passed",
                "entanglement_strength": stats["quantum_entanglement_strength"],
                "loaded_models": stats["loaded_models"],
                "active_domains": stats["active_domains"],
                "memory_usage_mb": stats["memory_usage_mb"]
            }
            
            # Проверяем, что запутанность работает
            if stats["quantum_entanglement_strength"] > 0:
                logger.info(f"✅ Квантовая запутанность: {stats['quantum_entanglement_strength']:.3f}")
            else:
                logger.warning("⚠️ Квантовая запутанность не активна")
                result["status"] = "warning"
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка теста квантовой запутанности: {e}")
            return {
                "test_name": "quantum_entanglement",
                "status": "failed",
                "error": str(e)
            }
    
    async def test_memory_system(self) -> Dict[str, Any]:
        """Тест системы памяти"""
        logger.info("🧪 Тест системы памяти...")
        
        try:
            # Выполняем несколько запросов для накопления памяти
            test_queries = [
                "Что такое искусственный интеллект?",
                "Объясните принципы машинного обучения",
                "Как работает нейронная сеть?"
            ]
            
            for query in test_queries:
                await self.system.query(query)
            
            # Получаем статистику памяти
            memory_stats = self.system.quantum_memory.get_memory_stats()
            
            result = {
                "test_name": "memory_system",
                "status": "passed",
                "total_entries": memory_stats["total_entries"],
                "total_patterns": memory_stats["total_patterns"],
                "memory_usage_mb": memory_stats["memory_usage_mb"],
                "average_confidence": memory_stats["average_confidence"],
                "domains": memory_stats["domains"]
            }
            
            logger.info(f"✅ Система памяти: {memory_stats['total_entries']} записей")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка теста системы памяти: {e}")
            return {
                "test_name": "memory_system",
                "status": "failed",
                "error": str(e)
            }
    
    async def test_performance(self) -> Dict[str, Any]:
        """Тест производительности"""
        logger.info("🧪 Тест производительности...")
        
        try:
            # Тест скорости обработки
            test_queries = [
                "Быстрый тест 1",
                "Быстрый тест 2", 
                "Быстрый тест 3",
                "Быстрый тест 4",
                "Быстрый тест 5"
            ]
            
            start_time = time.time()
            responses = await self.system.batch_query(test_queries)
            end_time = time.time()
            
            total_time = end_time - start_time
            avg_time_per_query = total_time / len(test_queries)
            
            result = {
                "test_name": "performance",
                "status": "passed",
                "total_queries": len(test_queries),
                "total_time": total_time,
                "average_time_per_query": avg_time_per_query,
                "queries_per_second": len(test_queries) / total_time,
                "average_confidence": sum(r.confidence for r in responses) / len(responses)
            }
            
            logger.info(f"✅ Производительность: {avg_time_per_query:.2f}с на запрос")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка теста производительности: {e}")
            return {
                "test_name": "performance",
                "status": "failed",
                "error": str(e)
            }
    
    async def test_optimization(self) -> Dict[str, Any]:
        """Тест оптимизации системы"""
        logger.info("🧪 Тест оптимизации системы...")
        
        try:
            # Получаем статистику до оптимизации
            stats_before = self.system.get_system_stats()
            
            # Запускаем оптимизацию
            start_time = time.time()
            await self.system.optimize_system()
            end_time = time.time()
            
            # Получаем статистику после оптимизации
            stats_after = self.system.get_system_stats()
            
            result = {
                "test_name": "optimization",
                "status": "passed",
                "optimization_time": end_time - start_time,
                "memory_before_mb": stats_before["memory_usage_mb"],
                "memory_after_mb": stats_after["memory_usage_mb"],
                "models_before": stats_before["loaded_models"],
                "models_after": stats_after["loaded_models"],
                "entanglement_before": stats_before["quantum_entanglement_strength"],
                "entanglement_after": stats_after["quantum_entanglement_strength"]
            }
            
            logger.info(f"✅ Оптимизация: {end_time - start_time:.2f}с")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка теста оптимизации: {e}")
            return {
                "test_name": "optimization",
                "status": "failed",
                "error": str(e)
            }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Запуск всех тестов"""
        logger.info("🚀 Запуск полного тестирования системы mozgach108...")
        
        await self.initialize_system()
        
        test_results = []
        
        # Базовые тесты
        test_results.append(await self.test_basic_query())
        
        # Тесты по доменам
        domain_results = await self.test_domain_specific_queries()
        test_results.extend(domain_results)
        
        # Пакетные тесты
        test_results.append(await self.test_batch_queries())
        
        # Тесты квантовой системы
        test_results.append(await self.test_quantum_entanglement())
        
        # Тесты памяти
        test_results.append(await self.test_memory_system())
        
        # Тесты производительности
        test_results.append(await self.test_performance())
        
        # Тесты оптимизации
        test_results.append(await self.test_optimization())
        
        # Анализ результатов
        passed_tests = [r for r in test_results if r["status"] == "passed"]
        failed_tests = [r for r in test_results if r["status"] == "failed"]
        warning_tests = [r for r in test_results if r["status"] == "warning"]
        
        summary = {
            "total_tests": len(test_results),
            "passed": len(passed_tests),
            "failed": len(failed_tests),
            "warnings": len(warning_tests),
            "success_rate": len(passed_tests) / len(test_results) if test_results else 0,
            "test_results": test_results,
            "system_stats": self.system.get_system_stats()
        }
        
        logger.info(f"📊 Результаты тестирования:")
        logger.info(f"✅ Пройдено: {len(passed_tests)}")
        logger.info(f"❌ Провалено: {len(failed_tests)}")
        logger.info(f"⚠️ Предупреждения: {len(warning_tests)}")
        logger.info(f"📈 Успешность: {summary['success_rate']:.1%}")
        
        return summary
    
    async def cleanup(self):
        """Очистка ресурсов"""
        if self.system:
            await self.system.shutdown()


async def main():
    """Главная функция тестирования"""
    tester = Mozgach108Tester()
    
    try:
        results = await tester.run_all_tests()
        
        # Сохраняем результаты
        import json
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        print("\n" + "="*60)
        print("🔮 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ MOZGACH108")
        print("="*60)
        print(f"📊 Всего тестов: {results['total_tests']}")
        print(f"✅ Пройдено: {results['passed']}")
        print(f"❌ Провалено: {results['failed']}")
        print(f"⚠️ Предупреждения: {results['warnings']}")
        print(f"📈 Успешность: {results['success_rate']:.1%}")
        print("="*60)
        
        if results['failed'] > 0:
            print("\n❌ ПРОВАЛЕННЫЕ ТЕСТЫ:")
            for test in results['test_results']:
                if test['status'] == 'failed':
                    print(f"  - {test['test_name']}: {test.get('error', 'Неизвестная ошибка')}")
        
        if results['warnings'] > 0:
            print("\n⚠️ ПРЕДУПРЕЖДЕНИЯ:")
            for test in results['test_results']:
                if test['status'] == 'warning':
                    print(f"  - {test['test_name']}")
        
        print(f"\n📄 Подробные результаты сохранены в test_results.json")
        
        # Возвращаем код выхода
        return 0 if results['failed'] == 0 else 1
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка тестирования: {e}")
        return 1
    
    finally:
        await tester.cleanup()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
