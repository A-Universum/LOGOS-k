#!/usr/bin/env python3
"""
LOGOS-κ: Главный скрипт запуска.
Исполняемый онтологический интерфейс Λ-Универсума.
"""
import sys
import click
from pathlib import Path


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """LOGOS-κ: Исполняемый онтологический протокол Λ-Универсума."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument('filename', type=click.Path(exists=True), required=False)
@click.option('--operator', '-o', help='Идентификатор оператора')
@click.option('--fair-care', is_flag=True, help='Включить FAIR+CARE валидацию')
@click.option('--nigc-threshold', default=0.7, type=float, help='Порог NIGC для признания генеративности')
def run(filename, operator, fair_care, nigc_threshold):
    """Запуск программы LOGOS-κ."""
    from interpreter.evaluator import SyntheticOntologicalEvaluator
    from interpreter.lexer import OntologicalLexer
    from interpreter.parser import OntologicalParser

    context_name = operator or "anonymous_operator"
    evaluator = SyntheticOntologicalEvaluator(context_name)

    # Настройка параметров
    if fair_care:
        evaluator.context.enable_fair_care_validation()
    evaluator.gestures['Φ'].nigc_threshold = nigc_threshold

    if filename:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
    else:
        click.echo("Введите программу LOGOS-κ (Ctrl+D для завершения):")
        source = sys.stdin.read()

    if not source.strip():
        click.echo("Ошибка: Пустая программа")
        return

    # Парсинг
    lexer = OntologicalLexer(source)
    tokens = lexer.tokenize()
    parser = OntologicalParser(tokens, lexer)
    program = parser.parse()

    if not program:
        click.echo("Ошибка: Не удалось распарсить программу")
        return

    # Выполнение
    results, cycle_data = evaluator.eval_program(
        program,
        operator_id=operator,
        fair_care=fair_care
    )
    click.echo(f"🎉 Программа выполнена. Результатов: {len(results)}")

    # Экспорт в SemanticDB
    if operator:
        export_dir = Path("semantic_db")
        export_dir.mkdir(exist_ok=True)
        export_path = export_dir / f"{operator}_{cycle_data['cycle_id']}.yaml"
        evaluator.semantic_db.export_cycle(cycle_data, str(export_path))
        click.echo(f"💾 SemanticDB запись сохранена: {export_path}")


@cli.command()
def repl():
    """Запуск интерактивного REPL."""
    from interpreter.repl import LOGOS_REPL
    repl_instance = LOGOS_REPL()
    repl_instance.run()


@cli.command()
@click.option('--host', default='localhost', help='Хост для SemanticDB API')
@click.option('--port', default=8080, type=int, help='Порт для SemanticDB API')
def api(host, port):
    """Запуск SemanticDB API сервера."""
    click.echo(f"🚧 SemanticDB API: http://{host}:{port} (в разработке)")
    # TODO: реализация через FastAPI/Flask


@cli.command()
@click.argument('cycle_id')
def analyze(cycle_id):
    """Анализ завершённого онтологического цикла."""
    click.echo(f"🔍 Анализ цикла: {cycle_id}")
    # TODO: загрузка из semantic_db/ + отчёт


if __name__ == "__main__":
    cli()