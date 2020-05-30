#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

def csvs_to_dfs(list_of_csv):
    current_df = []
    
    for csv in list_of_csv:
        df = pd.read_csv(csv, index_col = 0)
        current_df.append(df)
    return current_df

im = plt.imread('../maps/de_dust2.png')


# def plot_image(dataframe, idx, list_of_csv):
#     fig, ax = plt.subplots(figsize = (20, 20))
#
#     ax.scatter(dataframe.att_map_x, dataframe.att_map_y, alpha = 1, c = 'b')
#     ax.scatter(dataframe.vic_map_x, dataframe.vic_map_y, alpha = 1, c = 'r')
#
#     ax.imshow(im)
#
#     plt.savefig('./images/{}.jpg'.format(list_of_csv[idx]))
#
#
#
#
# def plot_image_with_lines(dataframe, idx, list_of_csv):
#     fig, ax = plt.subplots(figsize = (20, 20))
#
#     ax.scatter(dataframe.att_map_x, dataframe.att_map_y, alpha = 1, c = 'b')
#     ax.scatter(dataframe.vic_map_x, dataframe.vic_map_y, alpha = 1, c = 'r')
#
#     for j in range(len(dataframe)):
#         xyA = dataframe.att_map_x[j], dataframe.att_map_y[j]
#         xyB = dataframe.vic_map_x[j], dataframe.vic_map_y[j]
#
#         con = ConnectionPatch(xyA, xyB, coordsA = "data", coordsB = "data",
#                               arrowstyle="-", shrinkA=5, shrinkB=5,
#                               mutation_scale=20, fc="w")
#         ax.add_artist(con)
#
#     ax.imshow(im)
#
#     plt.savefig('./images_by_sides/{}.jpg'.format(list_of_csv[idx]))
#


def plot_image_by_rounds(dataframe, csv_name):
    last_idx = 0

    for j in range(dataframe['round'].nunique()):
        fig, ax = plt.subplots(figsize = (20, 20))
        current_demo_round = dataframe.loc[dataframe['round'] == j + 1]

        plt.title("Round outcome: " + current_demo_round.winner_team.to_list()[0], fontsize = 30)

        ax.scatter(current_demo_round.att_map_x, current_demo_round.att_map_y, alpha = 1, c = 'b', s = 19**2, edgecolors='black')
        ax.scatter(current_demo_round.vic_map_x, current_demo_round.vic_map_y, alpha = 1, c = 'r', s = 19**2, edgecolors='black')

        for i in range(len(current_demo_round)):
            xy_a = current_demo_round.att_map_x[i + last_idx], current_demo_round.att_map_y[i + last_idx] 
            xy_b = current_demo_round.vic_map_x[i + last_idx], current_demo_round.vic_map_y[i + last_idx] 
                
            con = ConnectionPatch(xy_a, xy_b, coordsA = "data", coordsB = "data",
                                    arrowstyle="-|>", shrinkA=5, shrinkB=5,
                                    mutation_scale=20, fc="w")
            ax.add_artist(con)

        last_idx += len(current_demo_round)

        ax.imshow(im)

        plt.savefig('./static/images_by_rounds/{}_round_{}.jpg'.format(csv_name, j + 1))
        plt.close()


def return_round_num(dataframe):
    return dataframe['round'].unique().tolist()


# def plot_image_by_sides(list_of_dfs, winner_side):
#     # plot images by sides NOT TEAMS
#     for i in range(len(list_of_dfs)):
#         fig, ax = plt.subplots(figsize = (20, 20))
#
#         demo_by_side = list_of_dfs[i].loc[list_of_dfs[i]['winner_team'] == winner_side]
#
#         ax.scatter(demo_by_side.att_map_x, demo_by_side.att_map_y, alpha = 1, c = 'b')
#         ax.scatter(demo_by_side.vic_map_x, demo_by_side.vic_map_y, alpha = 1, c = 'r')
#
#         ax.imshow(im)


def plot_ct_side(dataframe, ct_side, csv_name):
    # plot images by sides NOT TEAMS
    fig, ax = plt.subplots(figsize = (20, 20))

    demo_by_side = dataframe.loc[dataframe['winner_team'] == ct_side]
    plt.title('Demo plot for CT side for both teams', fontsize = 30)
    ax.scatter(demo_by_side.att_map_x, demo_by_side.att_map_y, alpha = 1, c = 'b', s = 15**2, edgecolors='black')
    ax.scatter(demo_by_side.vic_map_x, demo_by_side.vic_map_y, alpha = 1, c = 'r', s = 15**2, edgecolors='black')

    for j in range(len(demo_by_side)):
        xyA = demo_by_side.att_map_x.to_list()[j], demo_by_side.att_map_y.to_list()[j]
        xyB = demo_by_side.vic_map_x.to_list()[j], demo_by_side.vic_map_y.to_list()[j]

        con = ConnectionPatch(xyA, xyB, coordsA = "data", coordsB = "data",
                              arrowstyle="-|>", shrinkA=5, shrinkB=5,
                              mutation_scale=20, fc="w")
        ax.add_artist(con)

    ax.imshow(im)

    plt.savefig('./static/image_ct_side/{}_ct_side.jpg'.format(csv_name))
    plt.close()


def plot_t_side(dataframe, t_side, csv_name):
    # plot images by sides NOT TEAMS
    fig, ax = plt.subplots(figsize = (20, 20))

    demo_by_side = dataframe.loc[dataframe['winner_team'] == t_side]
    plt.title('Demo plot for T side for both teams', fontsize = 30)
    ax.scatter(demo_by_side.att_map_x, demo_by_side.att_map_y, alpha = 1, c = 'b', s = 15**2, edgecolors='black')
    ax.scatter(demo_by_side.vic_map_x, demo_by_side.vic_map_y, alpha = 1, c = 'r', s = 15**2, edgecolors='black')

    for j in range(len(demo_by_side)):
        xyA = demo_by_side.att_map_x.to_list()[j], demo_by_side.att_map_y.to_list()[j]
        xyB = demo_by_side.vic_map_x.to_list()[j], demo_by_side.vic_map_y.to_list()[j]

        con = ConnectionPatch(xyA, xyB, coordsA = "data", coordsB = "data",
                              arrowstyle="-|>", shrinkA=5, shrinkB=5,
                              mutation_scale=20, fc="w")
        ax.add_artist(con)

    ax.imshow(im)

    plt.savefig('./static/image_t_side/{}_t_side.jpg'.format(csv_name))
    plt.close()


def plot_image_by_team_one(dataframe, tm_one, csv_name):
    fig, ax = plt.subplots(figsize = (20, 20))

    demo_by_team_num = dataframe.loc[dataframe['team_num'] == tm_one]
    plt.title('Demo plot for Team 1', fontsize = 30)
    ax.scatter(demo_by_team_num.att_map_x, demo_by_team_num.att_map_y, alpha = 1, c = 'b', s = 15**2, edgecolors='black')
    ax.scatter(demo_by_team_num.vic_map_x, demo_by_team_num.vic_map_y, alpha = 1, c = 'r', s = 15**2, edgecolors='black')

    for j in range(len(demo_by_team_num)):
        xyA = demo_by_team_num.att_map_x.to_list()[j], demo_by_team_num.att_map_y.to_list()[j]
        xyB = demo_by_team_num.vic_map_x.to_list()[j], demo_by_team_num.vic_map_y.to_list()[j]

        con = ConnectionPatch(xyA, xyB, coordsA = "data", coordsB = "data",
                              arrowstyle="-|>", shrinkA=5, shrinkB=5,
                              mutation_scale=20, fc="w")
        ax.add_artist(con)

    ax.imshow(im)

    plt.savefig('./static/image_team_one/{}_team_one.jpg'.format(csv_name))
    plt.close()


def plot_image_by_team_two(dataframe, tm_two, csv_name):
    fig, ax = plt.subplots(figsize = (20, 20))

    demo_by_team_num = dataframe.loc[dataframe['team_num'] == tm_two]
    plt.title('Demo plot for Team 2', fontsize = 30)
    ax.scatter(demo_by_team_num.att_map_x, demo_by_team_num.att_map_y, alpha = 1, c = 'b', s = 15**2, edgecolors='black')
    ax.scatter(demo_by_team_num.vic_map_x, demo_by_team_num.vic_map_y, alpha = 1, c = 'r', s = 15**2, edgecolors='black')

    for j in range(len(demo_by_team_num)):
        xyA = demo_by_team_num.att_map_x.to_list()[j], demo_by_team_num.att_map_y.to_list()[j]
        xyB = demo_by_team_num.vic_map_x.to_list()[j], demo_by_team_num.vic_map_y.to_list()[j]

        con = ConnectionPatch(xyA, xyB, coordsA = "data", coordsB = "data",
                              arrowstyle="-|>", shrinkA=5, shrinkB=5,
                              mutation_scale=20, fc="w")
        ax.add_artist(con)

    ax.imshow(im)

    plt.savefig('./static/image_team_two/{}_team_two.jpg'.format(csv_name))
    plt.close()
#
#
#
#
# def plot_image_by_teams(list_of_dfs, tm_num):
#     for i in range(len(list_of_dfs)):
#         fig, ax = plt.subplots(figsize = (20, 20))
#
#         demo_by_team_num = list_of_dfs[i].loc[list_of_dfs[i]['team_num'] == tm_num]
#
#         ax.scatter(demo_by_team_num.att_map_x, demo_by_team_num.att_map_y, alpha = 1, c = 'b')
#         ax.scatter(demo_by_team_num.vic_map_x, demo_by_team_num.vic_map_y, alpha = 1, c = 'r')
#
#         ax.imshow(im)
#
#
#
#
# def plot_image_all_matches(list_of_dfs):
#     fig, ax = plt.subplots(figsize = (20, 20))
#     coff = 1
#
#     for i in range(len(list_of_dfs)):
#         ax.scatter(list_of_dfs[i].att_map_x, list_of_dfs[i].att_map_y, alpha = coff, c = 'b')
#         ax.scatter(list_of_dfs[i].vic_map_x, list_of_dfs[i].vic_map_y, alpha = coff, c = 'r')
#         rnd = 1/len(list_of_dfs)
#         coff -= rnd
#
#     ax.imshow(im)

def return_rnd_numbers():
    current_csv = []

    for file in os.listdir("../csv"):
        if file.endswith(".csv"):
            current_csv.append(os.path.join("../csv/", file))

    df = csvs_to_dfs(current_csv)
    round_number = return_round_num(df[0])
    return round_number

def res_images():
    current_csv = []
    current_csv_name = []

    for file in os.listdir("../csv"):
        if file.endswith(".csv"):
            current_csv.append(os.path.join("../csv/", file))
            current_csv_name.append(os.path.splitext(file)[0])

    df = csvs_to_dfs(current_csv)
    cts_win = 'CTs win'
    ts_win = 'Ts win'
    team_one = 'Team 1'
    team_two = 'Team 2'

    plot_image_by_rounds(df[0], current_csv_name[0])
    # plot_image(df, i, list_of_clear_csv)
    # plot_image_with_lines(df, i, list_of_clear_csv)
    # plot_image_all_matches(dfs)
    plot_ct_side(df[0], cts_win, current_csv_name[0])
    plot_t_side(df[0], ts_win, current_csv_name[0])
    plot_image_by_team_one(df[0], team_one, current_csv_name[0])
    plot_image_by_team_two(df[0], team_two, current_csv_name[0])
    # plot_image_by_sides(df[0], ts_win)
    # plot_image_by_teams(dfs, team_one)
    # plot_image_by_teams(dfs, team_two)