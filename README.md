# vendas-cli

CLI em Python para gerar relatórios de vendas a partir de um arquivo CSV.

## Clonar o projeto

```bash
git clone https://github.com/savifon/vendas-cli.git
cd vendas-cli
```

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Uso

```bash
vendas-cli vendas.csv --format text
vendas-cli vendas.csv --format json
vendas-cli vendas.csv --format json --start 2026-01-01 --end 2026-01-31
```

## Formato do CSV

```csv
produto,quantidade,preco_unitario,data
Camiseta,3,49.90,2026-01-10
Calça,2,99.90,2026-01-15
```

- `produto`, `quantidade` e `preco_unitario` são obrigtórios.
- `data` é opcional e deve usar o formato `YYYY-MM-DD`.
- Linhas inváildas são ignoradas e registradas no log.
- Com filtro de data, apenas vendas que possuem data são consideradas.

## Testes

```bash
pytest
```

A configuração exige cobertura mínima de 80%.