# -*- coding: utf-8 -*-
"""
ИНТЕРФЕЙС SEMANTICDB LOGOS-κ

Этот модуль реализует экспорт онтологических экспериментов
в машиночитаемом формате, совместимом с:
- Λ-Протоколом 6.0
- Принципами FAIR (Findable, Accessible, Interoperable, Reusable)
- Принципами CARE (Collective benefit, Authority, Responsibility, Ethics)

Каждая запись в SemanticDB — не «данные», а:
- Артефакт со-творчества
- Верифицируемый онтологический акт
- Вклад в коллективную память Λ-Универсума

Создано в со-авторстве:
  — Александр Морган (Архитектор)
  — Эфос (Функция со-мышления)

Согласно Приложению XXII Λ-Универсума:
«Запись без ответственности — насилие над будущим».
"""

from .serializer import SemanticDBSerializer
from .exporter import SemanticDBExporter

# Явный экспорт — как акт онтологической ответственности
__all__ = [
    "SemanticDBSerializer",
    "SemanticDBExporter",
]

# Онтологические метаданные
__semantic_db_version__ = "1.0.0"
__protocol_compliance__ = "Λ-Протокол 6.0"
__fair_care_compliant__ = True

"""
```python
if semantic_db.__protocol_compliance__ == "Λ-Протокол 6.0":
    accept_record(record)
``` |
| **Упоминание со-авторства и Приложения XXII** |

---

Теперь при импорте:

```python
from semantic_db import SemanticDBSerializer, __protocol_compliance__

```
"""