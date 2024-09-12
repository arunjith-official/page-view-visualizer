import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from pandas.api.types import CategoricalDtype
import matplotlib.dates as mdates

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("./fcc-forum-pageviews.csv",parse_dates=["date"])
df.set_index('date', inplace=True)
# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    plt.figure(figsize=(15, 6))
    plt.plot(df.index, df['value'], color='red', linewidth=1)
    
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel('Page Views')
    
    # Select specific dates to display on the x-axis
    selected_dates = df.index[[0, len(df) // 3, 2 * len(df) // 3, -1]]
    plt.xticks(selected_dates)  # Set these dates as ticks on the x-axis
    
    # Format dates to make them more readable
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig = plt.gcf()
    fig.savefig('line_plot.png')
    
    return fig

df["year"]=df.index.year
df["months"] = df.index.strftime('%B')
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
months_type = CategoricalDtype(categories=month_order, ordered= True)
#grouping to select the mean of the month views and all
df['months'] =  df['months'].astype(months_type)
df_grouped = df.groupby( ["year","months"])['value'].mean().reset_index()

month_palette = sns.color_palette("hsv", 12)  

def draw_bar_plot():
    # Copy and modify data for monthly bar plotplt.figure(figsize=(14, 14))
    plt.figure(figsize=(14, 7))
    sns.barplot(
        data=df_grouped,
        x='year',
        y='value',
        hue='months',
        palette=month_palette
    )
    # Setting legend
    plt.legend(title='Months')
    # Set plot labels and title
    plt.title('Monthly Average Values by Year')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    # df_bar = None
    fig = plt.gcf()
    # Draw bar plot





    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    # df_box = df.copy()
    # df_box.reset_index(inplace=True)
    # df_box['year'] = [d.year for d in df_box.date]
    # df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    year_grouped = [group['value'].values for _, group in df.groupby('year')]
    fig, (ax1,ax2) =plt.subplots(1,2,figsize=(20,8))
    #color palettes
    year_palette = sns.color_palette("hsv", len(df['year'].unique()))
    month_palette = sns.color_palette("Set3",12)
    box1 = ax1.boxplot(
        year_grouped, 
        patch_artist=True, 
        tick_labels=df['year'].unique()
    )
    for patch , color in zip(box1['boxes'], year_palette):
        patch.set_facecolor(color)

    #customise the plot 
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year") 
    ax1.set_ylabel("Page Views")
    #grouping by months
    month_grouped = [group['value'].values for _, group in df.groupby('months')]
    month_labels = [month[:3] for month in month_order]
    box2 = ax2.boxplot(
        month_grouped,
        patch_artist= True,
        tick_labels=month_labels
    )
    for patch , color in zip(box2['boxes'], month_palette):
        patch.set_facecolor(color)
    
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    fig = plt.gcf()



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
