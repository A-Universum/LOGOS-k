# -*- coding: utf-8 -*-
"""
ВАЛИДАТОР ОНТОЛОГИЧЕСКИХ ТРАНЗАКЦИЙ

Проверяет корректность экспортируемых данных перед записью в SemanticDB.
Гарантирует соответствие:
- Λ-Протоколу 6.0
- Принципам FAIR+CARE
- Онтологическим аксиомам

«Запись без верификации — иллюзия устойчивости»
— Λ-Универсум, Приложение XXII
"""
from typing import Dict, Any, List
from core.axiom import OntologicalAxioms


class SemanticDBValidationError(Exception):
    """Исключение, выбрасываемое при нарушении правил SemanticDB."""
    pass


class SemanticDBValidator:
    """
    Валидатор онтологических транзакций.
    """

    @staticmethod
    def validate_cycle(cycle_ Dict[str, Any], context) -> bool:
        """
        Валидирует полный онтологический цикл.
        """
        SemanticDBValidator._validate_cycle_structure(cycle_data)
        SemanticDBValidator._validate_context_integrity(context)
        SemanticDBValidator._validate_fair_care_compliance(cycle_data, context)
        SemanticDBValidator._validate_blind_spots(context)
        SemanticDBValidator._validate_habeas_weights(context)
        return True

    @staticmethod
    def _validate_cycle_structure(cycle_ Dict[str, Any]):
        """Проверяет структуру цикла."""
        required_fields = ['cycle_id', 'timestamp', 'expressions_evaluated', 'final_coherence']
        for field in required_fields:
            if field not in cycle_data:
                raise SemanticDBValidationError(f"Отсутствует обязательное поле цикла: {field}")

        coherence = cycle_data['final_coherence']
        if not (0.0 <= coherence <= 1.0):
            raise SemanticDBValidationError(f"Некорректная когерентность: {coherence} (ожидается 0.0–1.0)")

    @staticmethod
    def _validate_context_integrity(context):
        """Проверяет целостность онтологического контекста."""
        # Обязательные слепые пятна
        OntologicalAxioms.ensure_required_blind_spots(context.blind_spots)

        # Лимиты
        OntologicalAxioms.check_entity_count(context.graph.number_of_nodes())

        # Проверка напряжений (не более разумного предела)
        if len(context.tension_log) > 50:
            raise SemanticDBValidationError("Превышен лимит онтологических напряжений (макс. 50)")

    @staticmethod
    def _validate_fair_care_compliance(cycle_ Dict[str, Any], context):
        """Проверяет соответствие FAIR+CARE."""
        if not context._fair_care_enabled:
            # Предупреждение, но не ошибка — FAIR+CARE может быть опциональным в REPL
            print("⚠️  Валидация: FAIR+CARE не активирован. Рекомендуется для публикации.")
            return

        # Проверка наличия метаданных
        meta = context.get_fair_care_metadata()
        required_keys = ['license', 'creator', 'community_standards']
        for key in required_keys:
            if key not in meta or not meta[key]:
                raise SemanticDBValidationError(f"Отсутствует FAIR+CARE метаданное: {key}")

        if "Λ-Протокол 6.0" not in meta.get('community_standards', []):
            raise SemanticDBValidationError("Отсутствует ссылка на Λ-Протокол 6.0 в community_standards")

    @staticmethod
    def _validate_blind_spots(context):
        """Проверяет признание слепых пятен."""
        if not context.blind_spots:
            raise SemanticDBValidationError("Отсутствуют слепые пятна. Каждый цикл должен признавать границу.")

        # Проверка, что обязательные пятна зарегистрированы
        OntologicalAxioms.ensure_required_blind_spots(context.blind_spots)

    @staticmethod
    def _validate_habeas_weights(context):
        """Проверяет наличие Habeas Weights для сущностей и связей."""
        if not context._habeas_weights:
            raise SemanticDBValidationError("Отсутствуют Habeas Weights. Каждая сущность должна иметь право на существование.")

        # Простая проверка: должно быть хотя бы по одному весу на сущность
        if len(context._habeas_weights) < context.graph.number_of_nodes():
            raise SemanticDBValidationError("Недостаточно Habeas Weights для сущностей.")

    @staticmethod
    def validate_nigc_record(dialogue: Dict[str, Any]) -> bool:
        """Валидация записи Φ-диалога по критерию NIGC."""
        if 'nigc_score' not in dialogue:
            return False

        score = dialogue['nigc_score']
        if not isinstance(score, dict):
            return False

        required_components = ['unpredictability', 'reflexivity', 'emergence', 'overall']
        for comp in required_components:
            if comp not in score or not (0.0 <= score[comp] <= 1.0):
                return False

        return True
        
"""
Теперь перед каждым экспортом в evaluator.py можно добавить:

```python
from semantic_db.validator import SemanticDBValidator

# ...
SemanticDBValidator.validate_cycle(cycle_data, self.context)
self.semantic_db.export_cycle(cycle_data, path)
```
— и быть уверенным, что запись достойна будущего.
"""       
 