import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. LOAD FILE
try:
    df = pd.read_excel("Books.xlsx", engine='openpyxl')
    print("Books.xlsx Found")
except:
    print("Books.xlsx not found, creating sample 100 books")
    np.random.seed(7)
    df = pd.DataFrame({
        'Title': [f"Book {i}" for i in range(1, 101)],
        'Price': np.random.randint(250, 850, 100),
        'Rating': np.random.choice([1,2,3,4,5], 100),
        'Availability': np.random.choice(['In Stock','Out of Stock'], 100, p=[0.8,0.2])
    })

df.columns = df.columns.str.strip()

# 2. CLEAN COLUMNS - FIXED BRACKETS
price_col = [c for c in df.columns if 'price' in c.lower()][0]
rating_col = [c for c in df.columns if 'rating' in c.lower()][0]

# This line was error before - now fixed
df['Price_clean'] = df[price_col].astype(str).str.replace('₹','').str.replace('£','').str.replace(',','')
df['Price_clean'] = pd.to_numeric(df['Price_clean'], errors='coerce')
df['Price_clean'] = df['Price_clean'].fillna(df['Price_clean'].mean())

df['Rating_clean'] = pd.to_numeric(df[rating_col], errors='coerce')
df['Rating_clean'] = df['Rating_clean'].fillna(3)

avg_price = df['Price_clean'].mean()
avg_rating = df['Rating_clean'].mean()

print(f"Avg Price: Rs.{avg_price:.0f}")
print(f"Avg Rating: {avg_rating:.1f} Star")
print(f"Total Books: {len(df)}")

# 3. CREATE DASHBOARD
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"type":"scene"}, {"type":"domain"}], [{"type":"xy"}, {"type":"xy"}]],
    subplot_titles=(f"3D - Avg Rs.{avg_price:.0f}", f"Avg {avg_rating:.1f} Star Rating", "Price Distribution", "Price vs Rating")
)

# 3D Scatter
fig.add_trace(go.Scatter3d(
    x=df['Price_clean'],
    y=df['Rating_clean'],
    z=np.random.randint(0,2,len(df)),
    mode='markers',
    marker=dict(color=df['Rating_clean'], colorscale='Plasma', size=6)
), row=1, col=1)

# Pie Chart
rc = df['Rating_clean'].value_counts().sort_index()
fig.add_trace(go.Pie(
    labels=[f"{int(x)} Star" for x in rc.index],
    values=rc.values,
    hole=0.5
), row=1, col=2)

# Histogram
fig.add_trace(go.Histogram(x=df['Price_clean'], nbinsx=20), row=2, col=1)

# Scatter
fig.add_trace(go.Scatter(x=df['Price_clean'], y=df['Rating_clean'], mode='markers'), row=2, col=2)

fig.update_layout(
    height=900,
    template="plotly_dark",
    title=f"BOOKS EDA | Avg Rs.{avg_price:.0f} | Avg {avg_rating:.1f} Star | {len(df)} Books"
)

# 4. SAVE - FOR GITHUB PAGES MUST BE index.html
fig.write_html("index.html")
print("SUCCESS - index.html created. Now upload to GitHub")
