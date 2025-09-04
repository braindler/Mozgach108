"""
Квантовая память mozgach108 - система долговременной памяти
"""

import asyncio
import logging
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    """Запись в квантовой памяти"""
    entry_id: str
    content: str
    context: str
    domain: str
    confidence: float
    access_count: int
    created_at: datetime
    last_accessed: datetime
    quantum_signature: str
    related_entries: List[str]


@dataclass
class MemoryPattern:
    """Паттерн в квантовой памяти"""
    pattern_id: str
    description: str
    frequency: int
    domains: List[str]
    keywords: List[str]
    strength: float


class QuantumMemory:
    """
    Система квантовой памяти для mozgach108
    
    Хранит и обрабатывает долговременную память системы,
    включая контекст диалогов, паттерны взаимодействий
    и накопленные знания.
    """
    
    def __init__(self, memory_dir: str = "quantum_memory"):
        """
        Инициализация квантовой памяти
        
        Args:
            memory_dir: Директория для хранения памяти
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        self.entries: Dict[str, MemoryEntry] = {}
        self.patterns: Dict[str, MemoryPattern] = {}
        self.context_window = 100  # Размер контекстного окна
        self.max_entries = 10000   # Максимальное количество записей
        self.cleanup_threshold = 0.1  # Порог для очистки неиспользуемых записей
        
        # Квантовые индексы для быстрого поиска
        self.domain_index: Dict[str, List[str]] = {}
        self.keyword_index: Dict[str, List[str]] = {}
        self.temporal_index: Dict[str, List[str]] = {}
        
        logger.info("🧠 Инициализация квантовой памяти...")
    
    async def initialize(self):
        """Инициализация квантовой памяти"""
        try:
            # Загружаем существующую память
            await self._load_memory()
            
            # Строим индексы
            await self._build_indices()
            
            # Оптимизируем память
            await self._optimize_memory()
            
            logger.info(f"✅ Квантовая память инициализирована ({len(self.entries)} записей)")
            
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации квантовой памяти: {e}")
            raise
    
    async def _load_memory(self):
        """Загрузка памяти из файлов"""
        logger.info("📥 Загрузка квантовой памяти...")
        
        # Загружаем записи памяти
        entries_file = self.memory_dir / "entries.json"
        if entries_file.exists():
            try:
                with open(entries_file, 'r', encoding='utf-8') as f:
                    entries_data = json.load(f)
                
                for entry_data in entries_data:
                    # Восстанавливаем datetime объекты
                    entry_data['created_at'] = datetime.fromisoformat(entry_data['created_at'])
                    entry_data['last_accessed'] = datetime.fromisoformat(entry_data['last_accessed'])
                    
                    entry = MemoryEntry(**entry_data)
                    self.entries[entry.entry_id] = entry
                
                logger.info(f"📥 Загружено {len(self.entries)} записей памяти")
                
            except Exception as e:
                logger.warning(f"⚠️ Ошибка загрузки записей памяти: {e}")
        
        # Загружаем паттерны
        patterns_file = self.memory_dir / "patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    patterns_data = json.load(f)
                
                for pattern_data in patterns_data:
                    pattern = MemoryPattern(**pattern_data)
                    self.patterns[pattern.pattern_id] = pattern
                
                logger.info(f"📥 Загружено {len(self.patterns)} паттернов")
                
            except Exception as e:
                logger.warning(f"⚠️ Ошибка загрузки паттернов: {e}")
    
    async def _build_indices(self):
        """Построение индексов для быстрого поиска"""
        logger.debug("🔍 Построение индексов квантовой памяти...")
        
        self.domain_index.clear()
        self.keyword_index.clear()
        self.temporal_index.clear()
        
        for entry_id, entry in self.entries.items():
            # Индекс по доменам
            if entry.domain not in self.domain_index:
                self.domain_index[entry.domain] = []
            self.domain_index[entry.domain].append(entry_id)
            
            # Индекс по ключевым словам
            keywords = self._extract_keywords(entry.content + " " + entry.context)
            for keyword in keywords:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(entry_id)
            
            # Временной индекс (по дням)
            date_key = entry.created_at.date().isoformat()
            if date_key not in self.temporal_index:
                self.temporal_index[date_key] = []
            self.temporal_index[date_key].append(entry_id)
        
        logger.debug("✅ Индексы построены")
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Извлечение ключевых слов из текста"""
        import re
        
        # Простое извлечение ключевых слов
        words = re.findall(r'\b\w{3,}\b', text.lower())
        
        # Фильтруем стоп-слова
        stop_words = {
            'это', 'как', 'что', 'для', 'или', 'если', 'так', 'все', 'они',
            'она', 'его', 'её', 'уже', 'еще', 'при', 'про', 'том', 'тот',
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Возвращаем только уникальные ключевые слова
        return list(set(keywords))[:10]  # Максимум 10 ключевых слов
    
    async def store_memory(self, content: str, context: str, domain: str, confidence: float = 0.8) -> str:
        """
        Сохранение записи в квантовую память
        
        Args:
            content: Содержимое для сохранения
            context: Контекст записи
            domain: Домен знаний
            confidence: Уверенность в записи
            
        Returns:
            ID созданной записи
        """
        # Генерируем уникальный ID
        entry_id = self._generate_entry_id(content, context)
        
        # Проверяем, не существует ли уже такая запись
        if entry_id in self.entries:
            existing_entry = self.entries[entry_id]
            existing_entry.access_count += 1
            existing_entry.last_accessed = datetime.now()
            existing_entry.confidence = max(existing_entry.confidence, confidence)
            
            logger.debug(f"📝 Обновлена существующая запись: {entry_id}")
            return entry_id
        
        # Создаем новую запись
        quantum_signature = self._generate_quantum_signature(content, domain)
        related_entries = await self._find_related_entries(content, domain)
        
        new_entry = MemoryEntry(
            entry_id=entry_id,
            content=content,
            context=context,
            domain=domain,
            confidence=confidence,
            access_count=1,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            quantum_signature=quantum_signature,
            related_entries=related_entries
        )
        
        self.entries[entry_id] = new_entry
        
        # Обновляем индексы
        await self._update_indices(entry_id, new_entry)
        
        # Проверяем лимиты памяти
        if len(self.entries) > self.max_entries:
            await self._cleanup_memory()
        
        logger.debug(f"💾 Сохранена новая запись: {entry_id}")
        return entry_id
    
    def _generate_entry_id(self, content: str, context: str) -> str:
        """Генерация ID записи"""
        combined = f"{content}:{context}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _generate_quantum_signature(self, content: str, domain: str) -> str:
        """Генерация квантовой подписи записи"""
        signature_data = f"{content}:{domain}:quantum_memory"
        return hashlib.sha256(signature_data.encode()).hexdigest()[:12]
    
    async def _find_related_entries(self, content: str, domain: str, limit: int = 5) -> List[str]:
        """Поиск связанных записей"""
        related = []
        content_keywords = self._extract_keywords(content)
        
        # Ищем записи с похожими ключевыми словами в том же домене
        domain_entries = self.domain_index.get(domain, [])
        
        scores = {}
        for entry_id in domain_entries:
            if entry_id not in self.entries:
                continue
                
            entry = self.entries[entry_id]
            entry_keywords = self._extract_keywords(entry.content)
            
            # Вычисляем схожесть по ключевым словам
            common_keywords = set(content_keywords).intersection(set(entry_keywords))
            if common_keywords:
                similarity = len(common_keywords) / max(len(content_keywords), len(entry_keywords))
                scores[entry_id] = similarity
        
        # Возвращаем топ-N наиболее похожих записей
        sorted_related = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        related = [entry_id for entry_id, _ in sorted_related[:limit]]
        
        return related
    
    async def _update_indices(self, entry_id: str, entry: MemoryEntry):
        """Обновление индексов для новой записи"""
        # Обновляем индекс доменов
        if entry.domain not in self.domain_index:
            self.domain_index[entry.domain] = []
        self.domain_index[entry.domain].append(entry_id)
        
        # Обновляем индекс ключевых слов
        keywords = self._extract_keywords(entry.content + " " + entry.context)
        for keyword in keywords:
            if keyword not in self.keyword_index:
                self.keyword_index[keyword] = []
            self.keyword_index[keyword].append(entry_id)
        
        # Обновляем временной индекс
        date_key = entry.created_at.date().isoformat()
        if date_key not in self.temporal_index:
            self.temporal_index[date_key] = []
        self.temporal_index[date_key].append(entry_id)
    
    async def retrieve_memories(self, query: str, domain: Optional[str] = None, 
                              limit: int = 10) -> List[MemoryEntry]:
        """
        Поиск записей в памяти
        
        Args:
            query: Поисковый запрос
            domain: Фильтр по домену
            limit: Максимальное количество результатов
            
        Returns:
            Список найденных записей
        """
        query_keywords = self._extract_keywords(query)
        candidate_entries = set()
        
        # Поиск по ключевым словам
        for keyword in query_keywords:
            if keyword in self.keyword_index:
                candidate_entries.update(self.keyword_index[keyword])
        
        # Фильтрация по домену
        if domain and domain in self.domain_index:
            domain_entries = set(self.domain_index[domain])
            candidate_entries = candidate_entries.intersection(domain_entries)
        
        # Вычисляем релевантность
        scored_entries = []
        for entry_id in candidate_entries:
            if entry_id not in self.entries:
                continue
                
            entry = self.entries[entry_id]
            score = self._calculate_relevance_score(entry, query_keywords)
            
            if score > 0:
                scored_entries.append((entry, score))
        
        # Сортируем по релевантности и частоте обращений
        scored_entries.sort(key=lambda x: (x[1], x[0].access_count), reverse=True)
        
        # Обновляем статистику доступа
        result_entries = []
        for entry, _ in scored_entries[:limit]:
            entry.access_count += 1
            entry.last_accessed = datetime.now()
            result_entries.append(entry)
        
        logger.debug(f"🔍 Найдено {len(result_entries)} записей для запроса: {query[:50]}")
        return result_entries
    
    def _calculate_relevance_score(self, entry: MemoryEntry, query_keywords: List[str]) -> float:
        """Вычисление релевантности записи к запросу"""
        entry_keywords = self._extract_keywords(entry.content + " " + entry.context)
        
        if not entry_keywords:
            return 0.0
        
        # Количество совпадающих ключевых слов
        common_keywords = set(query_keywords).intersection(set(entry_keywords))
        keyword_score = len(common_keywords) / len(query_keywords) if query_keywords else 0
        
        # Учитываем уверенность записи
        confidence_score = entry.confidence
        
        # Учитываем частоту обращений (популярность)
        access_score = min(entry.access_count / 10.0, 1.0)
        
        # Учитываем свежесть записи
        days_old = (datetime.now() - entry.created_at).days
        recency_score = max(0, 1.0 - days_old / 365.0)  # Снижение за год до 0
        
        # Итоговая оценка
        total_score = (
            0.4 * keyword_score +
            0.3 * confidence_score +
            0.2 * access_score +
            0.1 * recency_score
        )
        
        return total_score
    
    async def enhance_response(self, response_data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Обогащение ответа через квантовую память
        
        Args:
            response_data: Исходные данные ответа
            query: Исходный запрос
            
        Returns:
            Обогащенные данные ответа
        """
        logger.debug("🧠 Обогащение ответа через квантовую память...")
        
        try:
            # Ищем релевантные воспоминания
            relevant_memories = await self.retrieve_memories(query, limit=3)
            
            enhanced_content = response_data.get("content", "")
            confidence = response_data.get("confidence", 0.5)
            
            # Добавляем контекст из памяти
            if relevant_memories:
                memory_context = "\n\n🧠 Контекст из квантовой памяти:"
                
                for memory in relevant_memories:
                    if memory.confidence > 0.7:  # Только высококачественные воспоминания
                        memory_context += f"\n• {memory.content[:100]}..."
                
                enhanced_content += memory_context
                
                # Увеличиваем уверенность, если есть подтверждающие воспоминания
                memory_boost = min(0.2, len(relevant_memories) * 0.05)
                confidence = min(1.0, confidence + memory_boost)
            
            # Сохраняем этот диалог в память
            await self.store_memory(
                content=enhanced_content,
                context=query,
                domain=response_data.get("quantum_state", {}).get("primary_domain", "general"),
                confidence=confidence
            )
            
            return {
                "content": enhanced_content,
                "confidence": confidence,
                "memory_enhanced": len(relevant_memories) > 0,
                "memory_context_count": len(relevant_memories)
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка обогащения ответа: {e}")
            return response_data
    
    async def analyze_patterns(self) -> List[MemoryPattern]:
        """Анализ паттернов в памяти"""
        logger.info("🔍 Анализ паттернов в квантовой памяти...")
        
        # Анализируем частые ключевые слова
        keyword_frequencies = {}
        domain_distributions = {}
        
        for entry in self.entries.values():
            # Подсчет ключевых слов
            keywords = self._extract_keywords(entry.content + " " + entry.context)
            for keyword in keywords:
                keyword_frequencies[keyword] = keyword_frequencies.get(keyword, 0) + 1
            
            # Распределение по доменам
            domain_distributions[entry.domain] = domain_distributions.get(entry.domain, 0) + 1
        
        # Создаем паттерны на основе частых ключевых слов
        new_patterns = []
        
        # Топ ключевые слова
        top_keywords = sorted(keyword_frequencies.items(), key=lambda x: x[1], reverse=True)[:20]
        
        for i, (keyword, frequency) in enumerate(top_keywords):
            if frequency > 5:  # Минимальная частота
                pattern_id = f"keyword_pattern_{keyword}_{i}"
                
                # Находим домены, связанные с этим ключевым словом
                related_domains = []
                for entry in self.entries.values():
                    entry_keywords = self._extract_keywords(entry.content + " " + entry.context)
                    if keyword in entry_keywords:
                        if entry.domain not in related_domains:
                            related_domains.append(entry.domain)
                
                pattern = MemoryPattern(
                    pattern_id=pattern_id,
                    description=f"Частое ключевое слово: {keyword}",
                    frequency=frequency,
                    domains=related_domains,
                    keywords=[keyword],
                    strength=min(1.0, frequency / 50.0)
                )
                
                new_patterns.append(pattern)
                self.patterns[pattern_id] = pattern
        
        logger.info(f"✅ Найдено {len(new_patterns)} новых паттернов")
        return new_patterns
    
    async def _cleanup_memory(self):
        """Очистка неиспользуемой памяти"""
        logger.info("🧹 Очистка квантовой памяти...")
        
        current_time = datetime.now()
        entries_to_remove = []
        
        for entry_id, entry in self.entries.items():
            # Удаляем записи с низкой релевантностью
            days_since_access = (current_time - entry.last_accessed).days
            
            # Критерии для удаления:
            # - Низкая уверенность и редкое использование
            # - Старые записи с очень редким доступом
            should_remove = (
                (entry.confidence < self.cleanup_threshold and entry.access_count < 3) or
                (days_since_access > 365 and entry.access_count < 2) or
                (entry.confidence < 0.3 and days_since_access > 180)
            )
            
            if should_remove:
                entries_to_remove.append(entry_id)
        
        # Удаляем записи
        removed_count = 0
        for entry_id in entries_to_remove:
            if len(self.entries) <= self.max_entries * 0.8:  # Оставляем 80% записей
                break
                
            del self.entries[entry_id]
            removed_count += 1
        
        # Перестраиваем индексы после очистки
        if removed_count > 0:
            await self._build_indices()
        
        logger.info(f"🧹 Удалено {removed_count} записей из памяти")
    
    async def _optimize_memory(self):
        """Оптимизация квантовой памяти"""
        logger.debug("🔧 Оптимизация квантовой памяти...")
        
        # Анализируем паттерны
        await self.analyze_patterns()
        
        # Обновляем связи между записями
        await self._update_related_entries()
        
        logger.debug("✅ Оптимизация памяти завершена")
    
    async def _update_related_entries(self):
        """Обновление связей между записями"""
        logger.debug("🔗 Обновление связей между записями...")
        
        for entry_id, entry in self.entries.items():
            # Находим новые связанные записи
            new_related = await self._find_related_entries(entry.content, entry.domain)
            
            # Обновляем список связанных записей
            entry.related_entries = new_related
    
    async def save_state(self):
        """Сохранение состояния памяти"""
        logger.info("💾 Сохранение состояния квантовой памяти...")
        
        try:
            # Сохраняем записи
            entries_data = []
            for entry in self.entries.values():
                entry_dict = asdict(entry)
                # Преобразуем datetime в строку
                entry_dict['created_at'] = entry.created_at.isoformat()
                entry_dict['last_accessed'] = entry.last_accessed.isoformat()
                entries_data.append(entry_dict)
            
            entries_file = self.memory_dir / "entries.json"
            with open(entries_file, 'w', encoding='utf-8') as f:
                json.dump(entries_data, f, ensure_ascii=False, indent=2)
            
            # Сохраняем паттерны
            patterns_data = [asdict(pattern) for pattern in self.patterns.values()]
            patterns_file = self.memory_dir / "patterns.json"
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(patterns_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Сохранено {len(self.entries)} записей и {len(self.patterns)} паттернов")
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения памяти: {e}")
            raise
    
    def get_memory_usage(self) -> int:
        """Получить использование памяти в MB"""
        # Примерная оценка использования памяти
        entries_size = len(self.entries) * 2  # ~2KB на запись
        patterns_size = len(self.patterns) * 1  # ~1KB на паттерн
        indices_size = sum(len(index) for index in [
            self.domain_index, self.keyword_index, self.temporal_index
        ]) * 0.1  # ~100B на индекс
        
        total_size_kb = entries_size + patterns_size + indices_size
        return int(total_size_kb / 1024)  # Конвертируем в MB
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Получить статистику памяти"""
        if not self.entries:
            return {
                "total_entries": 0,
                "total_patterns": 0,
                "memory_usage_mb": 0,
                "domains": {},
                "average_confidence": 0.0
            }
        
        domain_counts = {}
        total_confidence = 0.0
        total_access_count = 0
        
        for entry in self.entries.values():
            domain_counts[entry.domain] = domain_counts.get(entry.domain, 0) + 1
            total_confidence += entry.confidence
            total_access_count += entry.access_count
        
        return {
            "total_entries": len(self.entries),
            "total_patterns": len(self.patterns),
            "memory_usage_mb": self.get_memory_usage(),
            "domains": domain_counts,
            "average_confidence": total_confidence / len(self.entries),
            "total_access_count": total_access_count,
            "index_sizes": {
                "domain_index": len(self.domain_index),
                "keyword_index": len(self.keyword_index),
                "temporal_index": len(self.temporal_index)
            }
        }
