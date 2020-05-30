import pandas as pd
import os
import matplotlib.pyplot as plt

def csvs_to_dfs(list_of_csv):
    current_df = []
    
    for csv in list_of_csv:
        df = pd.read_csv(csv, index_col = 0)
        current_df.append(df)
    return current_df

def plot_t_economy(dataframe, csv_name):
    # ax = plt.gca()
    # dataframe.plot(kind='line', x='round', y='t_buy_level', ax=ax)
    dataframe.set_index('round')['t_buy_level'].plot()
    plt.xlabel("Round", labelpad=10)
    plt.ylabel("Buy Level", labelpad=15)
    plt.title("T economy level by rounds", y=1.02, fontsize=22)
    plt.xticks(dataframe['round'].unique(), rotation=90)
    plt.savefig('./static/t_economy_plot/{}_t_economy.jpg'.format(csv_name))
    plt.close()

def plot_ct_economy(dataframe, csv_name):
    # ax = plt.gca()
    # dataframe.plot(kind='line', x='round', y='ct_buy_level', ax=ax)
    dataframe.set_index('round')['ct_buy_level'].plot()
    plt.xlabel("Round", labelpad=10)
    plt.ylabel("Buy Level", labelpad=15)
    plt.title("CT economy level by rounds", y=1.02, fontsize=22)
    plt.xticks(dataframe['round'].unique(), rotation=90)
    plt.savefig('./static/ct_economy_plot/{}_ct_economy.jpg'.format(csv_name))
    plt.close()

def economy_images():
    current_csv = []
    current_csv_name = []
    for file in os.listdir("../economy_csv"):
        if file.endswith(".csv"):
            current_csv.append(os.path.join("../economy_csv/", file))
            current_csv_name.append(os.path.splitext(file)[0])

    df = csvs_to_dfs(current_csv)
    plot_t_economy(df[0], current_csv_name[0])
    plot_ct_economy(df[0], current_csv_name[0])
