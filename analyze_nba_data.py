import pandas as pd
import datetime
import json

#NBA ANALYSIS FUNCTIONS
def clean_df(df):
    df = df.drop(columns=['SEASON_ID', 'PLAYER_ID', 'TEAM_ID','VIDEO_AVAILABLE'])
    df['GAME_DATE'] = df['GAME_DATE'].astype(str)
    return df
def get_time_ellapsed(str_date):
    ymd = str_date.split('-')
    y = int(ymd[0])
    m = int(ymd[1])
    d = int(ymd[2])
    then = datetime.datetime(y,m,d)
    rn = datetime.datetime.now()
    delta = rn - then
    return delta.days
def make_days_since_col(df):
    dates = df['GAME_DATE']
    days_since_arr = []
    for i in dates:
        days_since_arr.append(get_time_ellapsed(i))
    df['DAYS_SINCE_RN'] = days_since_arr
    last_game = df['DAYS_SINCE_RN'][0]
    df['DAYS_SINCE_RN'] = df['DAYS_SINCE_RN'] - last_game
    return df
def get_team_df(team, df):
    team_df = df[df['TEAM_ABBREVIATION']==team]
    return team_df
def get_player_df(player, df):
    player_df = df[df['PLAYER_NAME']==player]
    return player_df
def predict_lineup(team_df):
    days_since_last_game = team_df['DAYS_SINCE_RN'].min()
    lineup_df = team_df[(team_df['DAYS_SINCE_RN'] - days_since_last_game)<=7]
    players = lineup_df['PLAYER_NAME'].unique()
    lineup_out = {}
    for player in players:
        player_df = lineup_df[lineup_df['PLAYER_NAME'] == player]
        lineup_out[player] = player_df['MIN'].mean()
    import operator
    line_up_sorted_12 = list(reversed(sorted(lineup_out.items(), key=operator.itemgetter(1))))[:12]
    lineup = []
    for obj in line_up_sorted_12:
        lineup.append(obj[0])
    return lineup
def predict_stat(player, stat, df):
    player_df = get_player_df(player, df)
    sum_days = 0
    for num_days in player_df['DAYS_SINCE_RN']:
        sum_days += num_days
    importances = []
    for num_days in player_df['DAYS_SINCE_RN']:
        importance = ((sum_days - num_days)/sum_days)
        importances.append(importance**4)
    sum_days
    stat_ser = player_df[stat]
    stats = []
    for stat in stat_ser:
        stats.append(int(stat))
    scores = []
    for i in range(len(stats)):
        score = importances[i]*stats[i]
        scores.append(score)
    sum_importance = 0
    for imp in importances:
        sum_importance += imp
    if (sum_importance == 0):
        return sum(scores)
    else:
        p_stat = sum(scores)/sum_importance
        return round(p_stat, 2)
def make_json_df(nba_json):
    headers = nba_json['resultSets'][0]['headers']
    data = nba_json['resultSets'][0]['rowSet']
    df = pd.DataFrame(data, columns=headers)
    return df
def predict_team(t):
    with open('data/nba_team_boxscores.json') as file_in:
        nba_t_json = json.load(file_in)
    df = make_json_df(nba_t_json)
    t_df = df[df['TEAM_ABBREVIATION'] == t]
    t_games = list(t_df['GAME_ID'])
    t_match_df = df[df['GAME_ID'].isin(t_games)]
    t_opp_df = t_match_df[t_match_df['TEAM_ABBREVIATION'] != t]
    t_opp_pts = list(t_opp_df['PTS'])
    t_pts = t_df['PTS']
    while len(t_opp_pts) < len(t_df):
        t_opp_pts.append(sum(t_opp_pts)/len(t_opp_pts))
    pts_list = []
    for pts in t_df['PTS']:
        pts_list.insert(0, pts)
    t_df['pts_r'] = pts_list
    o_pts_list = []
    for o_pts in t_opp_pts:
        o_pts_list.insert(0, o_pts)
    t_df['o_pts_r'] = o_pts_list
    predicted_pts = t_df['pts_r'].ewm(alpha=.5).mean().iloc[-1]
    predicted_opp_pts = t_df['o_pts_r'].ewm(alpha=.5).mean().iloc[-1]
    return {'predicted_pts': predicted_pts, 'predicted_opp_pts': predicted_opp_pts}
