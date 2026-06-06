import json

with open('assets/data/hypothesis_data.json') as f:
    d = json.load(f)

# ---- SVG helpers ----
def line_pts(values, W=380, H=88, PX=8, PY=6, mn=None, mx=None):
    mn = mn if mn is not None else min(values)
    mx = mx if mx is not None else max(values)
    rng = mx - mn if mx != mn else 1
    n = len(values)
    return [(PX + i*(W-2*PX)/(n-1), (H-PY) - (v-mn)/rng*(H-2*PY)) for i, v in enumerate(values)]

def pts_str(pts):
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)

def grid_lines(W, H, PX, PY, n=3):
    lines = []
    for i in range(n):
        y = PY + i*(H-2*PY)/(n-1)
        lines.append(f'<line x1="{PX}" y1="{y:.1f}" x2="{W-PX}" y2="{y:.1f}" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>')
    return lines

def x_axis(labels, W, H, PX):
    n = len(labels)
    items = []
    for i, lbl in enumerate(labels):
        x = PX + i*(W-2*PX)/(n-1) if n > 1 else PX
        items.append(f'<text x="{x:.1f}" y="{H+13}" text-anchor="middle" fill="rgba(255,255,255,0.3)" font-size="9" font-family="system-ui">{lbl}</text>')
    return items

def x_axis_bars(labels, W, H, PX, n_bars):
    bar_w = (W - 2*PX) / n_bars
    items = []
    for i, lbl in enumerate(labels):
        x = PX + i*bar_w + bar_w/2
        items.append(f'<text x="{x:.1f}" y="{H+13}" text-anchor="middle" fill="rgba(255,255,255,0.3)" font-size="9" font-family="system-ui">{lbl}</text>')
    return items

def multi_line_svg(series_list, x_labels=None, W=380, H=88, PX=8, PY=6):
    all_vals = [v for s in series_list for v in s[0]]
    mn, mx = min(all_vals), max(all_vals)
    items = grid_lines(W, H, PX, PY)
    for vals, color, fill in series_list:
        pts = line_pts(vals, W, H, PX, PY, mn, mx)
        area = ('M ' + f'{pts[0][0]:.1f},{pts[0][1]:.1f} ' +
                ' '.join(f'L {x:.1f},{y:.1f}' for x,y in pts[1:]) +
                f' L {pts[-1][0]:.1f},{H-PY:.1f} L {pts[0][0]:.1f},{H-PY:.1f} Z')
        items.append(f'<path d="{area}" fill="{fill}"/>')
        items.append(f'<polyline points="{pts_str(pts)}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>')
        for x, y in pts:
            items.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{color}"/>')
    if x_labels:
        items += x_axis(x_labels, W, H, PX)
    total_h = H + (18 if x_labels else 4)
    return f'<svg viewBox="0 0 {W} {total_h}" xmlns="http://www.w3.org/2000/svg" class="w-full">\n' + '\n'.join(items) + '\n</svg>'

def dual_line_svg(s1, c1, s2, c2, x_labels, W=380, H=88, PX=8, PY=6):
    items = grid_lines(W, H, PX, PY)
    for vals, color in [(s1, c1), (s2, c2)]:
        pts = line_pts(vals, W, H, PX, PY)
        area = ('M ' + f'{pts[0][0]:.1f},{pts[0][1]:.1f} ' +
                ' '.join(f'L {x:.1f},{y:.1f}' for x,y in pts[1:]) +
                f' L {pts[-1][0]:.1f},{H-PY:.1f} L {pts[0][0]:.1f},{H-PY:.1f} Z')
        items.append(f'<path d="{area}" fill="{color}1a"/>')
        items.append(f'<polyline points="{pts_str(pts)}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>')
        for x, y in pts:
            items.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{color}"/>')
    items += x_axis(x_labels, W, H, PX)
    return f'<svg viewBox="0 0 {W} {H+18}" xmlns="http://www.w3.org/2000/svg" class="w-full">\n' + '\n'.join(items) + '\n</svg>'

def bar_svg(values, colors, x_labels=None, W=380, H=88, PX=8, PY=6):
    mx = max(values)
    n = len(values)
    bar_w = (W - 2*PX) / n
    gap = bar_w * 0.18
    items = grid_lines(W, H, PX, PY)
    for i, (v, c) in enumerate(zip(values, colors)):
        bh = max((v/mx) * (H-2*PY), 2)
        bx = PX + i*bar_w + gap/2
        by = H - PY - bh
        bw = bar_w - gap
        items.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="{c}"/>')
    if x_labels:
        items += x_axis_bars(x_labels, W, H, PX, n)
    total_h = H + (18 if x_labels else 4)
    return f'<svg viewBox="0 0 {W} {total_h}" xmlns="http://www.w3.org/2000/svg" class="w-full">\n' + '\n'.join(items) + '\n</svg>'

def stacked_bar_svg(cat_data_list, colors, labels, W=380, H=88, PX=8, PY=6):
    n_months = len(labels)
    totals = [sum(cat_data_list[c][i] for c in range(len(cat_data_list))) for i in range(n_months)]
    mx = max(totals)
    bar_w = (W - 2*PX) / n_months
    gap = bar_w * 0.18
    items = grid_lines(W, H, PX, PY)
    for mi in range(n_months):
        bx = PX + mi*bar_w + gap/2
        bw = bar_w - gap
        cum = 0
        for ci, (cat_data, color) in enumerate(zip(cat_data_list, colors)):
            v = cat_data[mi]
            seg_h = max((v/mx) * (H-2*PY), 0)
            seg_y = H - PY - (cum + v)/mx*(H-2*PY)
            items.append(f'<rect x="{bx:.1f}" y="{seg_y:.1f}" width="{bw:.1f}" height="{seg_h:.1f}" rx="2" fill="{color}"/>')
            cum += v
    items += x_axis_bars(labels, W, H, PX, n_months)
    return f'<svg viewBox="0 0 {W} {H+18}" xmlns="http://www.w3.org/2000/svg" class="w-full">\n' + '\n'.join(items) + '\n</svg>'

# ---- Data ----
months = d['months_short']
rev_m = d['rev_m']
txn_m = d['txn_m']
ticket_m = d['ticket_m']
daily_avg = d['daily_avg']
rev_by_store = d['rev_by_store']
hours = d['hours']
rev_h_pct = d['rev_h_pct']
txn_wd = d['txn_wd_avg']
txn_we = d['txn_we_avg']
flavour_h = d['flavour_pct_h']
coffee_t_h = d['coffee_ticket_h']
rev_cat_m = d['rev_cat_m']
rev_per_txn = d['rev_per_txn']
cat_pct_store = d['cat_pct_store']
stores = ["Astoria", "Hell's Kitchen", "Lower Manhattan"]
S_COLORS = {'Astoria': '#38bdf8', "Hell's Kitchen": '#fbbf24', 'Lower Manhattan': '#34d399'}

# ---- Build charts ----
h1_series = [(rev_by_store[s], S_COLORS[s], S_COLORS[s]+'22') for s in stores]
ch1 = multi_line_svg(h1_series, months)

da_cols = ['rgba(52,211,153,0.3)','rgba(52,211,153,0.95)','rgba(52,211,153,0.45)',
           'rgba(52,211,153,0.55)','rgba(52,211,153,0.7)','rgba(52,211,153,0.88)']
ch2 = bar_svg(daily_avg, da_cols, months)

txn_cols = ['rgba(56,189,248,0.5)']*6
ch3_txn = bar_svg(txn_m, txn_cols, months)
ch3_ticket = multi_line_svg([(ticket_m, '#a78bfa', '#a78bfa22')], months, H=36)

h4_series = [(rev_by_store[s], S_COLORS[s], S_COLORS[s]+'22') for s in stores]
ch4 = multi_line_svg(h4_series, months)

hour_labels = [str(h) for h in hours]
ch7 = dual_line_svg(flavour_h, '#f472b6', coffee_t_h, '#fbbf24', hour_labels)

cats8 = ['Coffee','Tea','Bakery','Drinking Chocolate','Coffee beans','Others']
cat_colors8 = ['#f59e0b','#2dd4bf','#fb923c','#c084fc','#fde68a','rgba(255,255,255,0.18)']
cat_data8 = [rev_cat_m[c] for c in cats8]
ch8 = stacked_bar_svg(cat_data8, cat_colors8, months)

h9_cols = []
for i, v in enumerate(rev_h_pct):
    if hours[i] in [8, 9, 10]:
        h9_cols.append('#8b5cf6')
    elif hours[i] in [7, 11]:
        h9_cols.append('rgba(139,92,246,0.55)')
    else:
        h9_cols.append('rgba(139,92,246,0.28)')
ch9 = bar_svg(rev_h_pct, h9_cols, hour_labels, W=440)

ch10 = dual_line_svg(txn_wd, '#38bdf8', txn_we, '#f472b6', hour_labels)

# ---- Verdict badge helper ----
def vbadge(v):
    if v == 'c':
        return ('<span class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-semibold '
                'bg-emerald-500/15 text-emerald-300 border border-emerald-500/25">'
                '<svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 20 20">'
                '<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>'
                'Confirmada</span>')
    if v == 'p':
        return ('<span class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-semibold '
                'bg-amber-500/15 text-amber-300 border border-amber-500/25">'
                '<svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 20 20">'
                '<path d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"/></svg>'
                'Parcialmente Confirmada</span>')
    return ('<span class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-semibold '
            'bg-rose-500/15 text-rose-300 border border-rose-500/25">'
            '<svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 20 20">'
            '<path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>'
            'Refutada</span>')

# ---- Card wrappers ----
GLASS = ('bg-gradient-to-br from-white/[0.07] to-white/0 rounded-3xl shadow-lg backdrop-blur-lg '
         'border border-white/[0.08]')

def card_header(num, title, verdict_code):
    return f'''<div class="flex items-start justify-between mb-4">
        <div>
          <p class="text-[10px] font-medium uppercase tracking-[0.16em] text-neutral-500 mb-1">H{num}</p>
          <h3 class="text-[15px] font-semibold tracking-tight leading-snug">{title}</h3>
        </div>
        {vbadge(verdict_code)}
      </div>'''

def card_footer(text):
    return f'''<div class="mt-3 pt-3 border-t border-white/[0.07]">
        <p class="text-[11px] text-neutral-400 leading-relaxed">{text}</p>
      </div>'''

# ---- Legend helpers ----
def dot(color, label):
    return f'<span class="flex items-center gap-1.5"><span class="h-2 w-2 rounded-full flex-shrink-0" style="background:{color}"></span><span class="text-neutral-400">{label}</span></span>'

def legend_row(*items):
    dots = ''.join(dot(c, l) for c, l in items)
    return f'<div class="flex flex-wrap gap-3 text-[10px] mb-3">{dots}</div>'

# ---- H5: horizontal stacked bars ----
top_cats = ['Coffee', 'Tea', 'Bakery', 'Drinking Chocolate', 'Coffee beans', 'Flavours']
cat_colors_5 = ['#f59e0b', '#2dd4bf', '#fb923c', '#c084fc', '#fde68a', '#f472b6']

def stacked_row(store, pcts, cat_colors):
    segs = ''
    for cat, color, pct in zip(top_cats, cat_colors, [pcts[c] for c in top_cats]):
        segs += f'<div style="width:{pct}%;background:{color}" title="{cat}: {pct}%"></div>'
    return f'''<div class="mb-3 last:mb-0">
        <div class="flex justify-between items-center mb-1">
          <span class="text-[11px] text-neutral-300">{store}</span>
          <span class="text-[10px] text-neutral-500">100%</span>
        </div>
        <div class="flex rounded-full overflow-hidden h-5 gap-0.5">{segs}</div>
      </div>'''

h5_rows = ''.join(stacked_row(s, cat_pct_store[s], cat_colors_5) for s in stores)

# ---- H6: horizontal bars ----
rev_pts_items = list(rev_per_txn.items())
max_rpt = max(v for _,v in rev_pts_items)
cat_display = {
    'Coffee beans': ('#fde68a', 'Coffee Beans'),
    'Branded': ('rgba(255,255,255,0.4)', 'Branded'),
    'Loose Tea': ('#2dd4bf', 'Loose Tea'),
    'Packaged Chocolate': ('#c084fc', 'Pack. Choc.'),
    'Drinking Chocolate': ('#c084fc', 'Drink. Choc.'),
    'Coffee': ('#f59e0b', 'Coffee'),
    'Tea': ('#2dd4bf', 'Tea'),
    'Bakery': ('#fb923c', 'Bakery'),
    'Flavours': ('#f472b6', 'Flavours'),
}

h6_rows = ''
for cat, val in rev_pts_items:
    color, label = cat_display.get(cat, ('rgba(255,255,255,0.3)', cat))
    pct = val/max_rpt*100
    h6_rows += f'''<div class="mb-1.5 last:mb-0">
        <div class="flex justify-between text-[10px] mb-0.5">
          <span class="text-neutral-300">{label}</span>
          <span class="text-neutral-400">R${val:.2f}</span>
        </div>
        <div class="h-2 rounded-full bg-white/5 overflow-hidden">
          <div class="h-full rounded-full" style="width:{pct:.1f}%;background:{color}"></div>
        </div>
      </div>'''

# ---- Store growth pct ----
store_growth = {s: round((rev_by_store[s][-1] - rev_by_store[s][0]) / rev_by_store[s][0] * 100, 1) for s in stores}

# ---- Pre-compute values used inside f-string to avoid backslash issues ----
hk = "Hell's Kitchen"
sg_astoria = store_growth["Astoria"]
sg_hk = store_growth[hk]
sg_lm = store_growth["Lower Manhattan"]
h4_legend = legend_row(
    ('#38bdf8', f'Astoria +{sg_astoria}%'),
    ('#fbbf24', f"Hell's Kitchen +{sg_hk}%"),
    ('#34d399', f'Lower Manhattan +{sg_lm}%')
)
hk_pct = cat_pct_store[hk]
astoria_pct = cat_pct_store["Astoria"]
lm_pct = cat_pct_store["Lower Manhattan"]
sg_astoria_val = rev_by_store["Astoria"]
sg_hk_val = rev_by_store[hk]
sg_lm_val = rev_by_store["Lower Manhattan"]

# ---- Build HTML ----
html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<title>Coffee Shop Analytics · Hipóteses</title>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<script src="assets/resource_3fa48481346f.js"></script>
<script src="assets/lucide_latest_2eebd0ebe8c2.js"></script>
<script src="assets/iconify_654a1ef798a3.js"></script>
<link href="assets/css2_86e10c4bcbd4.css" rel="stylesheet"/>
<style>.font-geist {{ font-family: 'Geist', system-ui, sans-serif !important; }}</style>
<link href="assets/css2_0b2072b66163.css" rel="stylesheet"/>
<style>.font-jakarta {{ font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important; }}</style>
<style>
[style*="--border-gradient"]::before {{
  content: ""; position: absolute; inset: 0; padding: 1px;
  border-radius: var(--border-radius-before, inherit);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude;
  background: var(--border-gradient); pointer-events: none;
}}
svg {{ overflow: visible; }}
</style>
</head>
<body class="min-h-screen bg-neutral-950 text-white antialiased font-geist">

<!-- Background -->
<div class="fixed top-0 w-full h-screen -z-10 opacity-40" style="mask-image:linear-gradient(to bottom,transparent,black 0%,black 80%,transparent)">
  <div class="absolute inset-0" style="background:radial-gradient(ellipse 80% 50% at 20% 20%, rgba(56,189,248,0.12) 0%, transparent 60%), radial-gradient(ellipse 60% 40% at 80% 60%, rgba(245,158,11,0.08) 0%, transparent 60%), radial-gradient(ellipse 50% 60% at 50% 90%, rgba(139,92,246,0.08) 0%, transparent 60%)"></div>
</div>

<div class="min-h-screen flex flex-col">
<main class="flex-1">
<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 sm:py-10">

  <!-- ===== PAGE HEADER ===== -->
  <div class="mb-10">
    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-8">
      <div>
        <p class="text-[11px] font-medium uppercase tracking-[0.18em] text-neutral-500 mb-2">Análise · Jan–Jun 2023</p>
        <h1 class="text-[28px] sm:text-[32px] font-semibold tracking-tight leading-tight">Coffee Shop Analytics</h1>
        <p class="text-neutral-400 text-sm mt-1">Rede de 3 lojas · 149.116 transações · Gerente de Operações</p>
      </div>
      <div class="inline-flex items-center gap-2 rounded-2xl bg-white/5 border border-white/10 px-4 py-2 text-[12px] text-neutral-400">
        <span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
        Etapa 4 · Teste de Hipóteses
      </div>
    </div>

    <!-- KPI row -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div class="{GLASS} p-4">
        <p class="text-[10px] uppercase tracking-[0.14em] text-neutral-500 mb-1">Faturamento Total</p>
        <p class="text-[22px] font-semibold tracking-tight text-amber-300">R$ 698k</p>
        <p class="text-[11px] text-neutral-500 mt-0.5">Jan–Jun 2023</p>
      </div>
      <div class="{GLASS} p-4">
        <p class="text-[10px] uppercase tracking-[0.14em] text-neutral-500 mb-1">Crescimento</p>
        <p class="text-[22px] font-semibold tracking-tight text-emerald-300">+103.8%</p>
        <p class="text-[11px] text-neutral-500 mt-0.5">Jan → Jun (faturamento)</p>
      </div>
      <div class="{GLASS} p-4">
        <p class="text-[10px] uppercase tracking-[0.14em] text-neutral-500 mb-1">Transações</p>
        <p class="text-[22px] font-semibold tracking-tight text-sky-300">149.116</p>
        <p class="text-[11px] text-neutral-500 mt-0.5">Itens vendidos</p>
      </div>
      <div class="{GLASS} p-4">
        <p class="text-[10px] uppercase tracking-[0.14em] text-neutral-500 mb-1">Ticket Médio</p>
        <p class="text-[22px] font-semibold tracking-tight text-violet-300">R$ 4,69</p>
        <p class="text-[11px] text-neutral-500 mt-0.5">Por item · estável no período</p>
      </div>
    </div>
  </div>

  <!-- ===== HYPOTHESIS GRID ===== -->
  <div class="mb-4 flex items-center gap-3">
    <p class="text-[10px] font-medium uppercase tracking-[0.18em] text-neutral-600">Teste de 10 Hipóteses Analíticas</p>
    <div class="flex-1 h-px bg-white/5"></div>
    <div class="flex gap-2 text-[10px]">
      {vbadge('c')} {vbadge('p')} {vbadge('r')}
    </div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-8 lg:grid-cols-12 gap-4">

    <!-- ===== ROW 1: H1 + H2 ===== -->

    <!-- H1: Crescimento Sazonal (8 cols) -->
    <section class="md:col-span-5 lg:col-span-8 {GLASS} p-5 relative" style="--border-gradient:linear-gradient(180deg,rgba(255,255,255,0.1),rgba(255,255,255,0));--border-radius-before:24px">
      {card_header(1, 'O crescimento é sazonal, não estrutural?', 'p')}
      {legend_row(('#38bdf8','Astoria'), ('#fbbf24',"Hell's Kitchen"), ('#34d399','Lower Manhattan'))}
      {ch1}
      {card_footer('As 3 lojas crescem em paralelo — padrão consistente com sazonalidade. Sem dados do ano anterior não é possível isolar efeito estrutural de efeito sazonal. O pico de Jun (+6,2% MoM) vs Jan sugere que há aceleração real, não apenas calendário.')}
    </section>

    <!-- H2: Queda de Fev (4 cols) -->
    <section class="md:col-span-3 lg:col-span-4 bg-emerald-600 rounded-3xl p-5 shadow-lg shadow-emerald-900/30 border border-white/10 flex flex-col">
      {card_header(2, 'A queda de fev. é puramente calendária?', 'c')}
      <p class="text-[10px] text-emerald-100/70 -mt-2 mb-3">Receita média por dia (R$)</p>
      {ch2}
      {card_footer('<span class="text-emerald-200">Fev/dia: R$2.719 &gt; Jan/dia: R$2.635 (+3,2%).</span> A queda no total mensal (–6,8%) ocorreu apenas porque fevereiro tem 28 dias vs 31 de janeiro. Demanda não caiu.')}
    </section>

    <!-- ===== ROW 2: H3 + H4 ===== -->

    <!-- H3: Crescimento Volumétrico (6 cols) -->
    <section class="md:col-span-4 lg:col-span-6 bg-sky-600 rounded-3xl p-5 shadow-lg shadow-sky-900/30 border border-white/10 flex flex-col">
      {card_header(3, 'O crescimento é volumétrico, não de ticket?', 'c')}
      <p class="text-[10px] text-sky-100/70 -mt-2 mb-2">Volume de transações por mês</p>
      {ch3_txn}
      <p class="text-[10px] text-sky-100/70 mt-3 mb-1">Ticket médio por item (R$) — escala: 4,60–4,75</p>
      {ch3_ticket}
      {card_footer('<span class="text-sky-200">Transações: +104% (17k→35k). Ticket médio: +0,1% (R$4,72→4,71).</span> Crescimento 100% volumétrico. A rede cresce porque atende mais clientes, não porque cada visita gera mais receita.')}
    </section>

    <!-- H4: Crescimento Homogêneo (6 cols) -->
    <section class="md:col-span-4 lg:col-span-6 {GLASS} p-5 relative flex flex-col" style="--border-gradient:linear-gradient(180deg,rgba(255,255,255,0.1),rgba(255,255,255,0));--border-radius-before:24px">
      {card_header(4, 'O crescimento é homogêneo entre as lojas?', 'c')}
      {h4_legend}
      {ch4}
      <div class="mt-3 grid grid-cols-3 gap-2">
        <div class="rounded-2xl bg-sky-500/10 border border-sky-500/20 p-2 text-center">
          <p class="text-[18px] font-semibold text-sky-300">+{sg_astoria}%</p>
          <p class="text-[9px] text-neutral-500 mt-0.5">Astoria</p>
        </div>
        <div class="rounded-2xl bg-amber-500/10 border border-amber-500/20 p-2 text-center">
          <p class="text-[18px] font-semibold text-amber-300">+{sg_hk}%</p>
          <p class="text-[9px] text-neutral-500 mt-0.5">Hell's Kitchen</p>
        </div>
        <div class="rounded-2xl bg-emerald-500/10 border border-emerald-500/20 p-2 text-center">
          <p class="text-[18px] font-semibold text-emerald-300">+{sg_lm}%</p>
          <p class="text-[9px] text-neutral-500 mt-0.5">Lower Manhattan</p>
        </div>
      </div>
      {card_footer('As curvas são paralelas com diferença máxima de 3,4 p.p. entre lojas. O crescimento é sistêmico — mesma força motriz atuando nas 3 unidades simultaneamente.')}
    </section>

    <!-- ===== ROW 3: H5 + H6 ===== -->

    <!-- H5: Perfil por Loja (7 cols) -->
    <section class="md:col-span-5 lg:col-span-7 {GLASS} p-5 relative flex flex-col" style="--border-gradient:linear-gradient(135deg,rgba(255,255,255,0.09),rgba(255,255,255,0));--border-radius-before:24px">
      {card_header(5, 'Cada loja tem perfil de mix diferente?', 'p')}
      {legend_row(('#f59e0b','Coffee'), ('#2dd4bf','Tea'), ('#fb923c','Bakery'), ('#c084fc','Drink. Choc.'), ('#fde68a','Coffee Beans'), ('#f472b6','Flavours'))}
      <div class="flex-1">
        {h5_rows}
      </div>
      {card_footer("Coffee é idêntico nas 3 lojas (38,6–38,7%) — categoria sem diferenciação. Hell's Kitchen tem 7,9% em Coffee Beans vs 4,4% em Astoria — público mais voltado a preparo em casa. Diferença relevante mas mix global é homogêneo.")}
    </section>

    <!-- H6: Upsell Potential (5 cols) -->
    <section class="md:col-span-3 lg:col-span-5 bg-amber-500 rounded-3xl p-5 shadow-lg shadow-amber-900/30 border border-white/10 flex flex-col">
      {card_header(6, 'Há espaço para crescer via upsell de ticket alto?', 'c')}
      <p class="text-[10px] text-amber-950/70 -mt-2 mb-3">Receita por transação (R$) por categoria</p>
      <div class="flex-1">
        {h6_rows}
      </div>
      {card_footer('<span class="text-amber-900 font-medium">Coffee Beans: R$22,87/txn vs Coffee: R$4,62/txn (5x).</span> Com apenas 1.753 transações, a categoria tem vasta capacidade de absorver demanda. Upsell para produtos de alto ticket é a principal alavanca inexplorada.')}
    </section>

    <!-- ===== ROW 4: H7 + H8 ===== -->

    <!-- H7: Syrups proxy (6 cols) -->
    <section class="md:col-span-4 lg:col-span-6 {GLASS} p-5 relative flex flex-col" style="--border-gradient:linear-gradient(135deg,rgba(255,255,255,0.09),rgba(255,255,255,0));--border-radius-before:24px">
      {card_header(7, 'Mais vendas de syrup indicam ticket de café maior?', 'p')}
      {legend_row(('#f472b6','% transações Flavours/hora'), ('#fbbf24','Ticket médio café (R$)/hora'))}
      {ch7}
      {card_footer('Correlação de Pearson r=0,74. O padrão existe: horários de abertura (6h) e fechamento (20h) concentram mais customizações e ticket ligeiramente maior. Contudo, o efeito é puxado pelos extremos do dia — a relação não é uniforme ao longo do expediente.')}
    </section>

    <!-- H8: Coffee Motor (6 cols) -->
    <section class="md:col-span-4 lg:col-span-6 {GLASS} p-5 relative flex flex-col" style="--border-gradient:linear-gradient(135deg,rgba(255,255,255,0.09),rgba(255,255,255,0));--border-radius-before:24px">
      {card_header(8, 'Coffee é o principal motor do crescimento?', 'c')}
      {legend_row(('#f59e0b','Coffee'), ('#2dd4bf','Tea'), ('#fb923c','Bakery'), ('#c084fc','Drink. Choc.'), ('#fde68a','Coffee Beans'), ('rgba(255,255,255,0.3)','Outros'))}
      {ch8}
      <div class="mt-3 grid grid-cols-2 gap-2">
        <div class="rounded-xl bg-amber-500/10 border border-amber-500/20 px-3 py-2">
          <p class="text-[18px] font-semibold text-amber-300">39,5%</p>
          <p class="text-[9px] text-neutral-500">do crescimento vem de Coffee</p>
        </div>
        <div class="rounded-xl bg-teal-500/10 border border-teal-500/20 px-3 py-2">
          <p class="text-[18px] font-semibold text-teal-300">27,9%</p>
          <p class="text-[9px] text-neutral-500">do crescimento vem de Tea</p>
        </div>
      </div>
      {card_footer('Coffee respondeu por 39,5% do crescimento incremental (Jan→Jun). Junto com Tea (27,9%), as duas categorias explicam 67,4% de todo o crescimento da rede. Alta dependência de 2 categorias.')}
    </section>

    <!-- ===== ROW 5: H9 + H10 ===== -->

    <!-- H9: Concentração Horária (8 cols) -->
    <section class="md:col-span-5 lg:col-span-8 {GLASS} p-5 relative flex flex-col" style="--border-gradient:linear-gradient(135deg,rgba(255,255,255,0.09),rgba(255,255,255,0));--border-radius-before:24px">
      {card_header(9, 'A receita está concentrada em poucos horários?', 'c')}
      <div class="flex items-center gap-4 -mt-2 mb-3 text-[10px]">
        <span class="flex items-center gap-1.5"><span class="h-2.5 w-2.5 rounded-sm" style="background:#8b5cf6"></span><span class="text-neutral-400">Pico (8h–10h): <span class="text-violet-300 font-semibold">36,7%</span></span></span>
        <span class="flex items-center gap-1.5"><span class="h-2.5 w-2.5 rounded-sm" style="background:rgba(139,92,246,0.55)"></span><span class="text-neutral-400">Ombros (7h, 11h)</span></span>
        <span class="flex items-center gap-1.5"><span class="h-2.5 w-2.5 rounded-sm" style="background:rgba(139,92,246,0.28)"></span><span class="text-neutral-400">Fora do pico</span></span>
      </div>
      {ch9}
      {card_footer('Os horários 8h, 9h e 10h concentram 36,7% de toda a receita diária em apenas 3 horas de um expediente de 15h. O horário 20h representa <0,5% — operação residual. Dimensionamento de equipe deve priorizar fortemente o bloco 7h–11h.')}
    </section>

    <!-- H10: Semana vs FdS (4 cols) -->
    <section class="md:col-span-3 lg:col-span-4 {GLASS} p-5 relative flex flex-col" style="--border-gradient:linear-gradient(135deg,rgba(255,255,255,0.09),rgba(255,255,255,0));--border-radius-before:24px">
      {card_header(10, 'O padrão intradiário muda no fim de semana?', 'r')}
      {legend_row(('#38bdf8','Dias úteis'), ('#f472b6','Fim de semana'))}
      {ch10}
      {card_footer('Pico em ambos os grupos: hora 10 (103 txn/dia útil vs 101 txn/fds). Diferença máxima em qualquer hora: apenas 3 transações (~3%). O comportamento intradiário é praticamente idêntico — não há evidência para escalas diferenciadas por dia da semana.')}
    </section>

  </div><!-- /grid -->

  <!-- ===== SUMÁRIO ===== -->
  <div class="mt-6 {GLASS} p-5 relative" style="--border-gradient:linear-gradient(180deg,rgba(255,255,255,0.08),rgba(255,255,255,0));--border-radius-before:24px">
    <p class="text-[10px] font-medium uppercase tracking-[0.16em] text-neutral-500 mb-4">Sumário dos Vereditos</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
      <div class="rounded-2xl bg-emerald-500/8 border border-emerald-500/20 p-3 text-center">
        <p class="text-[32px] font-semibold text-emerald-300">6</p>
        <p class="text-[10px] text-neutral-500 mt-0.5">Confirmadas</p>
        <p class="text-[9px] text-neutral-600 mt-1">H2 H3 H4 H6 H8 H9</p>
      </div>
      <div class="rounded-2xl bg-amber-500/8 border border-amber-500/20 p-3 text-center">
        <p class="text-[32px] font-semibold text-amber-300">3</p>
        <p class="text-[10px] text-neutral-500 mt-0.5">Parc. Confirmadas</p>
        <p class="text-[9px] text-neutral-600 mt-1">H1 H5 H7</p>
      </div>
      <div class="rounded-2xl bg-rose-500/8 border border-rose-500/20 p-3 text-center">
        <p class="text-[32px] font-semibold text-rose-300">1</p>
        <p class="text-[10px] text-neutral-500 mt-0.5">Refutada</p>
        <p class="text-[9px] text-neutral-600 mt-1">H10</p>
      </div>
      <div class="rounded-2xl bg-white/4 border border-white/8 p-3 text-center lg:col-span-2">
        <p class="text-[11px] font-medium text-neutral-300 mb-1">Principal achado</p>
        <p class="text-[11px] text-neutral-400 leading-relaxed">Crescimento real, volumétrico e homogêneo entre lojas. A alavanca inexplorada é upsell via Coffee Beans (5x mais receita por transação). Pico operacional fortemente concentrado nas 3h matinais (8–10h).</p>
      </div>
    </div>
  </div>

</div>
</main>
</div>

<script>
window.addEventListener("DOMContentLoaded", () => {{ lucide.createIcons(); }});
</script>
</body>
</html>
'''

with open('design-system/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Done. File size: {len(html):,} chars, {html.count(chr(10))} lines")
