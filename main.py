import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
file_name = 'wfpvam_foodprices.csv'

pd.set_option('display.max_columns', None)
df = pd.read_csv(file_name, encoding='latin1')
print(df)

def pricebyyear(df):
   
    price_variation = df.groupby(['Year', 'Country'])['mp_price'].mean().unstack()
    mean_prices_by_country = price_variation.mean()
    top_10_countries = mean_prices_by_country.nlargest(10).index
    filtered_df = df[df['Country'].isin(top_10_countries)]
    price_variation = filtered_df.groupby(['Year', 'Country'])['mp_price'].mean().unstack()

   
    plt.figure(figsize=(12, 6))

    for country in price_variation.columns:
        plt.plot(price_variation.index, price_variation[country], marker='o', linestyle='-', label=country)

    plt.title('Price Variation by Year for Top 10 Countries')
    plt.xlabel('Year')
    plt.ylabel('Average Price')
    plt.xticks(price_variation.index.unique().astype(int))
    plt.grid(True)
    plt.legend(loc='best')

    plt.show()
pricebyyear(df)

def histograms(df):
    wholesale_prices = df[df['Wholesale or Retail'] == 'Wholesale']['mp_price']
    retail_prices = df[df['Wholesale or Retail'] == 'Retail']['mp_price']

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.hist(wholesale_prices, bins=20, color='blue', alpha=0.7)
    plt.title('Wholesale Price Distribution')
    plt.xlabel('Price')
    plt.ylabel('Frequency')

    plt.subplot(1, 2, 2)
    plt.hist(retail_prices, bins=20, color='green', alpha=0.7)
    plt.title('Retail Price Distribution')
    plt.xlabel('Price')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()
histograms(df)


def top5food(df):
    
    food_sum_prices = df.groupby('Food Name')['mp_price'].sum()
    top_5_food_names = food_sum_prices.nlargest(5).index
    top_5_prices = food_sum_prices.nlargest(5)

    def price_formatter(x, pos):
        return '${:,.2f}'.format(x)

    plt.figure(figsize=(12, 6))
    plt.barh(top_5_food_names, top_5_prices)
    plt.xlabel('Total Sum of Prices')
    plt.ylabel('Food Name')
    plt.title('Expensive Foods across the Countries')
    plt.grid(axis='x')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(FuncFormatter(price_formatter))
    plt.show()
top5food(df)
