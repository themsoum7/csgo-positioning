from demoparser.demofile import DemoFile
import pandas as pd
import os

def get_coordinates():
    def m_start(event, msg):
        result.append("Match start")

    def r_start(event, msg):
        for idx, key in enumerate(event['event'].keys):
            if key.name == 'objective':
                objective = msg.keys[idx].val_string

        result.append([objective])

    def r_end(event, msg):
        for idx, key in enumerate(event['event'].keys):
            if key.name == 'winner':
                winner = msg.keys[idx].val_byte
            elif key.name == 'reason':
                reason = msg.keys[idx].val_byte
            elif key.name == 'legacy':
                legacy = msg.keys[idx].val_byte
            elif key.name == 'message':
                message = msg.keys[idx].val_string
            elif key.name == 'player_count':
                player_count = msg.keys[idx].val_short

        result.append([message])

    def death(event, msg):
        for idx, key in enumerate(event['event'].keys):
            if key.name == 'attacker':
                user_id = msg.keys[idx].val_short
                attacker = d.entities.get_by_user_id(user_id)
            elif key.name == 'userid':
                user_id = msg.keys[idx].val_short
                victim = d.entities.get_by_user_id(user_id)
            elif key.name == 'weapon':
                weapon = msg.keys[idx].val_string
            elif key.name == 'headshot':
                headshot = msg.keys[idx].val_bool

        if attacker and victim:
            result.append([attacker.position, victim.position])

    def remove_warmup(res_list):
        match_start_idx = len(res_list) - 1 - res_list[::-1].index("Match start")
        new_res_list = res_list[match_start_idx:]
        return new_res_list

    def create_final_res(res_lst):
        new_result = remove_warmup(res_lst)
        res_with_round_num = define_round_num(new_result)
        res_no_trash = remove_trash(res_with_round_num)

        return res_no_trash

    def define_round_num(new_res_list):
        counter = 1
        for i in range(len(new_res_list)):
            if new_res_list[i] in ct_round_end_msgs:
                new_res_list[i] = [{"Round msg": new_res_list[i][0], "round num": counter, "winner team": "CTs win"}]
                counter += 1
            elif new_res_list[i] in t_round_end_msgs:
                new_res_list[i] = [{"Round msg": new_res_list[i][0], "round num": counter, "winner team": "Ts win"}]
                counter += 1

        return new_res_list

    def remove_trash(new_res_list):
        for el in new_res_list:
            if el == "Match start" or el == ['BOMB TARGET']:
                new_res_list.pop(new_res_list.index(el))
        return new_res_list


    def create_lists(new_res_list, att_list, vic_list, r_list, wnr_list, tms_list):
        round_counter = 1
        kill_counter = 0
        kills_counter = []
        final_winner_list = []
        final_team_list = []
        idx = 0
        rnd_cntr = 1
        team_one = ""
        team_two = ""

        for el in new_res_list:
            if len(el) == 1:
                round_counter += 1
                kills_counter.append(kill_counter)
                kill_counter = 0
                wnr_list.append(el[0].get("winner team", ""))
            else:
                att_list.append(el[0])
                vic_list.append(el[1])
                r_list.append(round_counter)
                kill_counter += 1

        for el in wnr_list:
            if rnd_cntr == 1:
                team_one = el

            if rnd_cntr == 15:
                team_two = team_one
                team_one = ""

            if rnd_cntr < 15:
                if el == team_one:
                    tms_list.append("Team 1")

                else:
                    tms_list.append("Team 2")
            else:
                if el == team_two:
                    tms_list.append("Team 2")
                else:
                    tms_list.append("Team 1")

            rnd_cntr += 1

        for el in kills_counter:
            for i in range(el):
                final_team_list.append(tms_list[idx])
                final_winner_list.append(wnr_list[idx])
            idx += 1

        return att_list, vic_list, r_list, final_winner_list, final_team_list


    def split_x_y_z(att_or_vic_list, att_or_vic_x, att_or_vic_y, att_or_vic_z):
        for el in att_or_vic_list:
            att_or_vic_x.append(el['x'])
            att_or_vic_y.append(el['y'])
            att_or_vic_z.append(el['z'])

        return att_or_vic_x, att_or_vic_y, att_or_vic_z

    def create_df_from_res(att_x, att_y, att_z, vic_x, vic_y, vic_z, rnds, wnrs, tms):
        data_frame = pd.DataFrame({'attacker_x': att_x,
                           'attacker_y': att_y,
                           'attacker_z': att_z,
                           'victim_x': vic_x,
                           'victim_y': vic_y,
                           'victim_z': vic_z,
                           'round': rnds,
                           'wnr_team': wnrs,
                           'team_num': tms
                          })
        return data_frame

    # points for old dust 2: StartX = -2486; StartY = -1150; EndX = 2127; EndY = 3455; ResX = 1024; ResY = 1024;

    def pointx_to_resolutionx(xinput, startX = -2486, endX = 2127, resX = 1024):
        sizeX = endX - startX
        if startX < 0:
            xinput += startX * (-1.0)
        else:
            xinput += startX
        xoutput = float((xinput / abs(sizeX)) * resX)
        return xoutput

    def pointy_to_resolutiony(yinput, startY = -1150, endY = 3455, resY = 1024):
        sizeY = endY - startY
        if startY < 0:
            yinput += startY * (-1.0)
        else:
            yinput += startY
        youtput = float((yinput / abs(sizeY)) * resY)
        return resY - youtput - 10


    # def convert_data(dataframe, list_of_dfs, rnds, wnrs, tms):
    #     new_df = pd.DataFrame()
    #     # Convert the data to radar positions
    #     new_df['att_map_x'] = dataframe['attacker_x'].apply(pointx_to_resolutionx)
    #     new_df['att_map_y'] = dataframe['attacker_y'].apply(pointy_to_resolutiony)
    #     new_df['vic_map_x'] = dataframe['victim_x'].apply(pointx_to_resolutionx)
    #     new_df['vic_map_y'] = dataframe['victim_y'].apply(pointy_to_resolutiony)
    #     new_df['round'] = rnds
    #     new_df['winner_team'] = wnrs
    #     new_df['team_num'] = tms
    #     list_of_dfs.append(new_df)
    #
    #     return list_of_dfs

    def convert_data(dataframe, actual_df, rnds, wnrs, tms):
        new_df = pd.DataFrame()
        # Convert the data to radar positions
        new_df['att_map_x'] = dataframe['attacker_x'].apply(pointx_to_resolutionx)
        new_df['att_map_y'] = dataframe['attacker_y'].apply(pointy_to_resolutiony)
        new_df['vic_map_x'] = dataframe['victim_x'].apply(pointx_to_resolutionx)
        new_df['vic_map_y'] = dataframe['victim_y'].apply(pointy_to_resolutiony)
        new_df['round'] = rnds
        new_df['winner_team'] = wnrs
        new_df['team_num'] = tms
        actual_df.append(new_df)

        return actual_df

    # def df_to_csv(list_of_demos, list_of_dfs):
    #     for i in range(len(list_of_demos)):
    #         for j in range(len(list_of_dfs)):
    #             if i == j:
    #                 list_of_dfs[j].to_csv('../csv/{}.csv'.format(list_of_demos[i]))

    def df_to_csv(actual_df, actual_clear_df):
        actual_df[0].to_csv('../csv/{}.csv'.format(actual_clear_df[0]))

    def all_processes(res):
        final_res = create_final_res(res)
        attackers_list, victims_list, rounds_list, winner_list, teams_list = create_lists(final_res, attackers, victims,
                                                                                          rounds, winners, teams)
        attackers_x, attackers_y, attackers_z = split_x_y_z(attackers, attacker_x, attacker_y, attacker_z)
        vitctims_x, victims_y, victims_z = split_x_y_z(victims, victim_x, victim_y, victim_z)
        df = create_df_from_res(attacker_x, attacker_y, attacker_z, victim_x, victim_y, victim_z, rounds_list, winner_list, teams_list)
        all_demos_result.append(final_res)
        new_dff = convert_data(df, current_df, rounds_list, winner_list, teams_list)
        df_to_csv(current_df, clear_demos_list)
        
        return all_demos_result

    all_demos_result = []
    current_df = []
    ct_round_end_msgs = [['#SFUI_Notice_Bomb_Defused'], ['#SFUI_Notice_CTs_Win'], ['#SFUI_Notice_Target_Saved']]
    t_round_end_msgs = [['#SFUI_Notice_Terrorists_Win'], ['#SFUI_Notice_Target_Bombed']]

    demos_list = []
    clear_demos_list = []

    for file in os.listdir("../uploads"):
        if file.endswith(".dem"):
            demos_list.append(os.path.join("../uploads/", file))
            clear_demos_list.append(os.path.splitext(file)[0])

    for demo in demos_list:
        result = []
        attackers, victims, rounds, attacker_x, attacker_y, attacker_z, victim_x, victim_y, victim_z, winners, teams = [], [], [], [], [], [], [], [], [], [], []
        data = open(demo, 'rb').read()
        d = DemoFile(data)
        d.add_callback('round_announce_match_start', m_start)
        d.add_callback('round_start', r_start)
        d.add_callback('player_death', death)
        d.add_callback('round_end', r_end)
        d.parse()
        res = all_processes(result)
    return res
