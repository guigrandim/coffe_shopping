# ☕ Coffee Shop Analytics

Dashboard analítico para uma rede de cafeterias com 3 unidades, construído para responder 10 hipóteses de negócio e identificar as principais alavancas de crescimento de receita.

---

## 🚨 Problema de Negócio

Uma rede de 3 cafeterias (Astoria, Hell's Kitchen e Lower Manhattan) encerrou o primeiro semestre de 2023 com crescimento expressivo de faturamento. A gestão, no entanto, não sabia **por que** a receita cresceu — se foi aumento de clientes, aumento do ticket médio por visita, melhora de mix de produtos ou concentração em poucas lojas — e tampouco conhecia as **alavancas ainda não exploradas** que poderiam ampliar esse resultado.

Sem clareza sobre a origem do crescimento, ações de expansão, escalonamento de equipe e estratégias de venda poderiam ser tomadas com base em premissas erradas.

**Pergunta central:** Onde estão as maiores oportunidades de receita que a rede ainda não está capturando?

---

## 🗺️ Planejamento da Solução

A solução foi estruturada em 4 etapas:

1. **Entendimento dos dados** — análise exploratória do dataset transacional (149.116 linhas), mapeamento do schema, identificação de quirks de formatação (moeda em BRL com vírgula decimal, datas DD-MM-YYYY) e limpeza dos dados antes da análise.

2. **Formulação de hipóteses** — 10 hipóteses de negócio ordenadas da maior para a menor alavanca potencial, cobrindo crescimento, concentração horária, mix de produtos, comportamento por loja e padrões temporais.

3. **Teste das hipóteses** — cada hipótese foi testada com os dados reais: análise descritiva, correlações, decomposição de receita por dimensão (hora, loja, categoria, mês) e cálculo de impacto financeiro estimado.

4. **Visualização e síntese** — dashboard interativo em HTML estático com 10 cards analíticos (`design-system/index.html`) e resumo executivo com recomendações priorizadas (`design-system/resumo_executivo.html`).

**Ferramentas:** Python (pandas), HTML, TailwindCSS, SVG inline para gráficos, Lucide Icons, Google Fonts (Geist, Plus Jakarta Sans).

---

## 🛠️ Desenvolvimento

### Dataset

| Atributo | Detalhe |
|---|---|
| Arquivo | `assets/data/coffee-shop-dataset.csv` |
| Período | Janeiro a Junho de 2023 |
| Volume | 149.116 transações |
| Lojas | Astoria (id 3), Hell's Kitchen (id 8), Lower Manhattan (id 5) |
| Moeda | Real Brasileiro (R$) — formato `"R$ 45,00"` |
| Granularidade | Item por item (cada linha = 1 produto vendido) |

### Estrutura do Projeto

```
coffee_shop/
├── assets/
│   └── data/
│       └── coffee-shop-dataset.csv
└── design-system/
    ├── index.html              # Dashboard principal (10 hipóteses)
    ├── resumo_executivo.html   # Resumo executivo para gestão
    └── assets/                 # CSS, fontes e bibliotecas JS
```

### Visualizações Desenvolvidas

- Gráfico de barras mensais (crescimento volumétrico)
- Dual-line chart sobrepostos (ticket médio vs. volume)
- Gráfico de barras horizontais (ranking de ticket por categoria)
- Histograma de receita por hora (concentração horária)
- Área chart com correlação syrups/ticket
- Stacked bar de participação de lojas por mês
- Tabela de performance por loja com crescimento
- Gráfico de linha por dia da semana (fins de semana vs. úteis)

---

## 💡 Top 3 Insights

### 1. 📈 O crescimento é 100% volumétrico — o ticket nunca variou

O faturamento cresceu **+103,8%** de janeiro (R$81.678) a junho (R$166.486), mas o ticket médio ficou flat em **R$4,69** durante todos os 6 meses. O crescimento veio inteiramente do aumento no número de transações (+104%: de 17k para 35k por mês).

**Implicação:** A rede dobrou de tamanho sem nenhuma ação de precificação ou upsell. Qualquer melhora no ticket médio representa receita incremental pura — sem precisar atrair um único novo cliente.

---

### 2. ☕ Coffee Beans têm ticket 5× maior que o café e quase ninguém vende

A categoria **Coffee Beans** gera R$22,87 por transação — contra R$4,62 do café comum. Com apenas 1.753 transações no semestre, representa uma fração irrisória do volume total, mas cada venda equivale a 5 cafés.

**Implicação:** Upsell ativo de Coffee Beans e Branded (R$18,22/txn) no momento do pedido é a alavanca de maior retorno imediato: nenhum novo produto, nenhum desconto, sem marketing — apenas script de balcão.

---

### 3. ⏰ 36,7% da receita diária está comprimida em 3 horas

Os horários das **8h às 10h** concentram mais de 1/3 de toda a receita de um dia de 15h de operação. O pico absoluto é às 10h, consistente nas 3 lojas e em todos os meses — inclusive sábados e domingos, com intensidade idêntica aos dias úteis.

**Implicação:** Qualquer gargalo operacional nessa janela (falta de equipe, equipamento, produto) custa ~12% da receita do dia por hora perdida. Escala de fim de semana precisa ser idêntica à de dias úteis.

---

## 📊 Resultados

| KPI | Valor |
|---|---|
| Faturamento total (Jan–Jun 2023) | R$ 698.000 |
| Crescimento do período | +103,8% (Jan → Jun) |
| Total de transações | 149.116 itens |
| Ticket médio por item | R$ 4,69 (estável) |
| Receita diária média — Janeiro | R$ 2.635/dia |
| Receita diária média — Junho | R$ 5.550/dia |
| Crescimento homogêneo entre lojas | +101% a +105% (sem outlier) |
| Participação do café na receita | 39,5% do total |
| Concentração no pico 8h–10h | 36,7% da receita diária |
| Correlação syrups × ticket | r = 0,74 |

---

## ✅ Conclusões

O crescimento da rede é real, sustentado e estruturalmente saudável — todas as 3 lojas crescem na mesma proporção, o que indica um modelo operacional que funciona e pode ser replicado.

A principal descoberta, porém, é que **a rede cresceu sem explorar nenhuma alavanca de ticket**. Isso é uma limitação do crescimento atual, mas também significa que o upside disponível é imediato e de baixo custo:

**Ações prioritárias recomendadas:**

1. 🗣️ **Protocolo de upsell no balcão** — cada +R$0,50 por transação equivale a +R$75k/ano na rede. Treinar o atendente para oferecer Coffee Beans e Branded na finalização do pedido é o mecanismo de maior retorno.

2. 🍬 **Oferta ativa de syrups e flavours** — a correlação r=0,74 entre personalização de sabores e ticket mais alto indica que horas com mais upsell de flavours têm ticket consistentemente maior. Uma pergunta padrão ("Deseja adicionar um sabor?") captura essa receita imediatamente.

3. 👥 **Dimensionamento de equipe das 8h às 10h** — incluindo sábados e domingos com a mesma intensidade dos dias úteis. O custo de subescalar essa janela é desproporcional.

4. 📋 **Formalizar o playbook operacional** — a homogeneidade entre lojas (+101% a +105%) indica que as práticas atuais funcionam. Documentar e formalizar cria a base para treinamento e expansão futura.

**Limitações da análise:** Os dados cobrem apenas 6 meses sem comparativo histórico. Não há identificador de cliente (impossível calcular LTV ou cohort de retenção) nem dados de custo (análise de margem requer informações adicionais).

---

*📁 Dados: coffee-shop-dataset.csv · 📅 Período: Jan–Jun 2023 · 🏪 3 lojas · 🔢 149.116 transações*
