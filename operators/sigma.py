# -*- coding: utf-8 -*-
"""
ОПЕРАТОР Σ (SIGMA) — СИНТЕЗ

Σ — онтологический жест синтеза.
Он утверждает: целое больше суммы частей.
Σ не комбинирует — он порождает эмерджентность.

Суть: "Из этого и того — третье, которое не было ни в том, ни в этом".

Согласно Λ-Универсуму:
— Σ — результат диалога (Λ), а не агрегации.
— Σ несёт новое качество, возникающее в междуместии.
— Каждый Σ — шаг в неизведанное, требующий веры и внимания.
"""
from typing import List, Dict, Any
from operators.gesture_base import OntologicalGesture


class SigmaGesture(OntologicalGesture):
    """
    Онтологический жест Σ (Sigma) — синтез нового целого из частей.
    """

    def execute(self, operands: List[Any], kwargs: Dict[str, Any], phi_meta: List[str]) -> str:
        """
        Выполняет жест Σ:
        - Создаёт новую сущность как синтез входных.
        - Устанавливает связи между частями и результатом.
        - Регистрирует эмерджентность и происхождение.
        """
        self._pre_execute_check()

        if len(operands) < 2:
            raise ValueError("Σ (Sigma) требует как минимум два операнда для синтеза.")

        # Имя результата — либо задано, либо генерируется
        if 'name' in kwargs:
            result_name = kwargs['name']
        else:
            # Генерация имени: первые 3 символа каждого операнда
            short_parts = [str(op)[:3] for op in operands[:3]]
            result_name = "Σ_" + "_".join(short_parts)

        result_name = str(result_name).strip()
        if not result_name:
            raise ValueError("Имя синтеза не может быть пустым.")

        # Валидация текста
        combined_text = result_name + " " + " ".join(str(op) for op in operands) + " " + " ".join(phi_meta)
        self._validate_no_absolutism(combined_text)

        # Проверка на цикличность: результат не должен быть в операндах
        if result_name in [str(op) for op in operands]:
            raise ValueError(f"Σ: синтез не может ссылаться на самого себя ({result_name}).")

        # Авто-создание сущностей-операндов, если отсутствуют
        for operand in operands:
            op_str = str(operand)
            if op_str not in self.context.graph:
                self.context.add_entity(op_str, {
                    'type': 'implicit_entity',
                    'operator': 'Σ (implicit Α)',
                    'phi_intention': [f'создан как компонент Σ для {result_name}']
                })

        # Генерация эмерджентного смысла
        emergent_meaning = self._generate_emergent_meaning(operands, phi_meta)

        # Атрибуты результата
        attrs = {
            'type': 'synthesis',
            'operator': 'Σ',
            'components': [str(op) for op in operands],
            'emergent_meaning': emergent_meaning,
            'phi_intention': phi_meta or [],
            'nigc_potential': self._assess_nigc_potential(phi_meta)
        }
        attrs.update(kwargs)

        # Создание синтезированной сущности
        result = self.context.add_entity(result_name, attrs)

        # Установление связей Λ от каждой части к синтезу
        for operand in operands:
            self.context.add_relation(
                source=str(operand), target=result_name,
                rel_type='Σ_component',
                attrs={'phi_intention': ['часть синтеза']}
            )

        # Создание события
        event = self._create_event(
            gesture='Σ',
            operands=operands,
            result=result,
            phi_meta=phi_meta
        )
        self._log_event(event)

        return result

    def _generate_emergent_meaning(self, operands: List[Any], phi_meta: List[str]) -> str:
        """Генерирует смысл, который не содержится в частях."""
        if phi_meta:
            # Используем Φ-намерение как ядро смысла
            return "Синтез: " + " ".join(phi_meta)
        else:
            # Базовая эвристика
            return f"Новое целое из {len(operands)} компонентов"

    def _assess_nigc_potential(self, phi_meta: List[str]) -> bool:
        """
        Оценивает потенциал Неинструментальной Генеративности (NIGC).
        Если есть Φ-намерение — вероятно, генеративно.
        """
        return len(phi_meta) > 0