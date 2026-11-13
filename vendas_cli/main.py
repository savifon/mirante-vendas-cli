from vendas_cli.core import (
    ler_vendas,
    produto_mais_vendido,
    total_geral,
    total_por_produto,
)
from vendas_cli.output import formatar_texto
from vendas_cli.parser import parse_args


def main() -> int:
    argumentos = parse_args()
    vendas = ler_vendas(argumentos.arquivo)

    relatorio = formatar_texto(
        totais=total_por_produto(vendas),
        total=total_geral(vendas),
        mais_vendido=produto_mais_vendido(vendas),
    )
    
    print(relatorio)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())