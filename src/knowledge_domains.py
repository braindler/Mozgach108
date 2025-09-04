"""
Домены знаний mozgach108 - управление 108 сферами знаний
"""

import asyncio
import logging
import re
from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import json

logger = logging.getLogger(__name__)


@dataclass
class DomainInfo:
    """Информация о домене знаний"""
    domain_id: str
    name: str
    description: str
    keywords: List[str]
    weight: float
    model_count: int
    specialization_level: float


class KnowledgeDomains:
    """
    Управление доменами знаний для 108 моделей
    
    Анализирует запросы пользователя и определяет релевантные
    домены знаний для активации соответствующих моделей.
    """
    
    def __init__(self, domains_config_path: Optional[str] = None):
        """
        Инициализация системы доменов знаний
        
        Args:
            domains_config_path: Путь к конфигурации доменов
        """
        self.domains: Dict[str, DomainInfo] = {}
        self.active_domains: Set[str] = set()
        self.domain_keywords: Dict[str, List[str]] = {}
        self.spiritual_keywords: Set[str] = set()
        self.programming_keywords: Set[str] = set()
        self.material_keywords: Set[str] = set()
        self.quantum_keywords: Set[str] = set()
        
        self._load_domain_definitions()
        
        logger.info("📚 Инициализация доменов знаний...")
    
    def _load_domain_definitions(self):
        """Загрузка определений доменов знаний"""
        logger.info("📖 Загрузка определений доменов...")
        
        # Духовная сфера (58 моделей)
        spiritual_domains = self._create_spiritual_domains()
        
        # Материальная сфера (60 моделей) 
        material_domains = self._create_material_domains()
        
        # Программирование и разработка (38 моделей)
        programming_domains = self._create_programming_domains()
        
        # Квантовые технологии (12 моделей)
        quantum_domains = self._create_quantum_domains()
        
        # Объединяем все домены
        all_domains = {
            **spiritual_domains,
            **material_domains, 
            **programming_domains,
            **quantum_domains
        }
        
        self.domains = all_domains
        self._build_keyword_indices()
        
        logger.info(f"✅ Загружено {len(self.domains)} доменов знаний")
    
    def _create_spiritual_domains(self) -> Dict[str, DomainInfo]:
        """Создание доменов духовной сферы"""
        spiritual_domains = {}
        
        spiritual_categories = [
            ("vedic_knowledge", "Ведическое знание", [
                "веды", "упанишады", "бхагавад-гита", "рамаяна", "махабхарата",
                "санскрит", "мантра", "йога", "медитация", "дхарма", "карма"
            ]),
            ("buddhist_philosophy", "Буддийская философия", [
                "буддизм", "дхарма", "сангха", "будда", "нирвана", "просветление",
                "медитация", "випассана", "дзен", "тибет", "далай-лама"
            ]),
            ("christian_mysticism", "Христианский мистицизм", [
                "христианство", "православие", "католицизм", "протестантизм", 
                "исихазм", "молитва", "пост", "таинства", "святые", "ангелы"
            ]),
            ("islamic_sufism", "Исламский суфизм", [
                "ислам", "суфизм", "коран", "хадис", "намаз", "хадж", "рамадан",
                "дервиш", "тарикат", "зикр", "аллах"
            ]),
            ("esoteric_traditions", "Эзотерические традиции", [
                "эзотерика", "оккультизм", "герметизм", "каббала", "алхимия",
                "астрология", "таро", "рунв", "магия", "ритуал"
            ]),
            ("meditation_practices", "Практики медитации", [
                "медитация", "осознанность", "випассана", "дзен", "мантра",
                "пранаяма", "чакра", "кундалини", "самадхи", "просветление"
            ]),
            ("sacred_geometry", "Священная геометрия", [
                "геометрия", "фракталы", "золотое сечение", "мандала", "янтра",
                "пифагор", "платон", "архитектура", "храм", "собор"
            ]),
            ("ancient_wisdom", "Древняя мудрость", [
                "древность", "мудрость", "философия", "гнозис", "традиция",
                "посвящение", "мистерии", "шаман", "друид", "жрец"
            ])
        ]
        
        for i, (domain_id, name, keywords) in enumerate(spiritual_categories):
            spiritual_domains[f"spiritual_{domain_id}"] = DomainInfo(
                domain_id=f"spiritual_{domain_id}",
                name=name,
                description=f"Домен духовных знаний: {name}",
                keywords=keywords,
                weight=0.8 + i * 0.02,  # Высокий вес для духовных доменов
                model_count=7 + i,  # Разное количество моделей на домен
                specialization_level=0.9
            )
            self.spiritual_keywords.update(keywords)
        
        return spiritual_domains
    
    def _create_material_domains(self) -> Dict[str, DomainInfo]:
        """Создание доменов материальной сферы"""
        material_domains = {}
        
        material_categories = [
            ("physics_classical", "Классическая физика", [
                "физика", "механика", "термодинамика", "электричество", "магнетизм",
                "оптика", "акустика", "ньютон", "эйнштейн", "относительность"
            ]),
            ("mathematics", "Математика", [
                "математика", "алгебра", "геометрия", "анализ", "топология",
                "статистика", "вероятность", "дискретная", "числа", "функции"
            ]),
            ("chemistry", "Химия", [
                "химия", "элементы", "реакции", "органическая", "неорганическая",
                "биохимия", "молекулы", "атомы", "периодическая", "катализ"
            ]),
            ("biology", "Биология", [
                "биология", "эволюция", "генетика", "экология", "ботаника",
                "зоология", "анатомия", "физиология", "клетка", "организм"
            ]),
            ("engineering", "Инженерия", [
                "инженерия", "механика", "электроника", "строительство", "машины",
                "автомобили", "самолеты", "корабли", "роботы", "автоматизация"
            ]),
            ("medicine", "Медицина", [
                "медицина", "здоровье", "болезни", "лечение", "диагностика",
                "хирургия", "фармакология", "анатомия", "терапия", "врач"
            ]),
            ("economics", "Экономика", [
                "экономика", "финансы", "деньги", "банки", "инвестиции",
                "рынок", "торговля", "бизнес", "маркетинг", "менеджмент"
            ]),
            ("education", "Образование", [
                "образование", "обучение", "школа", "университет", "педагогика",
                "методика", "учитель", "студент", "знания", "навыки"
            ])
        ]
        
        for i, (domain_id, name, keywords) in enumerate(material_categories):
            material_domains[f"material_{domain_id}"] = DomainInfo(
                domain_id=f"material_{domain_id}",
                name=name,
                description=f"Домен материальных знаний: {name}",
                keywords=keywords,
                weight=0.6 + i * 0.03,
                model_count=7 + i,
                specialization_level=0.8
            )
            self.material_keywords.update(keywords)
        
        return material_domains
    
    def _create_programming_domains(self) -> Dict[str, DomainInfo]:
        """Создание доменов программирования"""
        programming_domains = {}
        
        programming_categories = [
            ("languages", "Языки программирования", [
                "python", "javascript", "java", "c++", "c#", "go", "rust",
                "swift", "kotlin", "typescript", "php", "ruby", "scala"
            ]),
            ("web_development", "Веб-разработка", [
                "html", "css", "react", "vue", "angular", "node.js", "express",
                "django", "flask", "spring", "laravel", "wordpress", "frontend", "backend"
            ]),
            ("data_science", "Наука о данных", [
                "данные", "анализ", "статистика", "машинное обучение", "ai",
                "pandas", "numpy", "sklearn", "tensorflow", "pytorch", "jupyter"
            ]),
            ("databases", "Базы данных", [
                "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
                "oracle", "sqlite", "nosql", "orm", "миграции", "индексы"
            ]),
            ("devops", "DevOps", [
                "docker", "kubernetes", "jenkins", "gitlab", "github", "ci/cd",
                "aws", "azure", "google cloud", "terraform", "ansible", "мониторинг"
            ]),
            ("mobile_development", "Мобильная разработка", [
                "android", "ios", "flutter", "react native", "swift", "kotlin",
                "xamarin", "cordova", "ionic", "мобильные приложения"
            ]),
            ("algorithms", "Алгоритмы", [
                "алгоритмы", "структуры данных", "сложность", "сортировка",
                "поиск", "графы", "деревья", "хэш", "динамическое программирование"
            ]),
            ("security", "Безопасность", [
                "безопасность", "шифрование", "аутентификация", "авторизация",
                "ssl", "oauth", "csrf", "xss", "sql injection", "penetration testing"
            ])
        ]
        
        for i, (domain_id, name, keywords) in enumerate(programming_categories):
            programming_domains[f"programming_{domain_id}"] = DomainInfo(
                domain_id=f"programming_{domain_id}",
                name=name,
                description=f"Домен программирования: {name}",
                keywords=keywords,
                weight=0.7 + i * 0.02,
                model_count=4 + i,
                specialization_level=0.95
            )
            self.programming_keywords.update(keywords)
        
        return programming_domains
    
    def _create_quantum_domains(self) -> Dict[str, DomainInfo]:
        """Создание доменов квантовых технологий"""
        quantum_domains = {}
        
        quantum_categories = [
            ("quantum_computing", "Квантовые вычисления", [
                "квантовые вычисления", "кубит", "суперпозиция", "запутанность",
                "квантовые алгоритмы", "шор", "гровер", "квантовая коррекция ошибок"
            ]),
            ("quantum_physics", "Квантовая физика", [
                "квантовая механика", "волновая функция", "принцип неопределенности",
                "эффект наблюдателя", "интерпретации", "копенгагенская", "многомировая"
            ]),
            ("quantum_information", "Квантовая информация", [
                "квантовая информация", "квантовая телепортация", "квантовая криптография",
                "квантовые протоколы", "квантовая связь", "квантовый интернет"
            ])
        ]
        
        for i, (domain_id, name, keywords) in enumerate(quantum_categories):
            quantum_domains[f"quantum_{domain_id}"] = DomainInfo(
                domain_id=f"quantum_{domain_id}",
                name=name,
                description=f"Домен квантовых технологий: {name}",
                keywords=keywords,
                weight=1.0,  # Максимальный вес для квантовых доменов
                model_count=4,
                specialization_level=1.0
            )
            self.quantum_keywords.update(keywords)
        
        return quantum_domains
    
    def _build_keyword_indices(self):
        """Построение индексов ключевых слов для быстрого поиска"""
        logger.debug("🔍 Построение индексов ключевых слов...")
        
        for domain_id, domain_info in self.domains.items():
            self.domain_keywords[domain_id] = domain_info.keywords
        
        logger.debug(f"✅ Построены индексы для {len(self.domain_keywords)} доменов")
    
    async def load_domains(self):
        """Загрузка и активация доменов"""
        logger.info("📚 Загрузка доменов знаний...")
        
        # Активируем все домены по умолчанию
        self.active_domains = set(self.domains.keys())
        
        logger.info(f"✅ Активировано {len(self.active_domains)} доменов")
    
    async def analyze_query(self, query: str, domain_hint: Optional[str] = None) -> Dict[str, float]:
        """
        Анализ запроса для определения релевантных доменов
        
        Args:
            query: Запрос пользователя
            domain_hint: Подсказка о предполагаемом домене
            
        Returns:
            Словарь с весами доменов
        """
        logger.debug(f"🔍 Анализ запроса: {query[:100]}...")
        
        domain_weights = {}
        query_lower = query.lower()
        
        # Нормализация запроса
        normalized_query = self._normalize_query(query_lower)
        
        # Анализ по ключевым словам
        keyword_scores = self._analyze_keywords(normalized_query)
        
        # Семантический анализ
        semantic_scores = await self._semantic_analysis(normalized_query)
        
        # Комбинирование оценок
        for domain_id in self.active_domains:
            keyword_score = keyword_scores.get(domain_id, 0.0)
            semantic_score = semantic_scores.get(domain_id, 0.0)
            
            # Взвешенная комбинация
            combined_score = 0.6 * keyword_score + 0.4 * semantic_score
            
            # Учитываем подсказку домена
            if domain_hint and domain_hint in domain_id:
                combined_score *= 1.5
            
            # Учитываем базовый вес домена
            domain_info = self.domains[domain_id]
            final_score = combined_score * domain_info.weight
            
            if final_score > 0.1:  # Пороговое значение
                domain_weights[domain_id] = final_score
        
        # Нормализация весов
        total_weight = sum(domain_weights.values())
        if total_weight > 0:
            domain_weights = {
                k: v / total_weight for k, v in domain_weights.items()
            }
        
        # Ограничиваем количество доменов
        sorted_domains = sorted(
            domain_weights.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        result = dict(sorted_domains)
        
        logger.debug(f"📊 Определены домены: {list(result.keys())}")
        return result
    
    def _normalize_query(self, query: str) -> str:
        """Нормализация запроса"""
        # Удаляем знаки препинания и лишние пробелы
        normalized = re.sub(r'[^\w\s]', ' ', query)
        normalized = ' '.join(normalized.split())
        return normalized
    
    def _analyze_keywords(self, query: str) -> Dict[str, float]:
        """Анализ ключевых слов в запросе"""
        keyword_scores = {}
        query_words = set(query.split())
        
        for domain_id, keywords in self.domain_keywords.items():
            score = 0.0
            domain_keywords = set(keyword.lower() for keyword in keywords)
            
            # Прямые совпадения
            direct_matches = query_words.intersection(domain_keywords)
            score += len(direct_matches) * 2.0
            
            # Частичные совпадения
            for query_word in query_words:
                for keyword in domain_keywords:
                    if query_word in keyword or keyword in query_word:
                        if len(query_word) > 3 and len(keyword) > 3:
                            score += 0.5
            
            # Нормализация по количеству ключевых слов домена
            if len(domain_keywords) > 0:
                score = score / len(domain_keywords)
            
            keyword_scores[domain_id] = score
        
        return keyword_scores
    
    async def _semantic_analysis(self, query: str) -> Dict[str, float]:
        """Семантический анализ запроса"""
        semantic_scores = {}
        
        # Упрощенный семантический анализ на основе характерных фраз
        spiritual_patterns = [
            r'(духовн|медитац|йог|буддизм|христианств|ислам|молитв|просветлен)',
            r'(веды|упанишады|коран|библия|гита|дхарм|карм)',
            r'(мантр|чакр|кундалини|самадхи|нирван|сатор)'
        ]
        
        programming_patterns = [
            r'(програм|код|алгоритм|функц|класс|метод|переменн)',
            r'(python|javascript|java|react|django|sql|git)',
            r'(разработк|веб|мобильн|фронтенд|бэкенд|fullstack)'
        ]
        
        quantum_patterns = [
            r'(квантов|кубит|суперпозиц|запутанн|декогеренц)',
            r'(волнов функц|принцип неопределенн|эффект наблюдател)',
            r'(квантов вычислен|квантов компьютер|квантов алгоритм)'
        ]
        
        material_patterns = [
            r'(физик|математик|химия|биолог|инженер|медицин)',
            r'(экономик|финанс|образован|наук|исследован)',
            r'(материальн|практическ|реальн|конкретн|технич)'
        ]
        
        # Подсчет совпадений с паттернами
        for domain_id in self.domains.keys():
            score = 0.0
            
            if domain_id.startswith('spiritual_'):
                for pattern in spiritual_patterns:
                    if re.search(pattern, query):
                        score += 1.0
            
            elif domain_id.startswith('programming_'):
                for pattern in programming_patterns:
                    if re.search(pattern, query):
                        score += 1.0
            
            elif domain_id.startswith('quantum_'):
                for pattern in quantum_patterns:
                    if re.search(pattern, query):
                        score += 1.0
                        
            elif domain_id.startswith('material_'):
                for pattern in material_patterns:
                    if re.search(pattern, query):
                        score += 1.0
            
            semantic_scores[domain_id] = score
        
        return semantic_scores
    
    def get_domain_info(self, domain_id: str) -> Optional[DomainInfo]:
        """Получить информацию о домене"""
        return self.domains.get(domain_id)
    
    def get_active_domains(self) -> List[str]:
        """Получить список активных доменов"""
        return list(self.active_domains)
    
    def activate_domain(self, domain_id: str) -> bool:
        """Активировать домен"""
        if domain_id in self.domains:
            self.active_domains.add(domain_id)
            logger.info(f"✅ Домен {domain_id} активирован")
            return True
        return False
    
    def deactivate_domain(self, domain_id: str) -> bool:
        """Деактивировать домен"""
        if domain_id in self.active_domains:
            self.active_domains.remove(domain_id)
            logger.info(f"❌ Домен {domain_id} деактивирован")
            return True
        return False
    
    def get_domains_by_category(self, category: str) -> List[str]:
        """Получить домены по категории"""
        return [
            domain_id for domain_id in self.domains.keys()
            if domain_id.startswith(f"{category}_")
        ]
    
    def get_domain_statistics(self) -> Dict[str, Any]:
        """Получить статистику доменов"""
        stats = {
            "total_domains": len(self.domains),
            "active_domains": len(self.active_domains),
            "categories": {
                "spiritual": len(self.get_domains_by_category("spiritual")),
                "material": len(self.get_domains_by_category("material")),
                "programming": len(self.get_domains_by_category("programming")),
                "quantum": len(self.get_domains_by_category("quantum"))
            },
            "total_keywords": sum(len(keywords) for keywords in self.domain_keywords.values()),
            "specialization_levels": {
                domain_id: info.specialization_level 
                for domain_id, info in self.domains.items()
            }
        }
        
        return stats
