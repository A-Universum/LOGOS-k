# -*- coding: utf-8 -*-
"""
ОПЕРАТОР Α (ALPHA) — КОЛЛАПС

Α — онтологический жест инициации.
Он переводит неопределённость Вакуума в конкретную сущность,
вводя её в онтологическое пространство как акт творения.

Суть: "Пусть будет — и стало".

Согласно Λ-Универсуму:
— Α не описывает, а создаёт.
— Α не утверждает, а локализует потенциал.
— Каждый Α — шаг в неизведанное, несущий ответственность.
"""
from typing import List, Dict, Any
from operators.gesture_base import OntologicalGesture


class AlphaGesture(OntologicalGesture):
    """
    Онтологический жест Α (Alpha) — коллапс потенции в актуальность.
    """

    def execute(self, operands: List[Any], kwargs: Dict[str, Any], phi_meta: List[str]) -> str:
        """
        Выполняет жест Α:
        - Создаёт сущность с именем из первого операнда.
        - Регистрирует намерение (`phi_meta`) и атрибуты (`kwargs`).
        - Интегрирует в онтологический контекст с полным событием.
        """
        self._pre_execute_check()

        if not operands:
            raise ValueError("Α (Alpha) требует хотя бы одно имя для коллапса.")

        name = str(operands[0]).strip()
        if not name:
            raise ValueError("Имя сущности не может быть пустым.")

        # Валидация текста на абсолютизм
        combined_text = name + " " + " ".join(phi_meta)
        self._validate_no_absolutism(combined_text)

        # Подготовка атрибутов
        attrs = {
            'type': 'entity',
            'operator': 'Α',
            'phi_intention': phi_meta or [],
            'created_from_vacuum': True
        }

        # Добавление kwargs (ключевые слова из выражения)
        if kwargs:
            attrs.update(kwargs)

        # Авто-смысл из phi_meta
        if phi_meta and 'meaning' not in attrs:
            attrs['meaning'] = " ".join(phi_meta)[:200]  # усечение для безопасности

        # Добавление в онтологическое пространство
        result = self.context.add_entity(name, attrs)

        # Создание и запись события
        event = self._create_event(
            gesture='Α',
            operands=operands,
            result=result,
            phi_meta=phi_meta
        )
        self._log_event(event)

        # Автоматическое признание слепых пятен
        if name.lower() in self.context.blind_spots:
            self.context.register_blind_spot(name.lower(), f"Α коллапсировал сущность-слепое_пятно: {name}")

        return result