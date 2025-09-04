"""
FastAPI сервер для mozgach108
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from src.mozgach108_system import Mozgach108System, QueryResponse
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(
    title="mozgach108 API",
    description="API для системы из 108 квантово-запутанных языковых моделей",
    version=config.get("system.version", "1.0.0"),
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
if config.get("api.cors_enabled", True):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.get("security.allowed_origins", ["*"]),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Глобальная система
mozgach_system: Optional[Mozgach108System] = None


# Pydantic модели
class QueryRequest(BaseModel):
    """Модель запроса"""
    query: str = Field(..., description="Запрос к системе", max_length=10000)
    domain_hint: Optional[str] = Field(None, description="Подсказка о домене знаний")
    include_metadata: bool = Field(False, description="Включить метаданные в ответ")


class BatchQueryRequest(BaseModel):
    """Модель пакетного запроса"""
    queries: List[str] = Field(..., description="Список запросов", max_items=100)
    domain_hints: Optional[List[str]] = Field(None, description="Подсказки о доменах")
    include_metadata: bool = Field(False, description="Включить метаданные в ответ")


class QueryResponseModel(BaseModel):
    """Модель ответа"""
    content: str
    confidence: float
    domain_weights: Dict[str, float]
    processing_time: float
    timestamp: str
    quantum_state: Optional[Dict[str, Any]] = None


class SystemStatsModel(BaseModel):
    """Модель статистики системы"""
    total_queries: int
    total_processing_time: float
    average_processing_time: float
    success_rate: float
    loaded_models: int
    active_domains: int
    quantum_entanglement_strength: float
    memory_usage_mb: int


class HealthResponse(BaseModel):
    """Модель ответа health check"""
    status: str
    timestamp: str
    version: str
    uptime: float


# Зависимости
async def get_system() -> Mozgach108System:
    """Получение экземпляра системы"""
    global mozgach_system
    
    if mozgach_system is None:
        logger.info("🚀 Инициализация системы mozgach108...")
        mozgach_system = Mozgach108System()
        # Ждем инициализации
        await asyncio.sleep(2)
    
    return mozgach_system


# Middleware для логирования
@app.middleware("http")
async def log_requests(request, call_next):
    """Логирование запросов"""
    start_time = datetime.now()
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response


# Обработчики ошибок
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Глобальный обработчик ошибок"""
    logger.error(f"❌ Необработанная ошибка: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Внутренняя ошибка сервера",
            "detail": str(exc) if config.get("system.debug", False) else "Обратитесь к администратору"
        }
    )


# Маршруты API
@app.get("/", response_model=Dict[str, str])
async def root():
    """Корневой маршрут"""
    return {
        "message": "Добро пожаловать в mozgach108 API",
        "version": config.get("system.version", "1.0.0"),
        "description": "Система из 108 квантово-запутанных языковых моделей",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Проверка здоровья системы"""
    try:
        system = await get_system()
        stats = system.get_system_stats()
        
        return HealthResponse(
            status="healthy" if stats["loaded_models"] > 0 else "initializing",
            timestamp=datetime.now().isoformat(),
            version=config.get("system.version", "1.0.0"),
            uptime=stats.get("uptime", 0.0)
        )
    except Exception as e:
        logger.error(f"❌ Ошибка health check: {e}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            version=config.get("system.version", "1.0.0"),
            uptime=0.0
        )


@app.post("/query", response_model=QueryResponseModel)
async def query_endpoint(
    request: QueryRequest,
    system: Mozgach108System = Depends(get_system)
):
    """Выполнить запрос к системе"""
    try:
        logger.info(f"🔍 Обработка запроса: {request.query[:100]}...")
        
        # Выполняем запрос
        response = await system.query(request.query, request.domain_hint)
        
        # Формируем ответ
        response_data = {
            "content": response.content,
            "confidence": response.confidence,
            "domain_weights": response.domain_weights,
            "processing_time": response.processing_time,
            "timestamp": response.timestamp.isoformat()
        }
        
        if request.include_metadata:
            response_data["quantum_state"] = response.quantum_state
        
        return QueryResponseModel(**response_data)
        
    except Exception as e:
        logger.error(f"❌ Ошибка обработки запроса: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch", response_model=List[QueryResponseModel])
async def batch_query_endpoint(
    request: BatchQueryRequest,
    system: Mozgach108System = Depends(get_system)
):
    """Пакетная обработка запросов"""
    try:
        logger.info(f"📦 Пакетная обработка {len(request.queries)} запросов...")
        
        # Выполняем пакетные запросы
        responses = await system.batch_query(request.queries)
        
        # Формируем ответы
        response_data = []
        for response in responses:
            data = {
                "content": response.content,
                "confidence": response.confidence,
                "domain_weights": response.domain_weights,
                "processing_time": response.processing_time,
                "timestamp": response.timestamp.isoformat()
            }
            
            if request.include_metadata:
                data["quantum_state"] = response.quantum_state
            
            response_data.append(QueryResponseModel(**data))
        
        return response_data
        
    except Exception as e:
        logger.error(f"❌ Ошибка пакетной обработки: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=SystemStatsModel)
async def get_stats(system: Mozgach108System = Depends(get_system)):
    """Получить статистику системы"""
    try:
        stats = system.get_system_stats()
        return SystemStatsModel(**stats)
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения статистики: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/optimize")
async def optimize_system(
    background_tasks: BackgroundTasks,
    system: Mozgach108System = Depends(get_system)
):
    """Оптимизировать систему"""
    try:
        logger.info("🔧 Запуск оптимизации системы...")
        
        # Запускаем оптимизацию в фоне
        background_tasks.add_task(system.optimize_system)
        
        return {"message": "Оптимизация запущена в фоновом режиме"}
        
    except Exception as e:
        logger.error(f"❌ Ошибка оптимизации: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/domains")
async def get_domains(system: Mozgach108System = Depends(get_system)):
    """Получить список доменов знаний"""
    try:
        domains_info = system.knowledge_domains.get_domain_statistics()
        return domains_info
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения доменов: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
async def get_models(system: Mozgach108System = Depends(get_system)):
    """Получить информацию о загруженных моделях"""
    try:
        models_info = system.model_manager.get_loaded_models_info()
        memory_stats = system.model_manager.get_memory_stats()
        
        return {
            "loaded_models": models_info,
            "memory_stats": memory_stats
        }
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения моделей: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory")
async def get_memory_stats(system: Mozgach108System = Depends(get_system)):
    """Получить статистику квантовой памяти"""
    try:
        memory_stats = system.quantum_memory.get_memory_stats()
        return memory_stats
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения статистики памяти: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/config")
async def get_config():
    """Получить конфигурацию системы"""
    try:
        return {
            "system": config.get_section("system"),
            "models": config.get_section("models"),
            "quantum": config.get_section("quantum"),
            "api": config.get_section("api")
        }
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения конфигурации: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket для real-time взаимодействия
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    """WebSocket для real-time взаимодействия"""
    await websocket.accept()
    
    try:
        system = await get_system()
        
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_json()
            
            if data.get("type") == "query":
                query = data.get("query", "")
                domain_hint = data.get("domain_hint")
                
                if query:
                    # Выполняем запрос
                    response = await system.query(query, domain_hint)
                    
                    # Отправляем ответ
                    await websocket.send_json({
                        "type": "response",
                        "content": response.content,
                        "confidence": response.confidence,
                        "processing_time": response.processing_time,
                        "timestamp": response.timestamp.isoformat()
                    })
            
            elif data.get("type") == "ping":
                # Отвечаем на ping
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
            
            elif data.get("type") == "close":
                break
    
    except Exception as e:
        logger.error(f"❌ Ошибка WebSocket: {e}")
        await websocket.close()


# События жизненного цикла
@app.on_event("startup")
async def startup_event():
    """Событие запуска приложения"""
    logger.info("🚀 Запуск mozgach108 API сервера...")
    
    # Инициализируем систему
    global mozgach_system
    mozgach_system = Mozgach108System()
    
    logger.info("✅ API сервер готов к работе")


@app.on_event("shutdown")
async def shutdown_event():
    """Событие завершения приложения"""
    logger.info("🛑 Завершение работы mozgach108 API сервера...")
    
    # Корректно завершаем работу системы
    global mozgach_system
    if mozgach_system:
        await mozgach_system.shutdown()
    
    logger.info("✅ API сервер завершил работу")


if __name__ == "__main__":
    # Запуск сервера для разработки
    uvicorn.run(
        app,
        host=config.get("api.host", "0.0.0.0"),
        port=config.get("api.port", 8000),
        log_level=config.get("system.log_level", "info").lower()
    )
