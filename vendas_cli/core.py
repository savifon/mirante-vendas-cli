import csv
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Venda:
    produto: str
    quantidade: int
    preco_unitario: Decimal
    data: date | None = None


def ler_vendas(caminho: str) -> list [Venda]:
    vendas: list[Venda] = []

    with open(caminho, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        colunas_obrigatorias = {"produto", "quantidade", "preco_unitario"}
        colunas_faltantes = colunas_obrigatorias - set(leitor.fieldnames or [])

        if colunas_faltantes:
            raise ValueError(
                f"Colunas ausentes: {', '.join(faltantes)}"
            )
        
        for linha in leitor:
            data_texto = (linha.get("data") or "").strip()

            venda = Venda(
                produto=linha["produto"].strip(),
                quantidade=int(linha["quantidade"]),
                preco_unitario=Decimal(linha["preco_unitario"]),
                data=date.fromisoformat(data_texto) if data_texto else None,
            )

            vendas.append(venda)
    
    return vendas


def filtrar_por_periodo(
    vendas: list[Venda],
    inicio: date | None,
    fim: date | None,
) -> list[Venda]:
    vendas_filtradas = vendas

    if inicio is not None:
        vendas_filtradas = [
            venda
            for venda in vendas_filtradas
            if venda.data is not None and venda.data >= inicio
        ]

    if fim is not None:
        vendas_filtradas = [
            venda
            for venda in vendas_filtradas
            if venda.data is not None and venda.data <= fim
        ]

    return vendas_filtradas


def total_por_produto(vendas: list[Venda]) -> dict[str, Decimal]:
    totais: dict[str, Decimal] = {}

    for venda in vendas:
        valor = venda.quantidade * venda.preco_unitario
        totais[venda.produto] = totais.get(venda.produto, Decimal("0")) + valor
    
    return totais


def total_geral(vendas: list[Venda]) -> Decimal:
    return sum(
        total_por_produto(vendas).values(),
        start=Decimal("0")
    )


def produto_mais_vendido(vendas: list[Venda]) -> str | None:
    quantidades: dict[str, int] = {}

    for venda in vendas:
        quantidades[venda.produto] = (
            quantidades.get(venda.produto, 0) + venda.quantidade
        )
    
    if not quantidades:
        return None
    
    return max(quantidades, key=lambda produto: quantidades[produto])