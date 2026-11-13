import csv
import logging

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation


logger = logging.getLogger(__name__)


@dataclass
class Venda:
    """Representa uma venda registrada no CSV."""

    produto: str
    quantidade: int
    preco_unitario: Decimal
    data: date | None = None


def ler_vendas(caminho: str) -> list[Venda]:
    """Lê e valida um CSV de vendas e retorna uma lista de objetos Venda."""

    vendas: list[Venda] = []

    try:
        arquivo_aberto = open(caminho, encoding="utf-8", newline="")
    except FileNotFoundError:
        logger.error("Arquivo não foi encontrado: %s", caminho)
        raise

    with arquivo_aberto as arquivo:
        leitor = csv.DictReader(arquivo)

        colunas_obrigatorias = {"produto", "quantidade", "preco_unitario"}
        colunas_faltantes = colunas_obrigatorias - set(leitor.fieldnames or [])

        if colunas_faltantes:
            logger.error(
                "Colunas ausentes: %s",
                ", ".join(sorted(colunas_faltantes)),
            )
            raise ValueError(
                f"Colunas ausentes: {', '.join(sorted(colunas_faltantes))}"
            )
        
        for numero_linha, linha in enumerate(leitor, start=2):
            try:
                data_texto = (linha.get("data") or "").strip()

                venda = Venda(
                    produto=linha["produto"].strip(),
                    quantidade=int(linha["quantidade"]),
                    preco_unitario=Decimal(linha["preco_unitario"]),
                    data=date.fromisoformat(data_texto) if data_texto else None,
                )
            except (KeyError, ValueError, TypeError, InvalidOperation) as erro:
                logger.warning(
                    "Linha %d ignorada: %s",
                    numero_linha,
                    erro,
                )
                continue

            if not venda.produto:
                logger.warning(
                    "Linha %d ignorada: produto vazio.",
                    numero_linha,
                )
                continue

            if venda.quantidade <= 0:
                logger.warning(
                    "Linha %d ignorada: quantidade deve ser maior que zero.",
                    numero_linha,
                )
                continue

            vendas.append(venda)

        logger.info("Leitura concluída: %d venda(s) válida(s).", len(vendas))
    
    return vendas


def filtrar_por_periodo(
    vendas: list[Venda],
    inicio: date | None,
    fim: date | None,
) -> list[Venda]:
    """Filtra vendas dentro do intervalo informado. Vendas sem data sao ignoradas."""

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
    """Calcula o valor total de vndas por produto."""

    totais: dict[str, Decimal] = {}

    for venda in vendas:
        valor = venda.quantidade * venda.preco_unitario
        totais[venda.produto] = totais.get(venda.produto, Decimal("0")) + valor
    
    return totais


def total_geral(vendas: list[Venda]) -> Decimal:
    """Calcula o valor total de todas as vendas."""

    return sum(
        total_por_produto(vendas).values(),
        start=Decimal("0")
    )


def produto_mais_vendido(vendas: list[Venda]) -> str | None:
    """Retorna o produto com maior quantidade vendida (ou None, se não houver vendas)."""

    quantidades: dict[str, int] = {}

    for venda in vendas:
        quantidades[venda.produto] = (
            quantidades.get(venda.produto, 0) + venda.quantidade
        )
    
    if not quantidades:
        return None
    
    return max(quantidades, key=lambda produto: quantidades[produto])