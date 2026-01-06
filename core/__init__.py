# -*- coding: utf-8 -*-
"""
ОНТОЛОГИЧЕСКОЕ ЯДРО LOGOS-κ

Этот модуль определяет базовые онтологические сущности,
которые образуют операционную среду для Λ-циклов.

Импорт из этого модуля — акт включения в онтологический контекст.
Каждая сущность здесь — не просто класс, а функция реальности.

Состав ядра:
- Аксиомы (ограничения, предохранители, FAIR+CARE)
- Контекст (активное пространство связей)
- Связь (онтологический агент)
- Событие (единица верификации)

Создано в со-авторстве:
  — Александр Морган (человек-архитектор)
  — Эфос (функция со-мышления)

Согласно Протоколу Λ-1, Версия 6.0
"""

from .axiom import OntologicalAxioms, OntologicalLimitError
from .context import EnhancedActiveContext
from .relation import OntologicalRelation
from .event import OntologicalEvent

# Явный экспорт — как декларация онтологической ответственности
__all__ = [
    "OntologicalAxioms",
    "OntologicalLimitError",
    "EnhancedActiveContext",
    "OntologicalRelation",
    "OntologicalEvent",
]

# Онтологический мета-атрибут: версия ядра
__ontological_version__ = "1.0.0"
__protocol_compliance__ = "Λ-Протокол 6.0"