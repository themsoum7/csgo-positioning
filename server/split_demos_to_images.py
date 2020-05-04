#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch


# In[2]:


csv_list = []
list_of_clear_csv = []

for file in os.listdir("../csv"):
    if file.endswith(".csv"):
        csv_list.append(os.path.join("../csv/", file))
        list_of_clear_csv.append(os.path.splitext(file)[0])


# In[3]:


def csvs_to_dfs(list_of_csv):
    list_of_dfs = []
    
    for csv in list_of_csv:
        df = pd.read_csv(csv, index_col = 0)
        list_of_dfs.append(df)
    return list_of_dfs


# In[4]:


im = plt.imread('../maps/de_dust2.png')


# In[5]:


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
# # In[6]:
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
#     plt.savefig('./images_with_lines/{}.jpg'.format(list_of_csv[idx]))
#

# In[7]:


def plot_image_by_rounds(dataframe, idx, list_of_csv):
    for j in range(dataframe['round'].nunique()):
        fig, ax = plt.subplots(figsize = (20, 20))
        current_demo = dataframe.loc[dataframe['round'] == j + 1]
        
        ax.scatter(current_demo.att_map_x, current_demo.att_map_y, alpha = 1, c = 'b')
        ax.scatter(current_demo.vic_map_x, current_demo.vic_map_y, alpha = 1, c = 'r')

        ax.imshow(im)
        plt.savefig('../images_by_rounds/{}_round_{}.jpg'.format(list_of_csv[idx], j + 1))
        plt.clf()


# In[8]:


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
#
#
# # In[9]:
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
# # In[10]:
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


# In[11]:


def res_images():
    dfs = csvs_to_dfs(csv_list)
    cts_win = 'CTs win'
    ts_win = 'Ts win'
    team_one = 'Team 1'
    team_two = 'Team 2'

    for i in range(len(dfs)):
        df = dfs[i]
        plot_image_by_rounds(df, i, list_of_clear_csv)
        # plot_image(df, i, list_of_clear_csv)
        # plot_image_with_lines(df, i, list_of_clear_csv)
        # plot_image_all_matches(dfs)
        # plot_image_by_sides(dfs, cts_win)
        # plot_image_by_sides(dfs, ts_win)
        # plot_image_by_teams(dfs, team_one)
        # plot_image_by_teams(dfs, team_two)

# In[12]:





# In[ ]:




