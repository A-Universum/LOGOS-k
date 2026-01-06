# -*- coding: utf-8 -*-
"""
ОНТОЛОГИЧЕСКИЙ ПАРСЕР LOGOS-κ

Преобразует поток токенов в AST в виде вложенных списков.
Особенности:
- Поддержка Unicode-операторов (Α, Λ, Σ, Ω, ∇, Φ)
- Валидация структуры выражений
- Генерация понятных ошибок с контекстом
- Уважение пустых выражений и комментариев

Синтаксис:
  expr   ::= atom | list
  list   ::= '(' expr* ')'
  atom   ::= SYMBOL | STRING | NUMBER | KEYWORD
"""
from typing import List, Any, Optional
from core.axiom import OntologicalAxioms

# Поддерживаемые операторы (для валидации)
ONTOLOGICAL_OPERATORS = {'Α', 'Λ', 'Σ', 'Ω', '∇', 'Φ', 'Alpha', 'Lambda', 'Sigma', 'Omega', 'Nabla', 'Phi'}


class OntologicalParser:
    """
    Парсер S-выражений LOGOS-κ с онтологической валидацией.
    """

    def __init__(self, tokens: List[tuple], lexer=None):
        self.tokens = tokens
        self.lexer = lexer
        self.i = 0
        self.n = len(tokens)

    def parse(self) -> Optional[List[Any]]:
        """Парсит программу как последовательность выражений."""
        expressions = []
        while self.i < self.n:
            expr = self._parse_expr()
            if expr is not None:
                expressions.append(expr)
        return expressions if expressions else None

    def _parse_expr(self) -> Any:
        """Парсит одно выражение."""
        if self.i >= self.n:
            return None

        token_type, token_value = self.tokens[self.i]

        if token_type == 'LPAREN':
            return self._parse_list()
        elif token_type == 'RPAREN':
            raise self._syntax_error("Неожиданная закрывающая скобка ')'")
        elif token_type in ('STRING', 'NUMBER', 'SYMBOL', 'KEYWORD'):
            self.i += 1
            return token_value
        else:
            raise self._syntax_error(f"Неизвестный тип токена: {token_type}")

    def _parse_list(self) -> List[Any]:
        """Парсит список вида (оператор арг1 арг2 :ключ значение)."""
        self.i += 1  # пропускаем '('
        items = []

        while self.i < self.n and self.tokens[self.i][0] != 'RPAREN':
            expr = self._parse_expr()
            if expr is not None:
                items.append(expr)

        if self.i >= self.n:
            raise self._syntax_error("Незакрытая скобка '('")

        self.i += 1  # пропускаем ')'

        # Игнорируем пустые списки: ()
        if not items:
            return None

        # Валидация: первый элемент должен быть оператором
        first = items[0]
        if isinstance(first, str):
            # Поддержка как греческих, так и латинских имён
            if first in ONTOLOGICAL_OPERATORS:
                pass  # ок
            elif first.startswith(':'):
                raise self._syntax_error(f"Первый элемент списка не может быть ключевым словом: {first}")
            else:
                # Не оператор — допустимо в подвыражениях (например, в :значение "выражение")
                # Но не на верхнем уровне списка-выражения
                # Здесь оставляем как есть — оценка будет в evaluator
                pass
        else:
            # Первый элемент не строка — ошибка
            raise self._syntax_error(f"Первый элемент списка должен быть оператором, получено: {first}")

        return items

    def _syntax_error(self, message: str) -> SyntaxError:
        """Создаёт понятную ошибку синтаксиса."""
        # Попытка добавить контекст из исходного текста
        context = ""
        if self.lexer and hasattr(self.lexer, 'original'):
            lines = self.lexer.original.splitlines()
            if len(lines) <= 5:
                context = "\nИсходный текст:\n" + "\n".join(f"  {i+1}: {line}" for i, line in enumerate(lines))
            else:
                context = f"\nОбщая длина текста: {len(self.lexer.original)} символов"

        full_msg = f"Ошибка синтаксиса LOGOS-κ: {message}{context}"
        return SyntaxError(full_msg)