from decimal import Decimal

from vendas_cli.output import formatar_json, formatar_texto


def test_formatar_texto() -> None:
    relatorio = formatar_texto(
        totais={
            "Camiseta": Decimal("199.60"),
        },
        total=Decimal("199.60"),
        mais_vendido="Camiseta",
    )

    assert "Relatório de vendas" in relatorio
    assert "Camiseta" in relatorio
    assert "199.60" in relatorio
    assert "Produto mais vendido: Camiseta" in relatorio


def test_formatar_texto_sem_vendas() -> None:
    relatorio = formatar_texto(
        totais={},
        total=Decimal("0"),
        mais_vendido=None,
    )

    assert "Nenhuma venda encontrada." in relatorio
    assert "Produto mais vendido: Nenhum" in relatorio


def test_formatar_json() -> None:
    relatorio = formatar_json(
        totais={
            "Camiseta": Decimal("199.60"),
        },
        total=Decimal("199.60"),
        mais_vendido="Camiseta",
    )

    assert '"total_por_produto"' in relatorio
    assert '"Camiseta": "199.60"' in relatorio
    assert '"total_geral": "199.60"' in relatorio
    assert '"produto_mais_vendido": "Camiseta"' in relatorio