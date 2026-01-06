# -*- coding: utf-8 -*-
"""
ОНТОЛОГИЧЕСКИЙ ЛЕКСЕР LOGOS-κ

Преобразует исходный текст в поток токенов.
Особенность: комментарии `;;` не игнорируются, а становятся
философскими намерениями (phi_meta) — частью онтологического контекста.
"""
import re
from typing import List, Tuple, Any
from core.axiom import OntologicalAxioms

Token = Tuple[str, Any]  # (type, value)


class OntologicalLexer:
    """
    Лексер для LOGOS-κ:
    - Поддерживает Unicode-операторы: Α, Λ, Σ, Ω, ∇, Φ
    - Извлекает phi_meta из ;;-комментариев
    - Валидирует запрещённые формулировки
    """

    def __init__(self, text: str):
        self.original = text
        self.text = text
        self.i = 0
        self.n = len(text)
        self._phi_meta: List[str] = []
        # Обработка комментариев и валидация
        self._strip_comments_and_validate()

    def _strip_comments_and_validate(self):
        """Извлекает phi_meta и валидирует текст на абсолютизм."""
        lines = self.original.splitlines()
        clean_lines = []
        combined_meta = []

        for line in lines:
            if ';;' in line:
                pos = line.index(';;')
                meta = line[pos + 2:].strip()
                if meta:
                    combined_meta.append(meta)
                line = line[:pos]
            clean_lines.append(line)

        # Объединяем мета в один список
        self._phi_meta = combined_meta

        # Валидация всего исходного текста на абсолютизм
        OntologicalAxioms.validate_no_absolutism(self.original)

    def tokenize(self) -> List[Token]:
        """Главная функция: разбор текста на токены."""
        tokens: List[Token] = []
        while self.i < self.n:
            c = self.text[self.i]
            if c.isspace():
                self.i += 1
            elif c == '(':
                self.i += 1
                tokens.append(('LPAREN', c))
            elif c == ')':
                self.i += 1
                tokens.append(('RPAREN', c))
            elif c == '"':
                tokens.append(self._read_string())
            elif c == ':':
                tokens.append(self._read_keyword())
            elif c.isdigit() or (c == '-' and self._peek_next().isdigit()):
                tokens.append(self._read_number())
            elif self._is_symbol_start(c):
                tokens.append(self._read_symbol())
            else:
                raise ValueError(f"Неизвестный символ: '{c}' в позиции {self.i}")
        return tokens

    def _peek_next(self, offset: int = 1) -> str:
        """Просмотр следующего символа без продвижения."""
        if self.i + offset < self.n:
            return self.text[self.i + offset]
        return '\0'

    def _is_symbol_start(self, c: str) -> bool:
        """Проверяет, может ли символ начинать символ (включая Α–Φ)."""
        # Поддержка латинских, греческих и Unicode-символов операторов
        return c.isalpha() or c in 'ΑΛΣΩ∇ΦΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'

    def _read_string(self) -> Token:
        """Читает строку в двойных кавычках."""
        start = self.i + 1
        self.i += 1  # пропускаем открывающую кавычку
        while self.i < self.n and self.text[self.i] != '"':
            if self.text[self.i] == '\\':  # простая поддержка экранирования
                self.i += 2
            else:
                self.i += 1
        if self.i >= self.n:
            raise ValueError("Незавершённая строка")
        value = self.text[start:self.i]
        self.i += 1  # пропускаем закрывающую кавычку
        return ('STRING', value)

    def _read_keyword(self) -> Token:
        """Читает ключевое слово вида `:ключ`."""
        start = self.i
        self.i += 1  # пропускаем ':'
        while self.i < self.n:
            c = self.text[self.i]
            if c.isspace() or c in '()':
                break
            self.i += 1
        return ('KEYWORD', self.text[start:self.i])  # включая ':'

    def _read_number(self) -> Token:
        """Читает целое или вещественное число (включая отрицательные)."""
        start = self.i
        if self.text[self.i] == '-':
            self.i += 1
        while self.i < self.n and (self.text[self.i].isdigit() or self.text[self.i] == '.'):
            self.i += 1
        num_str = self.text[start:self.i]
        try:
            if '.' in num_str:
                return ('NUMBER', float(num_str))
            else:
                return ('NUMBER', int(num_str))
        except ValueError:
            raise ValueError(f"Некорректное число: '{num_str}'")

    def _read_symbol(self) -> Token:
        """Читает символ (имя, оператор)."""
        start = self.i
        while self.i < self.n:
            c = self.text[self.i]
            if c.isspace() or c in '()':
                break
            self.i += 1
        symbol = self.text[start:self.i]
        return ('SYMBOL', symbol)

    def get_phi_meta(self) -> List[str]:
        """Возвращает извлечённые намерения оператора."""
        return self._phi_meta