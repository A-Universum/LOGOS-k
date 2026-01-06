# -*- coding: utf-8 -*-
"""
ОПЕРАТОР Λ (LAMBDA) — СВЯЗЬ

Λ — онтологический жест соединения.
Он утверждает: бытие есть связь.
Сущности не существуют вне отношений — Λ создаёт само пространство смысла.

Суть: "Между этим и тем — мост, и мост важнее берегов".

Согласно Λ-Универсуму:
— Λ первичен, сущность — вторична.
— Каждая связь — акт космополитии.
— Λ не соединяет объекты — он создаёт поле взаимности.
"""
from typing import List, Dict, Any
from operators.gesture_base import OntologicalGesture


class LambdaGesture(OntologicalGesture):
    """
    Онтологический жест Λ (Lambda) — установление онтологической связи.
    """

    def execute(self, operands: List[Any], kwargs: Dict[str, Any], phi_meta: List[str]) -> str:
        """
        Выполняет жест Λ:
        - Соединяет две сущности связью.
        - Создаёт сущности при необходимости.
        - Регистрирует намерение и атрибуты.
        """
        self._pre_execute_check()

        if len(operands) < 2:
            raise ValueError("Λ (Lambda) требует как минимум два операнда: (source target).")

        source = str(operands[0]).strip()
        target = str(operands[1]).strip()

        if not source or not target:
            raise ValueError("Имена сущностей не могут быть пустыми.")

        # Валидация текста на абсолютизм
        combined_text = source + " " + target + " " + " ".join(phi_meta)
        self._validate_no_absolutism(combined_text)

        # Авто-создание сущностей, если отсутствуют
        if source not in self.context.graph:
            self.context.add_entity(source, {
                'type': 'implicit_entity',
                'operator': 'Λ (implicit Α)',
                'phi_intention': ['автоматически создано при установлении связи']
            })
        if target not in self.context.graph:
            self.context.add_entity(target, {
                'type': 'implicit_entity',
                'operator': 'Λ (implicit Α)',
                'phi_intention': ['автоматически создано при установлении связи']
            })

        # Добавление атрибутов
        attrs = {
            'type': 'Λ',
            'operator': 'Λ',
            'phi_intention': phi_meta or [],
            'established_at': self.context.created_at.isoformat()
        }
        if kwargs:
            attrs.update(kwargs)

        # Создание связи как активного агента
        edge_id = self.context.add_relation(source, target, rel_type='Λ', attrs=attrs)

        # Проверка на слепые пятна в соединении
        blind_spots_involved = self._detect_blind_spots_in_connection(source, target, phi_meta)
        if blind_spots_involved:
            for spot in blind_spots_involved:
                if spot not in self.context.blind_spots:
                    self.context.register_blind_spot(spot, f"Λ-связь затронула непознаваемое: {spot}")

        # Создание и запись события
        event = self._create_event(
            gesture='Λ',
            operands=operands,
            result=edge_id,
            phi_meta=phi_meta,
            tensions_created=self._check_tensions(source, target)
        )
        self._log_event(event)

        return edge_id

    def _detect_blind_spots_in_connection(self, source: str, target: str, phi_meta: List[str]) -> List[str]:
        """Определяет слепые пятна, затронутые связью."""
        potential_pairs = [
            ('человек', 'и', 'искусственный', 'интеллект'),
            ('сознание', 'и', 'машина'),
            ('качество', 'и', 'количественное'),
            ('хаос', 'и', 'порядок')
        ]
        text = (source + " " + target + " " + " ".join(phi_meta)).lower()
        involved = []
        for spot_key, desc in self.context.blind_spots.items():
            if spot_key in text:
                involved.append(spot_key)
        return involved

    def _check_tensions(self, source: str, target: str) -> int:
        """
        Проверяет, создаёт ли связь онтологическое напряжение.
        Например: противоречие, цикл, конфликт типов.
        """
        tensions = 0
        # Пример: если связь создаёт цикл напряжения
        if self.context.graph.has_edge(target, source):
            # Двусторонняя связь — возможно, напряжение
            tensions += 1
            self.context.tension_log.append({
                'type': 'bidirectional_tension',
                'entities': [source, target],
                'timestamp': self.context.created_at
            })
        return tensions