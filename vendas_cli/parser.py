import argparse
from datetime import date


def parse_args(argumentos: list[str] | None = None) -> argparse.Namespace:
    """Interpreta os argumentos da linha de comando e valida o intervalo de datas."""

    parser = argparse.ArgumentParser(
        description="Gera um relatório de vendas a partir de um CSV."
    )

    parser.add_argument("arquivo", help="Caminho do arquivo CSV")

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Formato de saída (default: text)",
    )

    parser.add_argument(
        "--start",
        dest="inicio",
        type=date.fromisoformat,
        help="Início do período (YYYY-MM-DD)",
    )

    parser.add_argument(
        "--end",
        dest="fim",
        type=date.fromisoformat,
        help="Fim do perído (YYYY-MM-DD)"
    )

    opcoes = parser.parse_args(argumentos)

    if opcoes.inicio and opcoes.fim and opcoes.inicio > opcoes.fim:
        parser.error("A data inicial não pode ser posterior a data final")
    
    return opcoes