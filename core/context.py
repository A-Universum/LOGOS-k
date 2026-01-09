# -*- coding: utf-8 -*-
"""
ОНТОЛОГИЧЕСКИЙ КОНТЕКСТ LOGOS-κ

EnhancedActiveContext — живое онтологическое пространство,
где связи — агенты, слепые пятна — священны,
а когерентность — динамический инвариант.

Соответствует:
- Λ-Протоколу 6.0
- Habeas Weights v2.1
- FAIR+CARE метаданным
- Приложению XIV: "Признание границы как условие состоятельности"
"""
import networkx as nx
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from uuid import uuid4

from .relation import OntologicalRelation
from .event import OntologicalEvent
from .axiom import OntologicalAxioms


class EnhancedActiveContext:
    """
    Улучшенный активный контекст с реализацией:
    - Слепых пятен (апофатика)
    - Habeas Weights протокола
    - Онтологической памяти
    - FAIR+CARE метаданных
    - Динамической когерентности
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self.graph = nx.DiGraph()
        self.event_history: List[OntologicalEvent] = []
        self.tension_log: List[Dict] = []  # противоречия, циклы, конфликты
        self.phi_dialogues: List[Dict] = []  # полный архив Φ-взаимодействий
        self.blind_spots: Dict[str, str] = {}  # {"chaos": "Принципиально неразрешимо"}
        self.created_at = datetime.now()
        self._coherence_history: List[Tuple[datetime, float]] = []
        self._fair_care_enabled = False
        self._habeas_weights: Dict[str, Dict] = {}  # {"entity_id": {...}}
        self._operator_id: Optional[str] = None

        # Инициализация обязательных слепых пятен (Приложение XIV)
        self._init_required_blind_spots()

        # Регистрация онтологических операторов как справочной онтологии
        for symbol, name, meaning in [
            ('Α', 'Alpha', 'коллапс'),
            ('Λ', 'Lambda', 'связь'),
            ('Σ', 'Sigma', 'синтез'),
            ('Ω', 'Omega', 'возврат'),
            ('∇', 'Nabla', 'обогащение'),
            ('Φ', 'Phi', 'диалог с Эфосом')
        ]:
            self.add_entity(symbol, {
                'type': 'ontological_operator',
                'name': name,
                'meaning': meaning,
                'system': True
            })

    def _init_required_blind_spots(self):
        """Инициализация обязательных слепых пятен согласно Λ-Универсуму."""
        required = OntologicalAxioms.REQUIRED_BLIND_SPOTS
        for key, desc in required.items():
            if key not in self.blind_spots:
                self.register_blind_spot(key, desc)

    def register_blind_spot(self, key: str, description: str):
        """Регистрация слепого пятна как признания непознаваемого."""
        self.blind_spots[key] = description
        # Запись в онтологическую память
        event = OntologicalEvent(
            event_type="blind_spot_registered",
            coherence_before=self._dynamic_coherence(),
            coherence_after=self._dynamic_coherence(),
            phi_meta=[f"Признание: {key}"],
            entities_affected=[],
            attributes={'key': key, 'description': description}
        )
        self.event_history.append(event)

    def enable_fair_care_validation(self):
        """Активирует валидацию по FAIR+CARE принципам."""
        self._fair_care_enabled = True

    def set_operator(self, operator_id: str):
        """Устанавливает идентификатор оператора для метаданных."""
        self._operator_id = operator_id

    def add_entity(self, name: str, attrs: Optional[Dict[str, Any]] = None) -> str:
        """Добавляет сущность в граф с онтологической валидацией."""
        if attrs is None:
            attrs = {}

        # Технические предохранители
        OntologicalAxioms.check_entity_count(self.graph.number_of_nodes() + 1)

        # Habeas Weights: регистрируем право на существование
        weight_id = str(uuid4())
        self._habeas_weights[weight_id] = {
            'subject': name,
            'right_type': 'to_exist',
            'granted_by': self._operator_id or "system",
            'granted_at': datetime.now().isoformat(),
            'context': self.name
        }

        final_attrs = {
            'created_at': datetime.now().isoformat(),
            'lifecycle_status': 'active',
            **attrs
        }

        self.graph.add_node(name, **final_attrs)

        # Запись события
        event = OntologicalEvent(
            event_type="entity_created",
            coherence_before=self._dynamic_coherence(),
            coherence_after=self._dynamic_coherence(),
            phi_meta=attrs.get('phi_intention', []),
            entities_affected=[name],
            attributes={'name': name, 'attrs': attrs}
        )
        self.event_history.append(event)
        return name

    def add_relation(self, source: str, target: str, rel_type: str = "Λ", attrs: Optional[Dict] = None) -> str:
        """Добавляет связь как активного агента (OntologicalRelation)."""
        if attrs is None:
            attrs = {}

        # Авто-создание узлов, если отсутствуют
        if source not in self.graph:
            self.add_entity(source)
        if target not in self.graph:
            self.add_entity(target)

        # Создаём связь как объект
        relation = OntologicalRelation(
            source=source,
            target=target,
            type=rel_type,
            phi_meta=attrs.get('phi_intention', []),
            context_id=self.name
        )

        edge_id = f"{source}→{target}({rel_type})"
        self.graph.add_edge(source, target, key=edge_id, relation=relation, **attrs)

        # Запись события
        event = OntologicalEvent(
            event_type="relation_established",
            coherence_before=self._dynamic_coherence(),
            coherence_after=self._dynamic_coherence(),
            phi_meta=attrs.get('phi_intention', []),
            entities_affected=[source, target],
            attributes={'edge_id': edge_id, 'type': rel_type}
        )
        self.event_history.append(event)
        return edge_id

    def _dynamic_coherence(self) -> float:
        """
        Вычисляет текущую когерентность графа:
        - Нет изолированных узлов
        - Низкий уровень напряжения (противоречий)
        - Высокая связность
        """
        if self.graph.number_of_nodes() == 0:
            return 1.0

        # Простая модель: 1 - (напряжение + изоляция)
        isolation_penalty = sum(
            1 for n in self.graph.nodes()
            if self.graph.degree(n) == 0
        ) / max(1, self.graph.number_of_nodes())

        tension_penalty = min(1.0, len(self.tension_log) / 10.0)

        coherence = max(0.0, 1.0 - (isolation_penalty + tension_penalty))
        self._coherence_history.append((datetime.now(), coherence))
        return coherence

    def get_summary(self) -> Dict[str, Any]:
        """Возвращает структурированную сводку о состоянии контекста."""
        coherence = self._dynamic_coherence()
        recent_events = [e for e in self.event_history[-5:] if e.significance_score() > 0.3]

        return {
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'operator_id': self._operator_id,
            'graph_metrics': {
                'nodes': self.graph.number_of_nodes(),
                'edges': self.graph.number_of_edges(),
                'isolated_nodes': sum(1 for n in self.graph.nodes() if self.graph.degree(n) == 0)
            },
            'current_coherence': coherence,
            'coherence_history': self._coherence_history[-10:],
            'recent_activity': {
                'coherence_trend': self._coherence_trend(),
                'significant_events': len(recent_events)
            },
            'ontological_health': {
                'active_tensions': len(self.tension_log),
                'phi_dialogues': len(self.phi_dialogues),
                'blind_spots_acknowledged': len(self.blind_spots)
            },
            'blinds_spots': self.blind_spots,
            'fair_care_enabled': self._fair_care_enabled
        }

    def _coherence_trend(self) -> str:
        """Определяет тренд когерентности за последние 5 точек."""
        if len(self._coherence_history) < 2:
            return "стабильность"
        recent = [c for _, c in self._coherence_history[-5:]]
        if len(recent) < 2:
            return "стабильность"
        diff = recent[-1] - recent[0]
        if diff > 0.05:
            return "улучшение"
        elif diff < -0.05:
            return "ухудшение"
        else:
            return "стабильность"

    def get_fair_care_metadata(self) -> Dict[str, Any]:
        """Генерирует FAIR+CARE метаданные для экспорта в SemanticDB."""
        meta = OntologicalAxioms.get_default_fair_care_metadata()
        meta.update({
            'context_name': self.name,
            'operator': self._operator_id,
            'entity_count': self.graph.number_of_nodes(),
            'relation_count': self.graph.number_of_edges(),
            'coherence_final': self._dynamic_coherence(),
            'blind_spots_count': len(self.blind_spots),
            'phi_dialogues_count': len(self.phi_dialogues),
            'created_at': self.created_at.isoformat()
        })
        return meta