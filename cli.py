"""
Командная строка mozgach108
"""

import asyncio
import click
import logging
import sys
from pathlib import Path
from typing import Optional

from src.mozgach108_system import Mozgach108System
from config import config

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.get("system.log_level", "INFO")),
    format=config.get("logging.format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=config.get("system.version", "1.0.0"))
@click.option('--debug', is_flag=True, help='Включить режим отладки')
@click.option('--config', type=click.Path(), help='Путь к файлу конфигурации')
@click.pass_context
def cli(ctx, debug, config_path):
    """mozgach108 - Система из 108 квантово-запутанных языковых моделей"""
    ctx.ensure_object(dict)
    
    if debug:
        config.set("system.debug", True)
        config.set("system.log_level", "DEBUG")
        logging.getLogger().setLevel(logging.DEBUG)
    
    if config_path:
        config.config_path = config_path
        config._load_config()
    
    ctx.obj['config'] = config


@cli.command()
@click.option('--query', '-q', prompt='Введите ваш запрос', help='Запрос к системе')
@click.option('--domain', '-d', help='Подсказка о домене знаний')
@click.option('--output', '-o', type=click.Choice(['text', 'json', 'detailed']), default='text', help='Формат вывода')
@click.pass_context
def query(ctx, query, domain, output):
    """Выполнить запрос к системе mozgach108"""
    
    async def run_query():
        try:
            logger.info("🚀 Инициализация системы mozgach108...")
            system = Mozgach108System()
            
            logger.info(f"🔍 Обработка запроса: {query[:100]}...")
            response = await system.query(query, domain)
            
            if output == 'json':
                import json
                click.echo(json.dumps({
                    "content": response.content,
                    "confidence": response.confidence,
                    "domain_weights": response.domain_weights,
                    "processing_time": response.processing_time,
                    "timestamp": response.timestamp.isoformat()
                }, ensure_ascii=False, indent=2))
            
            elif output == 'detailed':
                click.echo(f"🔮 Ответ mozgach108:")
                click.echo(f"📝 Содержимое: {response.content}")
                click.echo(f"🎯 Уверенность: {response.confidence:.2f}")
                click.echo(f"⏱️ Время обработки: {response.processing_time:.2f}с")
                click.echo(f"📊 Домены знаний: {list(response.domain_weights.keys())}")
                click.echo(f"🔮 Квантовое состояние: {response.quantum_state}")
            
            else:  # text
                click.echo(response.content)
            
            await system.shutdown()
            
        except Exception as e:
            logger.error(f"❌ Ошибка выполнения запроса: {e}")
            click.echo(f"❌ Ошибка: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(run_query())


@cli.command()
@click.argument('queries_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Файл для сохранения результатов')
@click.option('--format', 'output_format', type=click.Choice(['json', 'csv', 'txt']), default='json', help='Формат вывода')
@click.pass_context
def batch(ctx, queries_file, output, output_format):
    """Пакетная обработка запросов из файла"""
    
    async def run_batch():
        try:
            # Читаем запросы из файла
            with open(queries_file, 'r', encoding='utf-8') as f:
                queries = [line.strip() for line in f if line.strip()]
            
            logger.info(f"📦 Обработка {len(queries)} запросов...")
            
            system = Mozgach108System()
            responses = await system.batch_query(queries)
            
            # Сохраняем результаты
            if output:
                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                if output_format == 'json':
                    import json
                    results = []
                    for i, response in enumerate(responses):
                        results.append({
                            "query": queries[i],
                            "response": response.content,
                            "confidence": response.confidence,
                            "processing_time": response.processing_time
                        })
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(results, f, ensure_ascii=False, indent=2)
                
                elif output_format == 'csv':
                    import csv
                    with open(output_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Query', 'Response', 'Confidence', 'Processing Time'])
                        for i, response in enumerate(responses):
                            writer.writerow([
                                queries[i],
                                response.content,
                                response.confidence,
                                response.processing_time
                            ])
                
                else:  # txt
                    with open(output_path, 'w', encoding='utf-8') as f:
                        for i, response in enumerate(responses):
                            f.write(f"Query: {queries[i]}\n")
                            f.write(f"Response: {response.content}\n")
                            f.write(f"Confidence: {response.confidence:.2f}\n")
                            f.write(f"Processing Time: {response.processing_time:.2f}s\n")
                            f.write("-" * 50 + "\n")
                
                click.echo(f"✅ Результаты сохранены в {output_path}")
            
            else:
                # Выводим результаты в консоль
                for i, response in enumerate(responses):
                    click.echo(f"Query {i+1}: {queries[i]}")
                    click.echo(f"Response: {response.content}")
                    click.echo(f"Confidence: {response.confidence:.2f}")
                    click.echo("-" * 50)
            
            await system.shutdown()
            
        except Exception as e:
            logger.error(f"❌ Ошибка пакетной обработки: {e}")
            click.echo(f"❌ Ошибка: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(run_batch())


@cli.command()
@click.option('--host', default=None, help='Хост для API сервера')
@click.option('--port', default=None, type=int, help='Порт для API сервера')
@click.option('--workers', default=None, type=int, help='Количество воркеров')
@click.pass_context
def serve(ctx, host, port, workers):
    """Запустить API сервер"""
    
    def run_server():
        try:
            import uvicorn
            from api.server import app
            
            # Применяем переопределения из командной строки
            if host:
                config.set("api.host", host)
            if port:
                config.set("api.port", port)
            if workers:
                config.set("api.workers", workers)
            
            host = config.get("api.host", "0.0.0.0")
            port = config.get("api.port", 8000)
            workers = config.get("api.workers", 4)
            
            logger.info(f"🚀 Запуск API сервера на {host}:{port}")
            
            uvicorn.run(
                app,
                host=host,
                port=port,
                workers=workers,
                log_level=config.get("system.log_level", "info").lower()
            )
            
        except ImportError:
            click.echo("❌ Для запуска сервера установите: pip install fastapi uvicorn", err=True)
            sys.exit(1)
        except Exception as e:
            logger.error(f"❌ Ошибка запуска сервера: {e}")
            click.echo(f"❌ Ошибка: {e}", err=True)
            sys.exit(1)
    
    run_server()


@cli.command()
@click.pass_context
def status(ctx):
    """Показать статус системы"""
    
    async def show_status():
        try:
            system = Mozgach108System()
            
            # Ждем инициализации
            await asyncio.sleep(2)
            
            stats = system.get_system_stats()
            
            click.echo("🔮 Статус системы mozgach108:")
            click.echo(f"📊 Всего запросов: {stats['total_queries']}")
            click.echo(f"⏱️ Среднее время обработки: {stats['average_processing_time']:.2f}с")
            click.echo(f"📈 Успешность: {stats['success_rate']:.1%}")
            click.echo(f"🧠 Загружено моделей: {stats['loaded_models']}")
            click.echo(f"📚 Активных доменов: {stats['active_domains']}")
            click.echo(f"🔗 Сила запутанности: {stats['quantum_entanglement_strength']:.3f}")
            click.echo(f"💾 Использование памяти: {stats['memory_usage_mb']}MB")
            
            await system.shutdown()
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения статуса: {e}")
            click.echo(f"❌ Ошибка: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(show_status())


@cli.command()
@click.pass_context
def optimize(ctx):
    """Оптимизировать систему"""
    
    async def run_optimization():
        try:
            logger.info("🔧 Запуск оптимизации системы...")
            
            system = Mozgach108System()
            await system.optimize_system()
            
            click.echo("✅ Оптимизация завершена")
            
            # Показываем статистику после оптимизации
            stats = system.get_system_stats()
            click.echo(f"📊 Статистика после оптимизации:")
            click.echo(f"🧠 Загружено моделей: {stats['loaded_models']}")
            click.echo(f"💾 Использование памяти: {stats['memory_usage_mb']}MB")
            click.echo(f"🔗 Сила запутанности: {stats['quantum_entanglement_strength']:.3f}")
            
            await system.shutdown()
            
        except Exception as e:
            logger.error(f"❌ Ошибка оптимизации: {e}")
            click.echo(f"❌ Ошибка: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(run_optimization())


@cli.command()
@click.option('--section', help='Секция конфигурации для показа')
@click.pass_context
def config_show(ctx, section):
    """Показать конфигурацию"""
    
    if section:
        config_section = config.get_section(section)
        if config_section:
            import json
            click.echo(json.dumps(config_section, indent=2, ensure_ascii=False))
        else:
            click.echo(f"❌ Секция '{section}' не найдена", err=True)
    else:
        import json
        click.echo(json.dumps(config.config, indent=2, ensure_ascii=False))


@cli.command()
@click.argument('key_path')
@click.argument('value')
@click.pass_context
def config_set(ctx, key_path, value):
    """Установить значение конфигурации"""
    
    try:
        # Пытаемся преобразовать значение в соответствующий тип
        if value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        elif value.isdigit():
            value = int(value)
        elif value.replace('.', '').isdigit():
            value = float(value)
        
        config.set(key_path, value)
        config.save_config()
        
        click.echo(f"✅ Установлено {key_path} = {value}")
        
    except Exception as e:
        click.echo(f"❌ Ошибка установки конфигурации: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def validate(ctx):
    """Валидировать конфигурацию"""
    
    if config.validate_config():
        click.echo("✅ Конфигурация валидна")
        sys.exit(0)
    else:
        click.echo("❌ Конфигурация содержит ошибки", err=True)
        sys.exit(1)


@cli.command()
@click.option('--interactive', '-i', is_flag=True, help='Интерактивный режим')
@click.pass_context
def chat(ctx, interactive):
    """Интерактивный чат с системой"""
    
    async def run_chat():
        try:
            logger.info("🚀 Запуск интерактивного чата...")
            
            system = Mozgach108System()
            
            click.echo("🔮 Добро пожаловать в mozgach108!")
            click.echo("💡 Введите 'exit' или 'quit' для выхода")
            click.echo("💡 Введите 'help' для справки")
            click.echo("-" * 50)
            
            while True:
                try:
                    query = click.prompt("Вы", type=str)
                    
                    if query.lower() in ('exit', 'quit', 'выход'):
                        break
                    
                    if query.lower() == 'help':
                        click.echo("🔮 mozgach108 - Система из 108 квантово-запутанных моделей")
                        click.echo("💡 Доступные команды:")
                        click.echo("   - exit/quit/выход - выход из чата")
                        click.echo("   - help - показать эту справку")
                        click.echo("   - status - показать статус системы")
                        click.echo("   - optimize - оптимизировать систему")
                        continue
                    
                    if query.lower() == 'status':
                        stats = system.get_system_stats()
                        click.echo(f"📊 Статус: {stats['loaded_models']} моделей, {stats['memory_usage_mb']}MB памяти")
                        continue
                    
                    if query.lower() == 'optimize':
                        await system.optimize_system()
                        click.echo("✅ Система оптимизирована")
                        continue
                    
                    if not query.strip():
                        continue
                    
                    click.echo("🔮 mozgach108 думает...")
                    response = await system.query(query)
                    
                    click.echo(f"🔮 mozgach108: {response.content}")
                    click.echo(f"🎯 Уверенность: {response.confidence:.2f}")
                    click.echo("-" * 30)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    click.echo(f"❌ Ошибка: {e}")
            
            await system.shutdown()
            click.echo("👋 До свидания!")
            
        except Exception as e:
            logger.error(f"❌ Ошибка чата: {e}")
            click.echo(f"❌ Ошибка: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(run_chat())


def main():
    """Главная функция CLI"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n👋 До свидания!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        click.echo(f"❌ Критическая ошибка: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
