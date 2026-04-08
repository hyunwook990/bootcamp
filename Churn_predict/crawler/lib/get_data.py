import json
import time
import requests
import numpy as np
import pandas as pd
from collections import defaultdict
from itertools import product


# player 정보 가져오기기
def get_player_info(tiers, divisions, api_key, header):
    queue = "RANKED_SOLO_5x5"  # 솔로 랭크크

    # tier와 division을 1 대 n으로 묶어줌
    tiers_divisions = product(*[tiers, divisions])

    # data frame init
    player_id_list = defaultdict(list)

    for tier, division in tiers_divisions:
        for page in range(1, 1001):  # 1 ~ 1000 페이지까지 (끝페이지가 어딘지 알 수 없어 최대한 많은 페이지로로)
            player_id_url = f"https://kr.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}?page={page}&api_key={api_key}"

            # 205명 유저 불러와짐
            player_id_info = requests.get(player_id_url, headers=header).json()
            print(player_id_info)

            if player_id_info:  # 유저 id 정보가 있다면
                for player_id in player_id_info:
                    for key, value in player_id.items():
                        player_id_list[key].append(value)
                if not (page % 100):  # API를 100번 불러왔으면 2분 딜레이
                    time.sleep(120)
            else:  # 유저 id 정보가 없다면
                time.sleep(120)  # 무조건 2분 딜레이
                break

        # CHALLENGER, GRANDMASTER, MASTER는 division이 1개뿐
        if (tier == "CHALLENGER") or (tier == "GRANDMASTER") or (tier == "MASTER"):
            break

    player_id_df = pd.DataFrame(player_id_list)
    player_id_df.to_csv(f"bg_player_info.csv", index=False, encoding="utf-8")
    
    return player_id_list

def get_summoner(puuids, api_key, headers):
    player_summoner_list = defaultdict(list)

    for idx, puuid in enumerate(puuids):
        summoner_url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"

        if not (idx % 100):
            player_summoner_api = requests.get(summoner_url, headers=headers).json()
            for key, value in player_summoner_api.items():
                player_summoner_list[key].append(value)
            print(player_summoner_list)
            time.sleep(120)
        else:
            player_summoner_api = requests.get(summoner_url, headers=headers).json()
            for key, value in player_summoner_api.items():
                player_summoner_list[key].append(value)

    summoner_df = pd.DataFrame(player_summoner_list)
    summoner_df.to_csv("bg_player_summoner.csv", index=False, encoding="utf-8")

    return player_summoner_list

def get_champion_mastery(puuids, api_key, headers):
    champion_mastery_list = defaultdict(list)

    for idx, puuid in enumerate(puuids):
        if (idx != 0) and not(idx % 100):
            for key, value in champion_mastery_list.items():
                print(f"{key} of champion_mastery_list count : {len(value)}")
            champion_mastery_df = pd.DataFrame(champion_mastery_list)
            champion_mastery_df.to_csv(f"data/champion/champion_mastery{idx}.csv", index=False, encoding="utf-8")
            champion_mastery_list = defaultdict(list)
            time.sleep(120)

        champion_api_url = f"https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count=3&api_key={api_key}"
        
        champion_api = requests.get(champion_api_url, headers=headers).json()

        for champion in champion_api:
            if ("milestoneGrades" not in champion.keys()):
                champion_mastery_list["milestoneGrades"].append("NaN")
            for key, value in champion.items():
                if key == "status":
                    continue
                if (key == "milestoneGrades") and (len(value) == 0):
                    champion_mastery_list[key].append("NaN")
                else:
                    champion_mastery_list[key].append(value)

        # print(champion_mastery_list)

    champion_mastery_df = pd.DataFrame(champion_mastery_list)
    champion_mastery_df.to_csv("data/champion/champion_mastery.csv", index=False, encoding="utf-8")

    return champion_mastery_list

        