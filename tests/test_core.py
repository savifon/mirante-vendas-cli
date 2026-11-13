from datetime import date
from decimal import Decimal

from vendas_cli.core import (
    Venda,
    filtrar_por_periodo,
    produto_mais_vendido,
    total_geral,
    total_por_produto,
)


def test_total_geral() -> None:
    vendas = [
        Venda(
            produto="Camiseta",
            quantidade=3,
            preco_unitario=Decimal("49.90"),
        ),
        Venda(
            produto="Calça",
            quantidade=2,
            preco_unitario=Decimal("99.90"),
        ),
    ]

    resultado = total_geral(vendas)

    assert resultado == Decimal("349.50")


def test_produto_mais_vendido() -> None:
    vendas = [
        Venda(
            produto="Camiseta",
            quantidade=3,
            preco_unitario=Decimal("49.90"),
        ),
        Venda(
            produto="Calça",
            quantidade=2,
            preco_unitario=Decimal("99.90"),
        ),
    ]

    resultado = produto_mais_vendido(vendas)

    assert resultado == "Camiseta"


def test_produto_mais_vendido_sem_vendas() -> None:
    resultado = produto_mais_vendido([])

    assert resultado is None


def test_filtrar_por_periodo() -> None:
    vendas = [
        Venda(
            produto="Camiseta",
            quantidade=3,
            preco_unitario=Decimal("49.90"),
            data=date(2026, 1, 10),
        ),
        Venda(
            produto="Tênis",
            quantidade=1,
            preco_unitario=Decimal("199.90"),
            data=date(2026, 2, 10),
        ),
    ]

    resultado = filtrar_por_periodo(
        vendas=vendas,
        inicio=date(2026, 1, 1),
        fim=date(2026, 1, 31),
    )

    assert len(resultado) == 1
    assert resultado[0].produto == "Camiseta"