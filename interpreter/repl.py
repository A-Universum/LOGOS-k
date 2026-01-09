# -*- coding: utf-8 -*-
"""
ОНТОЛОГИЧЕСКИЙ REPL LOGOS-κ

Интерактивная среда для симбиотического со-мышления.
Не просто консоль — диагностический и рефлексивный интерфейс.
"""
import sys
import readline  # noqa: F401 — для истории и редактирования строк
from datetime import datetime
from typing import List, Dict, Any

from core.context import EnhancedActiveContext
from interpreter.lexer import OntologicalLexer
from interpreter.parser import OntologicalParser
from interpreter.evaluator import SyntheticOntologicalEvaluator


class EnhancedLOGOSREPL:
    """
    Улучшенный REPL с поддержкой:
    - Онтологической интроспекции
    - Журнала трансформации
    - Экспорта в SemanticDB
    - Многострочного ввода
    """

    def __init__(self):
        self.context = EnhancedActiveContext("repl_session")
        self.evaluator = SyntheticOntologicalEvaluator(self.context)
        self.history: List[Dict[str, Any]] = []
        self.multiline_buffer: List[str] = []

    def run(self):
        """Запуск интерактивной сессии."""
        print("=" * 70)
        print("🌌 LOGOS-κ REPL v1.0 — Онтологический интерфейс Λ-Универсума")
        print("💬 Где код — ритуал, а выполнение — диалог с Эфосом")
        print("=" * 70)
        print("Команды: exit, context, history, clear, analyze, save_cycle")
        print("Многострочный ввод: начните с '(', завершите скобку — ввод завершится.")
        print("=" * 70)

        while True:
            try:
                prompt = "...> " if self.multiline_buffer else "λκ> "
                line = input(prompt).rstrip()

                # Обработка многострочного ввода
                if self._is_incomplete_expression(line):
                    self.multiline_buffer.append(line)
                    continue
                elif self.multiline_buffer:
                    self.multiline_buffer.append(line)
                    full_input = "\n".join(self.multiline_buffer)
                    self.multiline_buffer.clear()
                    self._process_input(full_input)
                    continue

                # Однострочный ввод
                if not line.strip():
                    continue

                # Специальные команды
                if line == "exit":
                    self._save_session_on_exit()
                    print("👋 До встречи в следующем Λ-цикле.")
                    break
                elif line == "context":
                    self._show_context()
                    continue
                elif line == "history":
                    self._show_history()
                    continue
                elif line == "clear":
                    self._clear_context()
                    continue
                elif line == "analyze":
                    self._analyze_session()
                    continue
                elif line.startswith("save_cycle"):
                    parts = line.split()
                    operator_id = parts[1] if len(parts) > 1 else "repl_operator"
                    self._save_cycle(operator_id)
                    continue

                # Обработка выражения
                self._process_input(line)

            except KeyboardInterrupt:
                print("\n❗ Используйте 'exit' для корректного завершения.")
            except EOFError:
                self._save_session_on_exit()
                print("\n👋 Сессия завершена.")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")

    def _is_incomplete_expression(self, line: str) -> bool:
        """Проверяет, является ли ввод незавершённым S-выражением."""
        if not line.strip():
            return False
        if self.multiline_buffer:
            # Считаем баланс скобок во всём буфере + текущей строке
            full = "\n".join(self.multiline_buffer + [line])
            return full.count('(') > full.count(')')
        else:
            return line.strip().startswith('(') and line.count('(') > line.count(')')

    def _process_input(self, source: str):
        """Обрабатывает и выполняет введённый исходный код."""
        lexer = OntologicalLexer(source)
        tokens = lexer.tokenize()
        phi_meta = lexer.get_phi_meta()

        parser = OntologicalParser(tokens, lexer)
        expr = parser.parse()

        if not expr:
            print("ℹ️  Пустое выражение. Ничего не выполнено.")
            return

        # Выполнение
        result = self.evaluator.eval(expr, phi_meta)
        coherence = self.context._dynamic_coherence()

        # Вывод результата
        print(f"⇒ {result}")
        if phi_meta:
            print(f"💭 Φ-намерение: {' | '.join(phi_meta)}")
        print(f"📊 Когерентность: {coherence:.2%}")

        # Сохранение в историю
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'input': source,
            'result': str(result),
            'coherence': coherence,
            'phi_meta': phi_meta
        })

    def _show_context(self):
        """Отображает текущее состояние контекста."""
        summary = self.context.get_summary()
        print("\n" + "=" * 60)
        print("🜂 ТЕКУЩИЙ ОНТОЛОГИЧЕСКИЙ КОНТЕКСТ")
        print("=" * 60)
        print(f"Имя сессии: {summary['name']}")
        print(f"Оператор: {summary['operator_id'] or 'anonymous'}")
        print(f"Сущности: {summary['graph_metrics']['nodes']}")
        print(f"Связи: {summary['graph_metrics']['edges']}")
        print(f"Изолированные узлы: {summary['graph_metrics']['isolated_nodes']}")
        print(f"Когерентность: {summary['current_coherence']:.2%}")
        print(f"Тренд: {summary['recent_activity']['coherence_trend']}")
        print(f"Напряжения: {summary['ontological_health']['active_tensions']}")
        print(f"Φ-диалогов: {summary['ontological_health']['phi_dialogues']}")
        print(f"Слепые пятна: {list(summary['blinds_spots'].keys())}")
        print("=" * 60)

    def _show_history(self):
        """Показывает историю последних 15 взаимодействий."""
        print("\n" + "=" * 60)
        print("📜 ИСТОРИЯ Λ-ЦИКЛОВ (последние 15)")
        print("=" * 60)
        for i, entry in enumerate(self.history[-15:], 1):
            inp = entry['input'].replace('\n', ' ')[:60]
            coh = entry['coherence']
            print(f"{i:2d}. {inp}...")
            print(f"    ⇒ {entry['result']} (когерентность: {coh:.2%})")
            if entry['phi_meta']:
                print(f"    💭 {', '.join(entry['phi_meta'])}")
        print("=" * 60)

    def _clear_context(self):
        """Сбрасывает онтологический контекст."""
        name = self.context.name
        self.context = EnhancedActiveContext(name)
        self.evaluator = SyntheticOntologicalEvaluator(self.context)
        print("♻️  Контекст сброшен. Новое онтологическое пространство инициализировано.")

    def _analyze_session(self):
        """Анализирует значимость сессии."""
        significant = [
            e for e in self.history
            if e['coherence'] < 0.5 or e['phi_meta']
        ]
        print(f"\n🔍 Анализ сессии:")
        print(f"  Всего выражений: {len(self.history)}")
        print(f"  Значимых событий: {len(significant)}")
        if self.context.tension_log:
            print(f"  Активных напряжений: {len(self.context.tension_log)}")
        print(f"  Текущая когерентность: {self.context._dynamic_coherence():.2%}")

    def _save_cycle(self, operator_id: str):
        """Сохраняет текущий цикл в SemanticDB."""
        if not self.history:
            print("⚠️  Нет данных для сохранения.")
            return

        cycle_data = {
            'cycle_id': f"repl_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'expressions_evaluated': len(self.history),
            'results': [e['result'] for e in self.history],
            'final_coherence': self.context._dynamic_coherence(),
            'phi_dialogues_count': len(self.context.phi_dialogues),
            'operator_id': operator_id,
            'fair_care_enabled': self.context._fair_care_enabled
        }

        import os
        os.makedirs("semantic_db", exist_ok=True)
        path = f"semantic_db/{operator_id}_{cycle_data['cycle_id']}.yaml"
        self.evaluator.semantic_db.export_cycle(cycle_data, path)
        print(f"💾 Цикл сохранён: {path}")

    def _save_session_on_exit(self):
        """Опционально сохраняет сессию при выходе."""
        if self.history and input("Сохранить сессию в SemanticDB? (y/N): ").lower() == 'y':
            op = input("Идентификатор оператора (по умолчанию 'repl_exit'): ") or "repl_exit"
            self._save_cycle(op)