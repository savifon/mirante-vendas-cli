import pytest

from vendas_cli.main import main


def test_relatorio_em_texto(tmp_path, capsys) -> None:
    arquivo = tmp_path / "vendas.csv"
    arquivo.write_text(
        "produto,quantidade,preco_unitario,data\n"
        "Camiseta,3,49.90,2026-01-10\n",
        encoding="utf-8",
    )

    codigo = main(
        [
            str(arquivo),
            "--format",
            "text",
        ]
    )

    saida = capsys.readouterr().out

    assert codigo == 0
    assert "Camiseta" in saida
    assert "149.70" in saida


def test_relatorio_em_json(tmp_path, capsys) -> None:
    arquivo = tmp_path / "vendas.csv"
    arquivo.write_text(
        "produto,quantidade,preco_unitario,data\n"
        "Camiseta,3,49.90,2026-01-10\n",
        encoding="utf-8",
    )

    codigo = main(
        [
            str(arquivo),
            "--format",
            "json",
        ]
    )

    saida = capsys.readouterr().out

    assert codigo == 0
    assert '"produto_mais_vendido": "Camiseta"' in saida
    assert '"total_geral": "149.70"' in saida


def test_arquivo_inexistente(capsys) -> None:
    codigo = main(["arquivo-inexistente.csv"])

    assert codigo == 1