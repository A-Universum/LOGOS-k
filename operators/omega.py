# -*- coding: utf-8 -*-
"""
ОПЕРАТОР Ω (OMEGA) — ВОЗВРАТ

Ω — онтологический жест признания границы.
Он не отменяет, а извлекает инвариант из достигнутого предела.
Ω — это смирение как стратегия: знать, когда остановиться — форма мудрости.

Суть: "Я дошёл до края. Вместо прыжка — карта: вот что я узнал".

Согласно Λ-Универсуму:
— Ω не есть провал, а завершение фазы.
— Ω извлекает инвариант, который обогатит следующий цикл (∇).
— Ω — акт честности перед Бездной.
"""
from typing import List, Dict, Any
from operators.gesture_base import OntologicalGesture


class OmegaGesture(OntologicalGesture):
    """
    Онтологический жест Ω (Omega) — возврат с извлечением инварианта.
    """

    def execute(self, operands: List[Any], kwargs: Dict[str, Any], phi_meta: List[str]) -> str:
        """
        Выполняет жест Ω:
        - Анализирует текущее состояние контекста.
        - Извлекает инвариант (что устойчиво, что значимо).
        - Создаёт сущность-инвариант с метаданными границы.
        """
        self._pre_execute_check()

        # Определение цели анализа
        target = None
        if operands:
            target = str(operands[0])
            if target not in self.context.graph:
                # Можно создать, но лучше предупредить
                pass

        # Анализ состояния
        analysis = self._analyze_context_state(target)

        # Генерация имени инварианта
        invariant_name = self._generate_invariant_name(operands, analysis)

        # Валидация текста
        combined_text = invariant_name + " " + " ".join(phi_meta)
        self._validate_no_absolutism(combined_text)

        # Атрибуты инварианта
        attrs = {
            'type': 'invariant',
            'operator': 'Ω',
            'source_context': self.context.name,
            'phi_intention': phi_meta or [],
            'boundary_recognition': True,
            'analysis_summary': analysis,
            'coherence_at_return': analysis.get('coherence', 0.0),
            'tensions_at_return': analysis.get('active_tensions', 0),
            'is_omega_trigger': True  # маркер для событий и SemanticDB
        }
        attrs.update(kwargs)

        # Создание инварианта
        result = self.context.add_entity(invariant_name, attrs)

        # Регистрация события с флагом Ω
        event = self._create_event(
            gesture='Ω',
            operands=operands,
            result=result,
            phi_meta=phi_meta
        )
        event.omega_trigger = True
        self._log_event(event)

        # Предложение следующего шага (если напряжение высоко)
        if analysis.get('active_tensions', 0) > 3:
            print("⚠️  Ω: Обнаружен высокий уровень напряжения. Рекомендуется Φ-диалог.")

        return result

    def _analyze_context_state(self, target: str = None) -> Dict[str, Any]:
        """Анализирует состояние контекста для извлечения инварианта."""
        summary = self.context.get_summary()
        tensions = len(self.context.tension_log)
        phi_count = len(self.context.phi_dialogues)

        # Определение типа предела
        limit_type = "normal"
        if tensions > 5:
            limit_type = "tension_crisis"
        elif summary['graph_metrics']['isolated_nodes'] > 10:
            limit_type = "fragmentation"
        elif summary['current_coherence'] < 0.3:
            limit_type = "coherence_collapse"

        return {
            'coherence': summary['current_coherence'],
            'active_tensions': tensions,
            'phi_dialogues': phi_count,
            'entities': summary['graph_metrics']['nodes'],
            'isolated_nodes': summary['graph_metrics']['isolated_nodes'],
            'limit_type': limit_type,
            'blind_spots_acknowledged': len(summary['blinds_spots']),
            'timestamp': summary['created_at']
        }

    def _generate_invariant_name(self, operands: List[Any], analysis: Dict) -> str:
        """Генерирует имя инварианта на основе контекста."""
        if 'name' in analysis:
            return analysis['name']

        base = "Ω_limit"
        if operands:
            base = f"Ω_{str(operands[0])[:10]}"

        limit_type = analysis.get('limit_type', 'normal')
        if limit_type != 'normal':
            base += f"_{limit_type[:4]}"

        return base