import os
import json
import pandas as pd
from pathlib import Path
import re
from datetime import datetime
from itertools import compress

def get_matches_from_dir(data_dir=os.path.join(os.getcwd(), "match_data"), start_date: str | None = None, 
						 end_date: str | None = None) -> tuple[pd.DataFrame, int]:
	fps = list(Path(data_dir).rglob("*.json"))
	if start_date or end_date:
		fps = filter_fps_by_dates(fps, start_date, end_date)

	matches = []
	failure_count = 0

	for fp in fps:
		try:
			with open(fp) as f:
				json_String = f.read().strip()
				data = json.loads(json_String)
				matches.extend(data['replayDetailList'])
		except Exception as e:
			failure_count += 1

	df = pd.DataFrame(matches)
	df = df.drop_duplicates(subset='battleId', keep="last")
	return df, failure_count

def filter_fps_by_dates(fps: list[str], start_date: str | None, end_date: str | None) -> list[str]:
	matches = list(map(lambda fn: re.search(r"\d\d_\d\d_\d\d", str(fn)), fps))
	if not all(matches):
		print("ERROR: Wrong file format present in data. All folders in match_data/ should contain"
				" a date in the form of '%m_%d_%y'")
		os.exit(1)
	dates = list(map(lambda match: datetime.strptime(match.group(), r"%m_%d_%y"), matches))
	
	if start_date:
		start_date = datetime.strptime(start_date, r"%m_%d_%y")
		is_valid = list(map(lambda d: d >= start_date, dates))
		fps = compress(fps, is_valid)

	if end_date:
		end_date = datetime.strptime(end_date, r"%m_%d_%y")
		is_valid = list(map(lambda d: d <= end_date, dates))
		fps = compress(fps, is_valid)

	return fps

# Example of a match
# {
#     "battleId": "f7c4c3ba9d9d4484a14d08c9eb1e1f9a",
#     "battleType": 2,
#     "gameVersion": 10104,
#     "winResult": 2,
#     "totalRoundNum": 4,
#     "battleAt": 1707948450,
#     "viewNum": 0,
#     "stageId": "stg_1600",
#     "highlightFlag": false,
#     "1pUserId": "023591240125230934",
#     "1pPlayerName": "Shadowmane",
#     "1pPolarisId": "33Ge2NF493EJ",
#     "1pOnlineId": "Ghetto63zoo",
#     "1pNgWordFlag": 0,
#     "1pPlatform": 8,
#     "1pRank": 13,
#     "1pTekkenPower": 92575,
#     "1pCharaId": "chr_0029",
#     "1pWinRoundNum": 1,
#     "1pTagType01": 0,
#     "1pTagType02": 0,
#     "1pTagType03": 0,
#     "2pUserId": "894212240204104936",
#     "2pPlayerName": "Ramma",
#     "2pPolarisId": "3dJhi33AmJHn",
#     "2pOnlineId": "Ramazan123-",
#     "2pNgWordFlag": 0,
#     "2pPlatform": 8,
#     "2pRank": 10,
#     "2pTekkenPower": 74847,
#     "2pCharaId": "chr_0006",
#     "2pWinRoundNum": 3,
#     "2pTagType01": 0,
#     "2pTagType02": 0,
#     "2pTagType03": 0
# },