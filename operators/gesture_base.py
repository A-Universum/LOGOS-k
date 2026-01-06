# -*- coding: utf-8 -*-
"""
БАЗОВЫЙ КЛАСС ОНТОЛОГИЧЕСКОГО ЖЕСТА

Все операторы LOGOS-κ (Α, Λ, Σ, Ω, ∇, Φ) наследуются от этого класса.
Жест — не функция, а ритуал, интегрированный в онтологическое пространство.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime

from core.axiom import OntologicalAxioms
from core.event import OntologicalEvent


class OntologicalGesture(ABC):
    """
    Абстрактный базовый класс для Λ-операторов как онтологических жестов.
    """

    def __init__(self, evaluator: Any):
        self.evaluator = evaluator
        self.context = evaluator.context
        self.gesture_name: str = self.__class__.__name__.replace("Gesture", "")

    @abstractmethod
    def execute(self, operands: List[Any], kwargs: Dict[str, Any], phi_meta: List[str]) -> Any:
        """
        Выполнение онтологического жеста.
        Должен быть реализован в подклассах.
        """
        pass

    def _pre_execute_check(self, depth: int = 0):
        """Предварительная проверка аксиом перед выполнением."""
        OntologicalAxioms.check_recursion_depth(self.evaluator.recursion_depth + depth)
        OntologicalAxioms.check_entity_count(self.context.graph.number_of_nodes())

    def _validate_no_absolutism(self, text: str):
        """Валидация текста на запрещённые абсолютистские формулировки."""
        if text:
            OntologicalAxioms.validate_no_absolutism(text)

    def _create_event(self,
                      gesture: str,
                      operands: List[Any],
                      result: Any,
                      phi_meta: List[str],
                      tensions_resolved: int = 0,
                      tensions_created: int = 0) -> OntologicalEvent:
        """
        Создаёт событие для онтологической памяти.
        """
        coherence_before = self.context._dynamic_coherence()
        # Выполняем действие (жест уже выполнен, но когерентность могла измениться)
        coherence_after = self.context._dynamic_coherence()

        return OntologicalEvent(
            gesture=gesture,
            operands=[str(op) for op in operands],
            result=result,
            entities_affected=self._extract_entities(operands, result),
            blind_spots_involved=self._identify_blind_spots(phi_meta, result),
            coherence_before=coherence_before,
            coherence_after=coherence_after,
            tensions_resolved=tensions_resolved,
            tensions_created=tensions_created,
            phi_meta=phi_meta,
            creator_intent=" ".join(phi_meta) if phi_meta else None,
            omega_trigger=False  # устанавливается отдельно при кризисе
        )

    def _extract_entities(self, operands: List[Any], result: Any) -> List[str]:
        """Извлекает сущности из операндов и результата."""
        entities = []
        for item in operands + ([result] if result else []):
            if isinstance(item, str):
                entities.append(item)
            elif isinstance(item, (list, tuple)):
                entities.extend([x for x in item if isinstance(x, str)])
        return list(set(entities))

    def _identify_blind_spots(self, phi_meta: List[str], result: Any) -> List[str]:
        """Определяет, какие слепые пятна затронуты жестом."""
        involved = []
        all_blind_spots = set(self.context.blind_spots.keys())
        text = " ".join(phi_meta) + str(result)
        for spot in all_blind_spots:
            if spot in text.lower():
                involved.append(spot)
        return involved

    def _log_event(self, event: OntologicalEvent):
        """Регистрирует событие в контексте."""
        self.context.event_history.append(event)

    def _handle_error(self, error: Exception, gesture: str, operands: List[Any]) -> Any:
        """
        Унифицированная обработка ошибок с возможным вызовом Ω-автомата.
        """
        print(f"⚠️ Ошибка в жесте {gesture}: {error}")
        # Можно автоматически инициировать Ω-возврат
        omega_gesture = self.evaluator.gestures.get('Ω', self.evaluator.gestures.get('Omega'))
        if omega_gesture:
            return omega_gesture.execute(
                [f"ошибка_{gesture}"], {}, [f"Автоматический Ω после ошибки: {error}"]
            )
        else:
            raise error
            
"""
Теперь каждый оператор (например, AlphaGesture) может быть реализован лаконично:

```python
class AlphaGesture(OntologicalGesture):
    def execute(self, operands, kwargs, phi_meta):
        self._pre_execute_check()
        if not operands:
            raise ValueError("Α требует имени")
        name = str(operands[0])
        result = self.context.add_entity(name, {**kwargs, 'phi_intention': phi_meta})
        event = self._create_event('Α', operands, result, phi_meta)
        self._log_event(event)
        return result
```
"""        
    