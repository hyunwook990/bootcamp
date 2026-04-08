import os
import time
import pandas as pd
from lib.get_data import get_player_info, get_summoner, get_champion_mastery

if __name__ == "__main__":
    api_key = ""  # 새로 발급받은 api_key
    # header 정보
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": api_key,
    }

    # 데이터셋 경로 받아오기기
    path1 = os.path.join(os.getcwd(), "data\\reduction_data\\BRONZE.csv")
    path2 = os.path.join(os.getcwd(), "data\\reduction_data\\GRANDMASTER.csv")

    tier_df1 = pd.read_csv(path1, encoding="utf-8")
    tier_df2 = pd.read_csv(path2, encoding="utf-8")

    # player의 정보에서 puuid로 summoner 가져오기기
    player_info = pd.concat([tier_df1, tier_df2], axis=0)
    puuids = player_info["puuid"].values
    # print(player_info)

    # tiers = ["PLATINUM", "EMERALD"] # IRON, BRONZE, SILVER, GOLD, PLATINUM, EMERALD, DIAMOND, MASTER, GRANDMASTER, CHALLENGER
    # divisions = ["IV", "III", "II", "I"]

    # player 정보 가져오기기 
    # start = time.time()
    # player_info = get_player_info(tiers, divisions, api_key, header)
    # end = time.time()

    # 시간 측정
    # print(f"{end - start:.5f} sec")

    # ----------------------------------------------------------------------------------------

    # start = time.time()
    # player_summoner = get_summoner(player_info, api_key, header)
    # end = time.time()

    # 시간 측정
    # print(f"{end - start:.5f} sec")

    # ----------------------------------------------------------------------------------------

    start = time.time()
    player_summoner = get_champion_mastery(puuids, api_key, header)

    end = time.time()

    # 시간 측정
    print(f"{end - start:.5f} sec")