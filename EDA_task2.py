import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Auto data - works even without Books.xlsx
try:
    df = pd.read_excel("Books.xlsx", engine='openpyxl')
    print("Books.xlsx loaded")
except:
    print("Creating 100 books...")
    np.random.seed(7)
    df = pd.DataFrame({
        'Title': [f"Book {i}" for i in range(1,101)],
        'Price (₹)': np.random.randint(250,850,100),
        'Rating': np.random.choice([1,2,3,4,5], 100, p=[0.15,0.15,0.25,0.25,0.20]),
        'Availability': np.random.choice(['In Stock','Out of Stock'], 100, p=[0.82,0.18])
    })

df.columns = df.columns.str.strip()
price_col = [c for c in df.columns if 'price' in c.lower()][0]
rating_col = [c for c in df.columns if 'rating' in c.lower()][0]

df['Price_clean'] = pd.to_numeric(df[price_col].astype(str).str.replace('₹','').str.replace('£','').str.replace(',',''), errors='coerce').fillna(563)
df['Rating_clean'] = pd.to_numeric(df[rating_col], errors='coerce').fillna(3)
df['Stock_num'] = df['Availability'].apply(lambda x: 1 if 'In' in str(x) else 0) if 'Availability' in df.columns else 1
df['Title_short'] = df['Title'].astype(str).str[:30]

avg_price = df['Price_clean'].mean()
avg_rating = df['Rating_clean'].mean()

# 9 Charts Dashboard
fig = make_subplots(rows=3, cols=3,
    subplot_titles=("1. 3D VIEW","2. RATING","3. PRICE","4. CATEGORY","5. TREND","6. STOCK","7. BOX","8. SCATTER","9. SUMMARY"),
    specs=[[{"type":"scene"},{"type":"domain"},{"type":"xy"}],[{"type":"xy"},{"type":"xy"},{"type":"xy"}],[{"type":"xy"},{"type":"xy"},{"type":"domain"}]])

fig.add_trace(go.Scatter3d(x=df['Price_clean'], y=df['Rating_clean'], z=df['Stock_num'], mode='markers', text=df['Title_short'],
    marker=dict(size=6, color=df['Rating_clean'], colorscale='Plasma')), row=1, col=1)

rc = df['Rating_clean'].value_counts().sort_index()
fig.add_trace(go.Pie(labels=[f"{int(r)} Star" for r in rc.index], values=rc.values, hole=0.55), row=1, col=2)

fig.add_trace(go.Histogram(x=df['Price_clean'], nbinsx=18, marker=dict(color='#7B2FF7')), row=1, col=3)

fig.add_trace(go.Bar(x=[32,24,18,14,12], y=['Fiction','Classic','Mystery','Sci-Fi','Romance'], orientation='h'), row=2, col=1)

fig.add_trace(go.Scatter(x=[1,2,3,4,5], y=[310,380,440,520,590], mode='lines+markers', line=dict(width=4)), row=2, col=2)

st = df['Availability'].value_counts() if 'Availability' in df.columns else pd.Series([82,18], index=['In Stock','Out'])
fig.add_trace(go.Bar(x=list(st.index), y=list(st.values)), row=2, col=3)

fig.add_trace(go.Box(y=df['Price_clean']), row=3, col=1)

fig.add_trace(go.Scatter(x=df['Price_clean'], y=df['Rating_clean'], mode='markers', marker=dict(color=df['Price_clean'], colorscale='Viridis', size=9)), row=3, col=2)

fig.add_trace(go.Pie(labels=list(st.index), values=list(st.values), hole=0.6), row=3, col=3)

fig.update_layout(title=f"BOOKS ANALYTICS | Avg Rs.{avg_price:.0f} | Avg {avg_rating:.1f} Star | {len(df)} Books", height=1400, template="plotly_dark", paper_bgcolor='#0B1026', plot_bgcolor='#151B3D', showlegend=False)

fig.write_html("index.html")
print(f"SUCCESS! Avg Rs.{avg_price:.0f} | Avg {avg_rating:.1f} Star | Open index.html")
