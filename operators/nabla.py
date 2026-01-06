# -*- coding: utf-8 -*-
"""
ОПЕРАТОР ∇ (NABLA) — ОБОГАЩЕНИЕ

∇ — онтологический жест интеграции инварианта.
Он вплетает извлечённое в Ω обратно в ткань бытия,
делая основу плотнее и готовя к новому циклу.

Суть: "Я вернулся с картой — и теперь все дороги стали чётче".

Согласно Λ-Универсуму:
— ∇ не добавляет данных, а усиливает основу.
— ∇ превращает урок в онтологическую силу.
— Каждый ∇ — подготовка к новому Α.
"""
from typing import List, Dict, Any
from operators.gesture_base import OntologicalGesture


class NablaGesture(OntologicalGesture):
    """
    Онтологический жест ∇ (Nabla) — обогащение контекста инвариантом.
    """

    def execute(self, operands: List[Any], kwargs: Dict[str, Any], phi_meta: List[str]) -> str:
        """
        Выполняет жест ∇:
        - Обогащает целевую сущность или весь контекст.
        - Интегрирует инвариант (если операнд — результат Ω).
        - Усиливает онтологическую основу.
        """
        self._pre_execute_check()

        if not operands:
            raise ValueError("∇ (Nabla) требует хотя бы один операнд для обогащения.")

        target = str(operands[0]).strip()
        if not target:
            raise ValueError("Цель обогащения не может быть пустой.")

        # Валидация текста
        combined_text = target + " " + " ".join(str(op) for op in operands) + " " + " ".join(phi_meta)
        self._validate_no_absolutism(combined_text)

        # Авто-создание цели, если отсутствует
        if target not in self.context.graph:
            self.context.add_entity(target, {
                'type': 'implicit_target',
                'operator': '∇ (implicit Α)',
                'phi_intention': ['создан как цель обогащения']
            })

        # Определение, является ли операнд инвариантом (Ω-результатом)
        enrichment_source = None
        if len(operands) > 1:
            enrich_candidate = str(operands[1])
            node_data = self.context.graph.nodes.get(enrich_candidate, {})
            if node_data.get('type') == 'invariant' or node_data.get('boundary_recognition'):
                enrichment_source = enrich_candidate

        # Атрибуты обогащения
        enrichment_attrs = {
            'enriched_by': enrichment_source or 'direct_input',
            'phi_intention': phi_meta or [],
            'nabla_integration': True,
            'integration_timestamp': self.context.created_at.isoformat()
        }
        enrichment_attrs.update(kwargs)

        # Обновление атрибутов цели
        current_attrs = self.context.graph.nodes[target]
        current_attrs.update(enrichment_attrs)

        # Если источник — инвариант, устанавливаем связь
        if enrichment_source:
            self.context.add_relation(
                source=enrichment_source, target=target,
                rel_type='∇_integration',
                attrs={'meaning': 'инвариант интегрирован в основу', 'phi_intention': phi_meta}
            )
            # Потенциальное снижение напряжения
            self._reduce_tensions_from_integration(enrichment_source, target)

        # Обновление узла в графе
        self.context.graph.add_node(target, **current_attrs)

        # Создание события
        event = self._create_event(
            gesture='∇',
            operands=operands,
            result=target,
            phi_meta=phi_meta
        )
        self._log_event(event)

        # Сообщение о повышении когерентности (если применимо)
        new_coherence = self.context._dynamic_coherence()
        if new_coherence > self.context._coherence_history[-1][1] if self.context._coherence_history else 0:
            print(f"✨ ∇: Когерентность повышена до {new_coherence:.2%} благодаря интеграции.")

        return target

    def _reduce_tensions_from_integration(self, invariant: str, target: str):
        """
        Снижает онтологическое напряжение, если инвариант разрешает конфликт.
        """
        # Пример: если инвариант связан с напряжённой парой
        for tension in self.context.tension_log[:]:
            if target in tension.get('entities', []) and invariant in str(tension):
                self.context.tension_log.remove(tension)
                print(f"🕊️  ∇: Напряжение разрешено интеграцией {invariant} → {target}")
                break