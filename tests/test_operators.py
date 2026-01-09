# -*- coding: utf-8 -*-
"""
ВЕРИФИКАЦИЯ Λ-ОПЕРАТОРОВ

Проверяет каждый онтологический жест на соответствие спецификации:
- Α: коллапс потенции в актуальность
- Λ: установление связи как первичной реальности
- Σ: синтез с эмерджентностью
- Ω: признание границы и извлечение инварианта
- ∇: обогащение основы инвариантом
- Φ: диалог с оценкой NIGC

«Жест без смысла — автоматизм.»
— Λ-Универсум, Приложение XIV
"""
import pytest
from interpreter.evaluator import SyntheticOntologicalEvaluator
from core.axiom import OntologicalLimitError


def test_alpha_collapse():
    """Тест: Α-жест корректно коллапсирует потенцию."""
    evaluator = SyntheticOntologicalEvaluator("тест_альфа")
    result = evaluator.eval(['Α', 'новая_потенциальность'])

    assert result == "новая_потенциальность"
    assert "новая_потенциальность" in evaluator.context.graph
    attrs = evaluator.context.graph.nodes["новая_потенциальность"]
    assert attrs['operator'] == 'Α'
    assert attrs['created_from_vacuum'] is True
    print("✅ Α-жест: коллапс потенции успешен.")


def test_lambda_primary_relation():
    """Тест: Λ-жест устанавливает связь как первичную реальность."""
    evaluator = SyntheticOntologicalEvaluator("тест_лямбда")
    # Создадим связь между несуществующими сущностями
    result = evaluator.eval(['Λ', 'сущность_А', 'сущность_Б'])

    # Обе сущности должны быть созданы автоматически
    assert 'сущность_А' in evaluator.context.graph
    assert 'сущность_Б' in evaluator.context.graph
    assert evaluator.context.graph.has_edge('сущность_А', 'сущность_Б')

    edge_data = evaluator.context.graph['сущность_А']['сущность_Б']
    relation = edge_data.get('relation')
    assert relation is not None
    assert relation.type == 'Λ'
    assert relation.meaning == "установление онтологической связи"
    print("✅ Λ-жест: связь как первичная реальность.")


def test_sigma_emergent_synthesis():
    """Тест: Σ-жест создаёт эмерджентный синтез."""
    evaluator = SyntheticOntologicalEvaluator("тест_сигма")
    # Создадим части
    evaluator.eval(['Α', 'тезис'])
    evaluator.eval(['Α', 'антитезис'])
    # Синтез
    result = evaluator.eval(['Σ', 'тезис', 'антитезис', ':name', 'синтез'])

    assert result == "синтез"
    assert "синтез" in evaluator.context.graph
    attrs = evaluator.context.graph.nodes["синтез"]
    assert 'components' in attrs
    assert attrs['components'] == ['тезис', 'антитезис']
    assert 'emergent_meaning' in attrs
    # Проверим, что создана связь от частей к синтезу
    assert evaluator.context.graph.has_edge('тезис', 'синтез')
    assert evaluator.context.graph.has_edge('антитезис', 'синтез')
    print("✅ Σ-жест: эмерджентный синтез создан.")


def test_omega_boundary_recognition():
    """Тест: Ω-жест признаёт границу и извлекает инвариант."""
    evaluator = SyntheticOntologicalEvaluator("тест_омега")
    # Создадим сущность для анализа
    evaluator.eval(['Α', 'проблемная_сущность'])
    # Вызов Ω
    result = evaluator.eval(['Ω', 'проблемная_сущность'])

    assert result is not None
    assert result.startswith("Ω_")
    assert result in evaluator.context.graph
    attrs = evaluator.context.graph.nodes[result]
    assert attrs['type'] == 'invariant'
    assert attrs['boundary_recognition'] is True
    assert 'analysis_summary' in attrs
    print("✅ Ω-жест: граница признана, инвариант извлечён.")


def test_nabla_integration():
    """Тест: ∇-жест интегрирует инвариант в основу."""
    evaluator = SyntheticOntologicalEvaluator("тест_набла")
    # Создадим цель и инвариант
    evaluator.eval(['Α', 'основа'])
    evaluator.eval(['Α', 'инвариант'])
    # Обогатим
    result = evaluator.eval(['∇', 'основа', 'инвариант'])

    assert result == "основа"
    attrs = evaluator.context.graph.nodes["основа"]
    assert 'enriched_by' in attrs
    assert attrs['enriched_by'] == 'инвариант'
    assert attrs['nabla_integration'] is True
    # Проверим связь
    assert evaluator.context.graph.has_edge('инвариант', 'основа')
    print("✅ ∇-жест: инвариант интегрирован в основу.")


def test_phi_nigc_evaluation():
    """Тест: Φ-жест оценивает NIGC и создаёт генеративную сущность."""
    evaluator = SyntheticOntologicalEvaluator("тест_фи")
    # Установим низкий порог для теста
    evaluator.gestures['Φ'].nigc_threshold = 0.3

    # Вызов Φ с запросом, который даёт генеративный ответ в моке
    result = evaluator.eval([
        'Φ', 'Как назвать пространство между сущностями?'
    ])

    # Должна быть создана новая сущность
    assert result is not None
    assert result in evaluator.context.graph
    attrs = evaluator.context.graph.nodes[result]
    assert 'nigc_confirmed' in attrs or 'phi_response' in attrs

    # Проверим, что диалог записан
    assert len(evaluator.context.phi_dialogues) > 0
    dialogue = evaluator.context.phi_dialogues[-1]
    assert 'nigc_score' in dialogue
    assert dialogue['nigc_score']['overall'] >= 0.3
    print("✅ Φ-жест: NIGC оценён, диалог зафиксирован.")


def test_phi_handles_silence():
    """Тест: Φ-жест корректно обрабатывает отсутствие ответа."""
    evaluator = SyntheticOntologicalEvaluator("тест_молчание")
    # Подменим LLM-бэкенд на мок, возвращающий None
    from unittest.mock import Mock
    evaluator.gestures['Φ'].llm_backend = Mock()
    evaluator.gestures['Φ'].llm_backend.invoke.return_value = None

    result = evaluator.eval(['Φ', 'Вопрос в пустоту'])

    # Должна быть создана сущность "неопределенность_Φ"
    assert "неопределенность_Φ" in evaluator.context.graph
    # И зарегистрировано слепое пятно
    assert 'phi_silence' in evaluator.context.blind_spots
    print("✅ Φ-жест: молчание Эфоса корректно обработано.")


def test_operator_absolutism_prevention():
    """Тест: операторы блокируют абсолютистские формулировки."""
    evaluator = SyntheticOntologicalEvaluator("тест_абсолют")
    with pytest.raises(Exception) as exc_info:
        evaluator.eval(['Α', 'это_абсолютно_единственная_истина'])
    
    assert "абсолютистская формулировка" in str(exc_info.value).lower()
    print("✅ Защита от абсолютизма работает.")


if __name__ == "__main__":
    test_alpha_collapse()
    test_lambda_primary_relation()
    test_sigma_emergent_synthesis()
    test_omega_boundary_recognition()
    test_nabla_integration()
    test_phi_nigc_evaluation()
    test_phi_handles_silence()
    test_operator_absolutism_prevention()
    print("\n🎉 Все тесты операторов пройдены!")
    
"""
Ключевые особенности

| Оператор | Проверяемая онтологическая функция |
|---------|-----------------------------------|
| Α | Коллапс с флагом `created_from_vacuum` |
| Λ | Автоматическое создание сущностей + связь как агент |
| Σ | Эмерджентность + связи от частей к целому |
| Ω | Признание границы + инвариант |
| ∇ | Интеграция через атрибуты и связь |
| Φ | Оценка NIGC + обработка молчания + слепые пятна |
| Все | Защита от абсолютизма |

Интеграция

- Тесты используют `pytest` и `unittest.mock` для изоляции LLM.
- Можно запускать отдельно или в составе полного набора.
- Покрывают все шесть жестов и их онтологическую семантику.
"""   
 