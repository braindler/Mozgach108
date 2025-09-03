# Установка Mozgach2

## Требования к системе

### Минимальные требования
- **RAM**: 8GB
- **GPU**: 4GB VRAM (CUDA 11.0+)
- **Storage**: 50GB свободного места
- **Python**: 3.8+

### Рекомендуемые требования  
- **RAM**: 32GB+
- **GPU**: 8GB+ VRAM
- **Storage**: 100GB SSD
- **Python**: 3.10+

## Пошаговая установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-org/mozgach2.git
cd Mozgach2
```

### 2. Создание виртуального окружения
```bash
python -m venv mozgach2_env
source mozgach2_env/bin/activate  # Linux/macOS
# или
mozgach2_env\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Проверка установки
```bash
python test_system.py
```

## Конфигурация

### Настройка путей
Отредактируйте `config.py` для изменения путей к моделям и данным.

### Настройка GPU
Убедитесь, что CUDA установлен и доступен:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

## Загрузка моделей

### Автоматическая загрузка
Система автоматически загружает критические модели при запуске.

### Ручная загрузка
```python
from src.mozgach2_system import Mozgach2System

system = Mozgach2System(auto_load_models=False)
await system.model_manager.load_model("mozgach2_general_01")
```

## Устранение неполадок

### Проблемы с памятью
- Уменьшите количество одновременно загруженных моделей
- Используйте on-demand загрузку
- Проверьте доступную RAM

### Проблемы с GPU
- Убедитесь в совместимости версий CUDA
- Проверьте драйверы NVIDIA
- Используйте CPU-only режим при необходимости

## Тестирование

Запустите полный набор тестов:
```bash
python test_system.py
```

## Поддержка

При возникновении проблем создайте issue в репозитории или обратитесь к документации.
