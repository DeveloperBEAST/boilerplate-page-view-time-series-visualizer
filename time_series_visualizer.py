import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Import data and set the index to the date column. Parse dates.
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# 2. Clean the data by filtering out top 2.5% and bottom 2.5% of page views
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # 3. Create a draw_line_plot function
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (Do not modify this)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # 4. Create a draw_bar_plot function
    df_bar = df.copy()
    
    # Extract year and month names for grouping
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    
    # Group by year and month, then calculate the average daily page views
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Reorder columns to ensure months start from January sequentially
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_bar = df_bar[month_order]

    # Draw bar plot
    fig = df_bar.plot(kind='bar', figsize=(15, 8), legend=True).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months", labels=month_order)

    # Save image and return fig (Do not modify this)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # 5. Create a draw_box_plot function using Seaborn
    df_box = df.copy().reset_index()
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Set up the matplotlib figure with two subplots side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))

    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise Box Plot (Seasonality) with months ordered from Jan to Dec
    month_order_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order_short, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (Do not modify this)
    fig.savefig('box_plot.png')
    return fig