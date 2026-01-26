import requests
import json

request_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,und;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}

player_request_payload = {
    'Counter': '15990',
    'DateFrom': '',
    'DateTo': '',
    'Direction': 'DESC',
    'LeagueID': '00',
    'PlayerOrTeam': 'P',
    'Season': '2025-26',
    'SeasonType': 'Regular Season',
    'Sorter': 'DATE'
}

#DATA MINING FUNCTION
def get_player_data():
    base_url = "https://stats.nba.com/stats/leaguegamelog"
    re = requests.get(base_url, headers=request_headers, params=player_request_payload)
    print(re.status_code)
    nba_p_json = json.loads(re.text)
    return nba_p_json

def get_teams_data():
    team_url = "https://stats.nba.com/stats/leaguegamefinder?Conference=&DateFrom=&DateTo=&Division=&DraftNumber=&DraftRound=&DraftYear=&GB=N&LeagueID=00&Location=&Outcome=&PlayerOrTeam=T&Season=2022-23&SeasonType=&StatCategory=PTS&TeamID=&VsConference=&VsDivision=&VsTeamID="
    re = requests.get(team_url, headers=request_headers)
    print(re.status_code)
    nba_t_json = json.loads(re.text)
    return nba_t_json

#DATA LOCALIZATION
def localize_data():
    nba_p_json = get_player_data()
    with open("data/nba_player_boxscores.json", "w") as file_p_out:
        json.dump(nba_p_json, file_p_out)
    nba_t_json = get_teams_data()
    with open("data/nba_team_boxscores.json", "w") as file_t_out:
        json.dump(nba_t_json, file_t_out)
