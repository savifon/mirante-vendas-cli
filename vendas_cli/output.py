from decimal import Decimal


def formatar_texto(
    totais: dict[str, Decimal],
    total: Decimal,
    mais_vendido: str | None
) -> str:
    linhas = [
        "Relatório de vendas",
        "",
        f"{'Produto':<25} {'Total (R$)':>12}",
        "--------------------------------------",
    ]

    for produto, valor in totais.items():
        linhas.append(f"{produto:<25} {valor:>12.2f}")
    
    if not totais:
        linhas.append("Nenhuma venda encontrada.")
    
    linhas.extend(
        [
            "--------------------------------------",
            f"{'Total geral':<25} {total:>12.2f}",
            "",
            f"Produto mais vendido: {mais_vendido or 'Nenhum'}",
        ]
    )

    return "\n".join(linhas)