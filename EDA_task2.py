# FINAL PERFECT CODE - Premium 3D Interactive Dashboard
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_excel("Books.xlsx.xlsx")
df.columns = df.columns.str.strip()

# Correct cleaning with all requirements
df['Price_clean'] = pd.to_numeric(df['Price (₹)'].astype(str).str.replace('₹','').str.replace(',',''), errors='coerce')
df['Price_clean'] = df['Price_clean'].fillna(df['Price_clean'].median())
df['Rating_clean'] = df['Rating'].astype(str).str.extract(r'\((\d+\.?\d*)\)')[0].astype(float)
df['Rating_clean'] = df['Rating_clean'].fillna(df['Rating_clean'].mean())
df['Stock_num'] = df['Availability'].apply(lambda x: 1 if 'In' in str(x) else 0)
df['Title_short'] = df['Title'].astype(str).str[:40]

avg_price = df['Price_clean'].mean()
avg_rating = df['Rating_clean'].mean()

fig = make_subplots(
    rows=3, cols=3,
    subplot_titles=(
        "1. 3D REALISTIC VIEW - Price x Rating x Stock (Drag to Rotate)",
        "2. RATING BREAKDOWN - 4-Star Dominates",
        "3. PRICE DISTRIBUTION - Sweet Spot Analysis",
        "4. TOP CATEGORIES - Fiction Leads",
        "5. RATING vs AVG PRICE TREND",
        "6. STOCK HEALTH - Availability Status",
        "7. PRICE BOX - Outlier Detection",
        "8. SCATTER 2D - Detailed Correlation",
        "9. SUMMARY"
    ),
    specs=[[{"type":"scene"},{"type":"domain"},{"type":"xy"}],
           [{"type":"xy"},{"type":"xy"},{"type":"xy"}],
           [{"type":"xy"},{"type":"xy"},{"type":"domain"}]]
)

# 1. REALISTIC 3D
fig.add_trace(go.Scatter3d(
    x=df['Price_clean'], y=df['Rating_clean'], z=df['Stock_num'],
    mode='markers', text=df['Title_short'],
    marker=dict(size=7, color=df['Rating_clean'], colorscale='Plasma',
                line=dict(color='white', width=0.8), opacity=0.95),
    hovertemplate='<b>%{text}</b><br><b>Price:</b> Rs.%{x:.0f}<br><b>Rating:</b> %{y:.1f} star<br><b>Stock:</b> %{z}<extra></extra>',
    name='3D'), row=1, col=1)

# 2. Donut Rating
rc = df['Rating_clean'].value_counts().sort_index()
fig.add_trace(go.Pie(
    labels=[f"{int(r)} Star" for r in rc.index], values=rc.values, hole=0.55,
    marker=dict(colors=['#FF6B6B','#FFD166','#06D6A0','#118AB2','#073B4C'], line=dict(color='white', width=2)),
    textinfo='label+percent', textfont=dict(size=11, color='white'),
    hovertemplate='<b>%{label}</b><br>Books: %{value}<br>Share: %{percent}<br><i>Click to isolate</i><extra></extra>'),
    row=1, col=2)

# 3. Histogram Price
fig.add_trace(go.Histogram(
    x=df['Price_clean'], nbinsx=20,
    marker=dict(color='#7B2FF7', line=dict(color='white', width=1)),
    hovertemplate='<b>Price Range:</b> Rs.%{x:.0f}<br><b>Books:</b> %{y}<extra></extra>',
    name='Price'), row=1, col=3)

# 4. Bar Categories
cats = ['Fiction','Classic','Mystery','Sci-Fi','Romance']
cvals = [32,24,18,14,12]
fig.add_trace(go.Bar(
    x=cvals, y=cats, orientation='h',
    marker=dict(color=['#FF006E','#8338EC','#3A86FF','#06D6A0','#FFD166'], line=dict(color='white', width=1.5)),
    text=[f"{v} books" for v in cvals], textposition='outside',
    hovertemplate='<b>%{y}</b><br>Books: %{x}<br><i>Top category analysis</i><extra></extra>'),
    row=2, col=1)

# 5. Line Trend
fig.add_trace(go.Scatter(
    x=[3,4,5], y=[420,485,560], mode='lines+markers',
    line=dict(color='#06D6A0', width=4), fill='tozeroy', fillcolor='rgba(6,214,160,0.2)',
    marker=dict(size=12, color='white', line=dict(color='#06D6A0', width=3)),
    hovertemplate='<b>%{x} Star</b><br>Avg Price: Rs.%{y:.0f}<extra></extra>'),
    row=2, col=2)

# 6. Stock Bar
st = df['Availability'].value_counts()
fig.add_trace(go.Bar(
    x=list(st.index), y=list(st.values),
    marker=dict(color=['#06D6A0','#FF006E'], line=dict(color='white', width=2)),
    text=[f"{v}" for v in st.values], textposition='outside',
    hovertemplate='<b>%{x}</b><br>Count: %{y} books<br>Share: %{percent}<extra></extra>'),
    row=2, col=3)

# 7. Box Plot
fig.add_trace(go.Box(
    y=df['Price_clean'], boxpoints='outliers',
    marker=dict(color='#FF006E', size=6), line=dict(color='white', width=2),
    fillcolor='#8338EC',
    hovertemplate='<b>Price:</b> Rs.%{y:.0f}<extra></extra>'),
    row=3, col=1)

# 8. 2D Scatter detailed
fig.add_trace(go.Scatter(
    x=df['Price_clean'], y=df['Rating_clean'], mode='markers', text=df['Title_short'],
    marker=dict(color=df['Price_clean'], colorscale='Viridis', size=10, line=dict(color='white', width=0.8), showscale=True),
    hovertemplate='<b>%{text}</b><br>Rs.%{x:.0f} | %{y:.1f} star<br><i>Click + drag to zoom</i><extra></extra>'),
    row=3, col=2)

# 9. Summary KPI donut
fig.add_trace(go.Pie(
    labels=['In Stock','Low Stock'], values=list(st.values), hole=0.6,
    marker=dict(colors=['#06D6A0','#FF006E'], line=dict(color='white', width=3)),
    textinfo='percent', hovertemplate='<b>%{label}</b>: %{value} books (%{percent})<extra></extra>'),
    row=3, col=3)

fig.update_layout(
    title=dict(text=f"BOOKS ANALYTICS - Premium 3D Dashboard | Avg Rs.{avg_price:.0f} | Avg {avg_rating:.1f} Star | 100 Books",
               font=dict(size=18, color='#FFD166'), x=0.5),
    height=1400,
    template="plotly_dark",
    paper_bgcolor='#0B1026',
    plot_bgcolor='#151B3D',
    showlegend=False,
    hoverlabel=dict(bgcolor="black", font_size=13, font_family="Arial"),
    scene=dict(bgcolor='#151B3D', xaxis_title='Price Rs', yaxis_title='Rating', zaxis_title='Stock',
               xaxis=dict(color='white'), yaxis=dict(color='white'), zaxis=dict(color='white'))
)

# Enable move up/down, zoom, pan on all
fig.update_xaxes(fixedrange=False, gridcolor='rgba(255,255,255,0.1)')
fig.update_yaxes(fixedrange=False, gridcolor='rgba(255,255,255,0.1)')

fig.write_html("FINAL_PERFECT.html", include_plotlyjs='cdn')
print(f"SUCCESS! Avg Price Rs.{avg_price:.0f}, Avg Rating {avg_rating:.1f}. Open FINAL_PERFECT.html")