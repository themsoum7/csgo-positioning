import pandas as pd
import os
import matplotlib.pyplot as plt
from server.get_coordinates import *

# res_list = [[[]]] # test with copied list
res_list = get_coordinates()

def csv_to_df(list_of_csv):
    for csv in list_of_csv:
        df = pd.read_csv(csv, index_col = 0)
    return df

def economy(dataframe):
    t_buy_level = 0
    ct_buy_level = 0
    counter = 1
    win_streak = 0
    prev_winner = ''

    for i in range(len(res_list[0])):
        if len(res_list[0][i]) == 1:
            rnd_winner = res_list[0][i][0].get("winner team")
            if counter == 1 or counter == 16:
                win_streak = 0
                if rnd_winner:
                    win_streak += 1
                ct_buy_level = 1
                t_buy_level = 1

            if counter == 2 or counter == 17:
                if rnd_winner == "CTs win":
                    if rnd_winner == prev_winner:
                        win_streak += 1
                        ct_buy_level = 2.5
                        t_buy_level = 1.5
                    else:
                        win_streak = 1
                        ct_buy_level = 1.5
                        t_buy_level = 2.5
                    
            if counter == 3 or counter == 18:
                if rnd_winner == "Ts win":
                    if rnd_winner == prev_winner:
                        win_streak += 1
                        ct_buy_level = 1.5
                        t_buy_level = 2.7
                    else:
                        win_streak = 1
                        ct_buy_level = 2.7
                        t_buy_level = 1.5

            if 3 < counter <= 15 or 18 < counter <= 30:
                if rnd_winner == "CTs win":
                    if rnd_winner != prev_winner:
                        win_streak = 1
                        # ct_buy_level += 0.2
                        t_buy_level -= 0.5
                    else:
                        if win_streak > 4 and t_buy_level == 2.5:
                            t_buy_level = 3
                        elif win_streak > 4 and t_buy_level == 3:
                            t_buy_level = 2.5
                        else:
                            win_streak += 1
                            if win_streak >= 4:
                                ct_buy_level += 0.7
                                t_buy_level = 2.5
                            else:
                                if win_streak > 1 and ct_buy_level < 3:
                                    t_buy_level += 0.5
                                else:
                                    ct_buy_level += 0.4
                                    t_buy_level -= 0.5
                                if t_buy_level < 1:
                                    t_buy_level = 1
                                
                    if ct_buy_level > 5:
                        ct_buy_level = 5
                    if t_buy_level > 5:
                        t_buy_level = 5
                    
                elif rnd_winner == "Ts win":
                    if rnd_winner != prev_winner:
                        win_streak = 1
                        ct_buy_level -= 0.8
                        # t_buy_level += 0.5
                    else:
                        if win_streak > 4 and ct_buy_level == 2.5:
                            ct_buy_level = 3
                        elif win_streak > 4 and ct_buy_level == 3:
                            ct_buy_level = 2.5
                        else:
                            win_streak += 1
                            if win_streak >= 4:
                                ct_buy_level = 2.5
                                t_buy_level += 0.7
                            else:
                                if win_streak > 1 and t_buy_level < 3:
                                    ct_buy_level += 0.5
                                else:
                                    ct_buy_level -= 0.4
                                    t_buy_level += 0.4
                                if ct_buy_level < 1:
                                    ct_buy_level = 1

                    if ct_buy_level > 5:
                        ct_buy_level = 5
                    if t_buy_level > 5:
                        t_buy_level = 5
            res_list[0][i][0]["t buy level"] = round(t_buy_level, 1)
            res_list[0][i][0]["ct buy level"] = round(ct_buy_level, 1)
            res_list[0][i] = [res_list[0][i][0]]
            # res_list[0][i] = [res_list[0][i][0], {"t buy level": round(t_buy_level, 1), "ct buy level": round(ct_buy_level, 1)}]
            prev_winner = dataframe['winner_team'].loc[dataframe['round'] == counter].unique()
            counter += 1
    return res_list[0]


def add_levels_to_df(result_lst, ct_lvl_list, t_lvl_list, result_dataframe):
    kills_counter = []
    kill_counter = 0
    idx = 0
    final_ct_lvl_list = []
    final_t_lvl_list = []

    for el in result_lst:
        if len(el) == 1:
            kills_counter.append(kill_counter)
            kill_counter = 0
            ct_lvl_list.append(el[0].get("ct buy level", ""))
            t_lvl_list.append(el[0].get("t buy level", ""))
        else:
            kill_counter += 1

    for el in kills_counter:
        for i in range(el):
            final_ct_lvl_list.append(ct_lvl_list[idx])
            final_t_lvl_list.append(t_lvl_list[idx])
        idx += 1
    result_dataframe['ct_buy_level'] = final_ct_lvl_list
    result_dataframe['t_buy_level'] = final_t_lvl_list

    return result_dataframe


def df_to_csv(new_df, actual_clear_df):
    new_df.to_csv('../economy_csv/{}_economy.csv'.format(actual_clear_df[0]))

def economy_res():
    current_csv = []
    current_csv_name = []

    for file in os.listdir("../csv"):
        if file.endswith(".csv"):
            current_csv.append(os.path.join("../csv/", file))
            current_csv_name.append(os.path.splitext(file)[0])

    res_df = csv_to_df(current_csv)
    res = economy(res_df)
    ct_lvls = []
    t_lvls = []
    new_res_df = add_levels_to_df(res, ct_lvls, t_lvls, res_df)
    df_to_csv(new_res_df, current_csv_name)