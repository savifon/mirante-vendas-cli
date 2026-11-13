from vendas_cli.core import (
    filtrar_por_periodo,
    ler_vendas,
    produto_mais_vendido,
    total_geral,
    total_por_produto,
)
from vendas_cli.output import formatar_texto, formatar_json
from vendas_cli.parser import parse_args

import logging


logger = logging.getLogger(__name__)


def main() -> int:
    argumentos = parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    try:
        vendas = filtrar_por_periodo(
            vendas=ler_vendas(argumentos.arquivo),
            inicio=argumentos.inicio,
            fim=argumentos.fim,
        )
    except (FileNotFoundError, ValueError):
        return 1

    totais = total_por_produto(vendas)
    total = total_geral(vendas)
    mais_vendido = produto_mais_vendido(vendas)

    if argumentos.format == "json":
        relatorio = formatar_json(
            totais=totais,
            total=total,
            mais_vendido=mais_vendido,
        )
    else:
        relatorio = formatar_texto(
            totais=totais,
            total=total,
            mais_vendido=mais_vendido,
        )
    
    print(relatorio)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())