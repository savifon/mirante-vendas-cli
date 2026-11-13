import pytest

from vendas_cli.parser import parse_args


def test_argumentos_padrao() -> None:
    argumentos = parse_args(["vendas.csv"])

    assert argumentos.arquivo == "vendas.csv"
    assert argumentos.format == "text"
    assert argumentos.inicio is None
    assert argumentos.fim is None


def test_argumentos_com_periodo() -> None:
    argumentos = parse_args(
        [
            "vendas.csv",
            "--format",
            "json",
            "--start",
            "2026-01-01",
            "--end",
            "2026-01-31",
        ]
    )

    assert argumentos.arquivo == "vendas.csv"
    assert argumentos.format == "json"
    assert argumentos.inicio.isoformat() == "2026-01-01"
    assert argumentos.fim.isoformat() == "2026-01-31"


def test_periodo_invalido() -> None:
    with pytest.raises(SystemExit):
        parse_args(
            [
                "vendas.csv",
                "--start",
                "2026-01-31",
                "--end",
                "2026-01-01",
            ]
        )