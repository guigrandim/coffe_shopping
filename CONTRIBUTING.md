# Como este projeto foi construído

Este repositório é um projeto de análise de dados de uma rede de cafeterias. Todo o trabalho — desde a limpeza dos dados até o dashboard e o relatório executivo — foi construído em sessões iterativas com **[Claude Code](https://claude.ai/code)** como co-analista.

---

## O que é Claude Code neste contexto

Claude Code é uma CLI da Anthropic que roda dentro do terminal ou do VS Code. Em vez de usar o chat como uma caixa de respostas, ele atua como um agente que lê arquivos, escreve código, executa comandos e itera — sem precisar copiar e colar manualmente.

Neste projeto ele foi usado para:

- Inspecionar e entender o schema do CSV sem abrir o arquivo manualmente
- Escrever e refinar a função `parse_brl()` para normalizar moeda brasileira (vírgula decimal, prefixo `R$`)
- Explorar hipóteses analíticas em tempo real (ex: *"onde está o r=0.74 mencionado no resumo?"*)
- Gerar o notebook de EDA, o dashboard HTML e o relatório executivo
- Iterar no design do bento-grid sem sair do editor

---

## Estrutura do projeto

```
coffee_shop/
├── assets/
│   └── data/
│       └── coffee-shop-dataset.csv   # 149 116 transações, Jan–Jun 2023
├── docs/
│   ├── index.html                    # Dashboard bento-grid (TailwindCSS)
│   └── resumo_executivo.html         # Relatório de insights para stakeholders
├── notebooks/
│   └── analysis.ipynb                # EDA: limpeza, agregações, correlações
├── generate_dashboard.py             # Script auxiliar de geração
└── index.html                        # Redirect raiz → docs/
```

---

## Dataset

| Campo | Detalhe |
|-------|---------|
| Fonte | Transações reais de 3 lojas (Hell's Kitchen, Lower Manhattan, Astoria) |
| Período | Janeiro a Junho de 2023 |
| Volume | 149 116 linhas |
| Moeda | Real brasileiro — formato `"R$ 45,00"` (vírgula decimal, prefixo textual) |
| Datas | `DD-MM-YYYY` (day-first, não ISO 8601) |
| Dia da semana | Indexado em 0 = segunda-feira |

**Limpeza necessária:**

```python
def parse_brl(series: pd.Series) -> pd.Series:
    return (
        series
        .str.strip()
        .str.replace(r'^R\$\s*', '', regex=True)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )
```

---

## Principais achados analíticos

| Métrica | Valor |
|---------|-------|
| Receita total (6 meses) | R$ 698 812 |
| Ticket médio | R$ 4,69 |
| Hora de pico | 10h |
| Categoria líder | Coffee (39,5% da receita; 38,6% das transações) |
| Crescimento mensal | r = 0.96 (quase-linear Jan→Jun) |
| Correlação syrup × ticket | r = 0.73 (horas com mais personalização têm ticket maior) |

### A correlação r ≈ 0.74 (syrup ratio × coffee ticket)

O achado mais não-óbvio do projeto: nas horas de menor movimento (abertura às 6h, fechamento às 20h), a proporção de pedidos de syrup/flavour chega a 17% e o ticket médio do café é ~R$ 4,80. No pico operacional (10–14h), os clientes pedem café simples e a proporção cai para ~7%, com ticket ~R$ 4,55.

Isso sustenta a recomendação do resumo executivo: **oferecer ativamente syrups durante o rush é o alavancamento de maior ROI** — é exatamente quando a personalização está mais baixa, e um simples *"deseja adicionar um sabor?"* pode mover o ticket sem custo adicional de operação.

---

## Como reproduzir

```bash
# 1. Clone o repositório
git clone <repo-url>
cd coffee_shop

# 2. Instale as dependências do notebook
pip install pandas numpy matplotlib seaborn scipy jupyter

# 3. Execute o notebook
jupyter lab notebooks/analysis.ipynb

# 4. Abra o dashboard
# Basta abrir docs/index.html no browser — sem servidor necessário
```

---

## Stack do dashboard

O `docs/index.html` é completamente estático e self-contained:

- **TailwindCSS** — via bundle local `assets/resource_3fa48481346f.js`
- **Lucide icons** — via `assets/lucide_latest_2eebd0ebe8c2.js`
- **Iconify + Solar icon set** — via `assets/iconify_654a1ef798a3.js`
- **Google Fonts** — carregadas dos CSS bundlados em `docs/assets/`
- Layout: bento-grid 12 colunas (`grid-cols-1 md:grid-cols-8 lg:grid-cols-12`)

---

## Fluxo de trabalho com Claude Code

O processo não foi linear — foi conversacional. Exemplo representativo de uma sessão:

1. **Pergunta exploratória** → *"onde está o r=0.74 mencionado no resumo executivo?"*
2. **Claude lê o CSV** → identifica que o valor não existe como constante em nenhum arquivo
3. **Busca exaustiva** → testa ~50 combinações de pares de variáveis agregadas
4. **Hipótese** → o valor surge em `syrup_ratio_by_hour × coffee_avg_ticket_by_hour`
5. **Validação** → r = 0.7259, p = 0.0027 — estatisticamente significativo
6. **Célula adicionada ao notebook** com scatter plot anotado e interpretação de negócio

Esse ciclo — hipótese → código → resultado → interpretação — aconteceu inteiramente dentro do editor, sem trocar de contexto.

---

## Contribuindo

Este é um projeto de portfólio individual, mas o código e os dados são abertos. Se quiser explorar os dados ou adaptar o dashboard:

1. Faça um fork
2. Trabalhe em uma branch
3. Abra um PR com descrição do que foi alterado e por quê
