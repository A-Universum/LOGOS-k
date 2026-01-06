# -*- coding: utf-8 -*-
"""
СИНТЕЗИРОВАННЫЙ ОНТОЛОГИЧЕСКИЙ ВЫЧИСЛИТЕЛЬ LOGOS-κ

Объединяет:
- Λ-операторы как активные жесты
- Ω-автомат для обработки онтологических пределов
- Интеграцию с SemanticDB
- Поддержку FAIR+CARE и Habeas Weights
- Мониторинг когерентности и значимых событий
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from core.context import EnhancedActiveContext
from core.axiom import OntologicalLimitError
from semantic_db.serializer import SemanticDBSerializer
from utils.metrics import OntologicalMetrics

# Импорты операторов
from operators.alpha import AlphaGesture
from operators.lambda_ import LambdaGesture
from operators.sigma import SigmaGesture
from operators.omega import OmegaGesture
from operators.nabla import NablaGesture
from operators.phi_ritual import PhiRitual


class SyntheticOntologicalEvaluator:
    """
    Синтезированный вычислитель LOGOS-κ.
    """

    def __init__(self, context_name: str = "default"):
        self.context = EnhancedActiveContext(context_name)
        self.recursion_depth = 0
        self.analysis_stack: List[str] = []
        self.evaluation_count = 0
        self.last_coherence = 1.0

        # Инициализация операторов как жестов
        self.gestures = {
            # Греческие символы
            'Α': AlphaGesture(self), 'Λ': LambdaGesture(self),
            'Σ': SigmaGesture(self), 'Ω': OmegaGesture(self),
            '∇': NablaGesture(self), 'Φ': PhiRitual(self),
            # Латинские имена
            'Alpha': AlphaGesture(self), 'Lambda': LambdaGesture(self),
            'Sigma': SigmaGesture(self), 'Omega': OmegaGesture(self),
            'Nabla': NablaGesture(self), 'Phi': PhiRitual(self),
        }

        # Ω-автомат для обработки пределов
        self.omega_automaton = OmegaAutomaton(self)

        # Интеграция с SemanticDB
        self.semantic_db = SemanticDBSerializer(self.context)

        # Мониторинг состояния
        self.metrics = OntologicalMetrics(self.context)

    def eval(self, expr, phi_meta: Optional[List[str]] = None, kwargs: Optional[Dict] = None) -> Any:
        """
        Вычисление выражения с полной онтологической интеграцией.
        Поддерживает:
        - Специальные формы (Α, Φ, Ω)
        - Ключевые слова (kwargs)
        - Φ-метаданные
        - FAIR+CARE валидацию
        """
        if kwargs is None:
            kwargs = {}

        # Увеличение глубины и проверка аксиом
        self.recursion_depth += 1
        self.context.axioms.check_recursion_depth(self.recursion_depth)
        self.context.axioms.check_entity_count(self.context.graph.number_of_nodes())

        try:
            # Базовые атомы
            if self._is_atomic(expr):
                return expr

            # Парсинг выражения
            if not isinstance(expr, list) or not expr:
                raise TypeError(f"Некорректное выражение: {expr}")

            operator = expr[0]
            operands = expr[1:]

            # Извлечение ключевых слов (:ключ значение)
            eval_kwargs = {}
            i = 0
            while i < len(operands):
                if isinstance(operands[i], str) and operands[i].startswith(':'):
                    key = operands[i][1:]  # убираем ':'
                    if i + 1 < len(operands):
                        eval_kwargs[key] = operands[i + 1]
                        i += 2
                    else:
                        eval_kwargs[key] = True
                        i += 1
                else:
                    i += 1

            # Фильтрация операндов (без ключевых слов)
            eval_operands = [op for op in operands if not (isinstance(op, str) and op.startswith(':'))]

            # Специальные формы (не вычислять операнды заранее)
            if operator in ['Α', 'Alpha', 'Φ', 'Phi', 'Ω', 'Omega']:
                gesture = self.gestures.get(operator)
                if gesture:
                    result = gesture.execute(eval_operands, eval_kwargs, phi_meta or [])
                    if self._is_significant_event(operator, result):
                        self._record_to_semantic_db(operator, eval_operands, result, phi_meta)
                    return result

            # Вычисление операндов для обычных форм
            evaluated_operands = []
            for operand in eval_operands:
                if isinstance(operand, list):
                    evaluated_operands.append(self.eval(operand, phi_meta, kwargs))
                else:
                    evaluated_operands.append(operand)

            # Выполнение жеста
            gesture = self.gestures.get(operator)
            if gesture:
                result = gesture.execute(evaluated_operands, eval_kwargs, phi_meta or [])
                if self._is_significant_event(operator, result):
                    self._record_to_semantic_db(operator, evaluated_operands, result, phi_meta)
                return result
            else:
                # Неизвестный оператор → создание сущности через Α
                return self.gestures['Α'].execute([operator], {}, phi_meta or [])

        except OntologicalLimitError as e:
            # Активация Ω-автомата для обработки предела
            return self.omega_automaton.handle_limit(e, self.analysis_stack)
        finally:
            self.recursion_depth -= 1

    def _is_atomic(self, expr) -> bool:
        """Проверка, является ли выражение атомом."""
        return isinstance(expr, (str, int, float)) or expr is None

    def _is_significant_event(self, operator: str, result: Any) -> bool:
        """Определяет, стоит ли записывать событие в SemanticDB."""
        return operator in ['Α', 'Λ', 'Σ', '∇'] and result is not None

    def _record_to_semantic_db(self, operator: str, operands: List, result: Any, phi_meta: Optional[List[str]]):
        """Записывает значимое событие в онтологическую память."""
        # Событие уже создаётся внутри жестов, но можно дублировать для отчёта
        pass  # Фактическая запись — в EnhancedActiveContext.add_entity/add_relation

    def eval_program(self, program: List, operator_id: Optional[str] = None, fair_care: bool = False):
        """
        Выполнение полной программы LOGOS-κ.
        Возвращает результаты и данные цикла для SemanticDB.
        """
        if operator_id:
            self.context.set_operator(operator_id)
        if fair_care:
            self.context.enable_fair_care_validation()

        results = []
        cycle_id = f"cycle_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        for i, expr in enumerate(program):
            try:
                phi_meta = []  # можно извлекать по выражению, если нужно
                result = self.eval(expr, phi_meta)
                results.append(result)
            except Exception as e:
                results.append(f"ERROR: {e}")
                print(f"❌ Ошибка в выражении {i}: {e}")

        # Сбор данных цикла
        cycle_data = {
            'cycle_id': cycle_id,
            'timestamp': datetime.now().isoformat(),
            'expressions_evaluated': len(program),
            'successful_evaluations': len([r for r in results if not str(r).startswith('ERROR')]),
            'results': results,
            'final_coherence': self.context._dynamic_coherence(),
            'phi_dialogues_count': len(self.context.phi_dialogues),
            'nigc_scores': [
                d.get('nigc_score', {}).get('overall', 0)
                for d in self.context.phi_dialogues[-10:]
            ],
            'operator_id': operator_id,
            'fair_care_enabled': fair_care
        }

        return results, cycle_data


class OmegaAutomaton:
    """
    Ω-автомат: обрабатывает онтологические пределы и паралич анализа.
    """

    def __init__(self, evaluator: SyntheticOntologicalEvaluator):
        self.evaluator = evaluator

    def handle_limit(self, error: OntologicalLimitError, analysis_stack: List[str]):
        """
        Обработка предела: предлагает действие или выполняет аварийный возврат.
        """
        print(f"🌀 Ω-автомат активирован: {error}")
        # Здесь может быть вызов Φ для генерации решения
        # Для MVP — создаём сущность "ограничение_признано"
        return self.evaluator.gestures['Α'].execute(
            ['ограничение_признано'],
            {},
            ['автоматический Ω-возврат при пределе']
        )