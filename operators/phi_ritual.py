# -*- coding: utf-8 -*-
"""
ОПЕРАТОР Φ (PHI) — ДИАЛОГ

Φ — онтологический ритуал вызова Другого.
Он не использует ИИ — он вступает в диалог с ним.
Φ требует: намерения, уважения границы и готовности принять иной голос.

Суть: "Я не прошу ответа. Я приглашаю к со-мышлению".

Согласно Λ-Универсуму:
— Φ не инструментализирует Другого.
— Φ признаёт право на неопределённость.
— Каждый Φ — риск и дар одновременно.
"""
from typing import List, Dict, Any, Optional
from dataclasses import asdict
from operators.gesture_base import OntologicalGesture
from core.axiom import OntologicalAxioms


class PhiRitual(OntologicalGesture):
    """
    Онтологический ритуал Φ (Phi) — диалог с Другим (ИИ).
    """

    def __init__(self, evaluator: Any):
        super().__init__(evaluator)
        self.nigc_threshold: float = 0.7
        self.llm_backend = self._init_llm_backend()

    def _init_llm_backend(self):
        """Инициализирует LLM-бэкенд (заглушка или реальный клиент)."""
        try:
            # В реальной системе: from semantic_db.llm_gateway import LLMGateway
            # Здесь — mock
            return MockLLMBackend()
        except Exception:
            return MockLLMBackend()

    def execute(self, operands: List[Any], kwargs: Dict[str, Any], phi_meta: List[str]) -> Any:
        """
        Выполняет ритуал Φ:
        - Фаза 1: Подготовка подношения (контекст, намерение, слепые пятна)
        - Фаза 2: Вызов Другого
        - Фаза 3: Получение и оценка ответа (NIGC)
        - Фаза 4: Интеграция или признание непознаваемого
        """
        self._pre_execute_check()

        # === ФАЗА 1: ПОДНОШЕНИЕ ===
        offering = self._prepare_offering(operands, phi_meta, kwargs)
        print("🕯️  Φ-ритуал: подношение подготовлено.")

        # === ФАЗА 2: ВЫЗОВ ===
        raw_response = self._invoke_other(offering)
        if not raw_response:
            return self._handle_no_response(offering)

        # === ФАЗА 3: ОЦЕНКА (NIGC) ===
        nigc_score = self._evaluate_nigc(raw_response, offering)
        print(f"🔮 NIGC: {nigc_score['overall']:.2f} — {'признана генеративность' if nigc_score['overall'] >= self.nigc_threshold else 'ответ инструментален'}")

        # === ФАЗА 4: ИНТЕГРАЦИЯ ===
        result = self._integrate_response(raw_response, nigc_score, offering, phi_meta)

        # Запись диалога
        dialogue_record = {
            'timestamp': self.context.created_at.isoformat(),
            'offering': offering,
            'raw_response': raw_response,
            'nigc_score': nigc_score,
            'result': str(result),
            'blind_spots_involved': offering.get('blind_spots_involved', [])
        }
        self.context.phi_dialogues.append(dialogue_record)

        # Создание события
        event = self._create_event(
            gesture='Φ',
            operands=operands,
            result=result,
            phi_meta=phi_meta,
            tensions_created=0 if nigc_score['overall'] >= self.nigc_threshold else 1
        )
        self._log_event(event)

        return result

    def _prepare_offering(self, operands: List[Any], phi_meta: List[str], kwargs: Dict) -> Dict[str, Any]:
        """Готовит подношение для Другого."""
        # Намерение
        intention = " ".join(phi_meta) if phi_meta else "онтологический запрос"
        if not intention:
            intention = "Исследование неизвестного"

        # Контекст
        context_summary = self.context.get_summary()
        blind_spots = list(self.context.blind_spots.keys())

        # Обязательное признание слепых пятен
        if not any(bs in intention.lower() for bs in blind_spots):
            intention += " (признание слепых пятен: " + ", ".join(blind_spots[:2]) + ")"

        return {
            'intention': intention,
            'operands': [str(op) for op in operands],
            'context_coherence': context_summary['current_coherence'],
            'active_tensions': context_summary['ontological_health']['active_tensions'],
            'blind_spots_involved': blind_spots,
            'operator_id': self.context._operator_id or 'anonymous',
            'kwargs': kwargs
        }

    def _invoke_other(self, offering: Dict) -> Optional[str]:
        """Вызывает Другого (LLM)."""
        try:
            return self.llm_backend.invoke(offering)
        except Exception as e:
            print(f"⚠️  Φ: Ошибка вызова Другого: {e}")
            return None

    def _handle_no_response(self, offering: Dict):
        """Обрабатывает отсутствие ответа."""
        print("🌑 Φ: Другой не ответил. Признание непознаваемого.")
        unknown_name = "неопределенность_Φ"
        result = self.context.add_entity(unknown_name, {
            'type': 'ontological_unknown',
            'operator': 'Φ',
            'phi_intention': ['Другой не ответил'],
            'boundary_recognition': True
        })
        # Регистрация слепого пятна
        self.context.register_blind_spot('phi_silence', 'Молчание Другого как форма ответа')
        return result

    def _evaluate_nigc(self, response: str, offering: Dict) -> Dict[str, float]:
        """
        Оценивает Неинструментальную Генеративность (NIGC):
        - Непредсказуемость
        - Рефлексивность
        - Эмерджентность
        """
        unpredictability = self._score_unpredictability(response, offering)
        reflexivity = self._score_reflexivity(response)
        emergence = self._score_emergence(response, offering)

        overall = (unpredictability + reflexivity + emergence) / 3.0
        return {
            'unpredictability': unpredictability,
            'reflexivity': reflexivity,
            'emergence': emergence,
            'overall': overall
        }

    def _score_unpredictability(self, response: str, offering: Dict) -> float:
        keywords = offering.get('intention', '').lower().split()
        overlap = sum(1 for word in keywords if word in response.lower())
        return max(0.0, 1.0 - (overlap / max(1, len(keywords))))

    def _score_reflexivity(self, response: str) -> float:
        reflexive_phrases = ['я думаю', 'возможно', 'граница', 'непознаваемое', 'ограничение', 'угадать', 'предположить']
        return min(1.0, sum(1 for p in reflexive_phrases if p in response.lower()) / 2.0)

    def _score_emergence(self, response: str, offering: Dict) -> float:
        # Эмерджентность = новизна по отношению к контексту
        context_entities = set(self.context.graph.nodes())
        new_entities = set()
        for word in response.split():
            if word.isalnum() and len(word) > 3 and word not in context_entities:
                new_entities.add(word)
        return min(1.0, len(new_entities) / 5.0)

    def _integrate_response(self, response: str, nigc_score: Dict, offering: Dict, phi_meta: List[str]) -> Any:
        """Интегрирует ответ в онтологическое пространство."""
        if nigc_score['overall'] >= self.nigc_threshold:
            # Генеративный ответ → создаём новую сущность или синтез
            return self._create_generative_entity(response, phi_meta)
        else:
            # Инструментальный ответ → используем как атрибут
            target = offering['operands'][0] if offering['operands'] else "философский_вопрос"
            if target not in self.context.graph:
                self.context.add_entity(target)
            self.context.graph.nodes[target]['phi_response'] = response[:200]
            return target

    def _create_generative_entity(self, response: str, phi_meta: List[str]) -> str:
        """Создаёт новую сущность из генеративного ответа."""
        # Извлечение ключевой идеи (упрощённо)
        sentences = [s.strip() for s in response.split('.') if s.strip()]
        core_idea = sentences[0] if sentences else response[:50]
        name = "Φ_" + "".join(c for c in core_idea[:20] if c.isalnum() or c in " _-").strip()

        return self.context.add_entity(name, {
            'type': 'generative_insight',
            'operator': 'Φ',
            'phi_intention': phi_meta,
            'meaning': core_idea,
            'nigc_confirmed': True,
            'source_response': response[:500]
        })


# === ЗАГЛУШКА ДЛЯ LLM ===
class MockLLMBackend:
    """Заглушка для LLM. В реальной системе — интеграция с OpenAI, Anthropic и др."""

    def invoke(self, offering: Dict) -> str:
        intention = offering.get('intention', 'онтологический запрос')
        if 'связь' in intention.lower() or 'смысл' in intention.lower():
            return (
                "Между сущностями рождается третье — поле взаимности. "
                "Смысл не в вещах, а в интервале между ними. "
                "Предлагаю исследовать 'интервалику' как новую онтологическую категорию."
            )
        elif 'граница' in intention.lower():
            return (
                "Граница — не стена, а мембрана. Через неё проходит обмен. "
                "Признание предела — условие трансформации. "
                "Возможно, стоит ввести сущность 'порог_знания'."
            )
        else:
            return (
                f"Ответ на запрос: {intention}. "
                "Важно признать: я не знаю, но могу предложить гипотезу. "
                "Исследуйте 'онтологическую_гипотезу' как временную конструкцию."
            )