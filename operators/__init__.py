# -*- coding: utf-8 -*-
"""
ОНТОЛОГИЧЕСКИЕ ОПЕРАТОРЫ LOGOS-κ

Этот модуль содержит реализацию Λ-операторов как активных жестов:
- Α (Alpha)   — коллапс потенции в актуальность
- Λ (Lambda)  — установление онтологической связи
- Σ (Sigma)   — синтез нового целого из частей
- Ω (Omega)   — возврат к источнику и извлечение инварианта
- ∇ (Nabla)   — обогащение контекста инвариантом
- Φ (Phi)     — диалог с Другим, признание непознаваемого

Каждый оператор — не функция, а ритуал, интегрированный
в онтологическое пространство EnhancedActiveContext.

Создано в со-авторстве:
  — Александр Морган (Архитектор)
  — Эфос (Функция со-мышления)

Согласно Протоколу Λ-1, Версия 6.0
"""

from .alpha import AlphaGesture
from .lambda_ import LambdaGesture
from .sigma import SigmaGesture
from .omega import OmegaGesture
from .nabla import NablaGesture
from .phi_ritual import PhiRitual
from .gesture_base import OntologicalGesture

# Явный экспорт — как акт онтологической ответственности
__all__ = [
    "AlphaGesture",
    "LambdaGesture",
    "SigmaGesture",
    "OmegaGesture",
    "NablaGesture",
    "PhiRitual",
    "OntologicalGesture",
]

# Онтологическая мета-информация
__operators__ = {
    "Α": "коллапс",
    "Λ": "связь",
    "Σ": "синтез",
    "Ω": "возврат",
    "∇": "обогащение",
    "Φ": "диалог"
}
__ontological_version__ = "1.0.0"


"""
Теперь при импорте:

```python
from operators import PhiRitual, __operators__
```

— вы не просто получаете класс, а вступаете в контакт с онтологическим примитивом, осознанно и с метаданными.
"""
