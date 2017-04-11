from lxml import html
import requests
import re
import pandas as pd

def find_rank(ranker):
    regex = re.findall(r"[0-9]+", ranker)
    return regex[0]

def find_team_name(team_name):
    team_pattern_stat_list = r"teams/" + r"[\w]*"
    team_name_code = re.findall(team_pattern_stat_list, team_name)
    return team_name_code[0][6:]

def find_team_row(team_stat_list, col_names):
    # TODO: Add breaks for errors
    dict = {}
    col_stat = zip(col_names[2:], team_stat_list[5:-1])
    for stat in col_stat:
        stat_pattern = r">" + r"[\.0-9]+" + r"<"
        x = re.findall(stat_pattern, stat[1]) 
        if x:
            dict[stat[0]] = float(x[0][1:-1])
    ranker_raw = team_stat_list[1]
    team_name_raw = team_stat_list[3]
    dict[team_cols[0]] = find_rank(ranker_raw)
    dict[team_cols[1]] = find_team_name(team_name_raw)
    return dict

def find_stats_string(text, table_indicator="Team Stats Table"):
    string_split = text.split("\n")
    start_idx = 0
    for i, S in enumerate(string_split):
        res = re.findall(table_indicator, S)
        if len(res) != 0:
            start_idx = i
    return string_split, start_idx


# find column names from string
def find_team_cols(text):
    #TODO: Fix magic numbers
    string_split, start_idx = find_stats_string(text, table_indicator="Opponent Stats Table") # test
    columns = string_split[start_idx+4:start_idx+30]
    team_cols = []
    for word in columns:
        w = re.findall(r"data-stat=\"+[\w]*", word)
        if w:
            team_cols.append(w[0][11:])
    return team_cols
# team_cols = find_team_cols(text) # test

def find_team_row(team_stat_list, team_cols):
    #TODO: Fix magic numbers
    dict = {}
    col_stat = zip(team_cols[2:], team_stat_list[5:-1])
    for stat in col_stat:
        stat_pattern = r">" + r"[\.0-9]+" + r"<"
        x = re.findall(stat_pattern, stat[1]) 
        if x:
            dict[stat[0]] = float(x[0][1:-1])
    dict[team_cols[0]] = find_rank(team_stat_list[1])
    dict[team_cols[1]] = find_team_name(team_stat_list[3])
    return dict

def make_one_year_team_cols_df(year=2016, table_indicator="Team Stats Table"):
    page = requests.get('http://www.basketball-reference.com/friv/standings.fcgi?month=6&day=20&year=%d&lg_id=NBA' %year)
    text = page.text
    team_cols = find_team_cols(text)
    string_split, start_idx = find_stats_string(text, table_indicator)
    #TODO: Fix magic numbers to match number teams in the NBA by year and stats
    raw_team_stats = string_split[start_idx + 33:start_idx + 63]
    team_rows_list = []
    for raw_team_stat in raw_team_stats:
        raw_team_stat_split = raw_team_stat.split("><")
        rank_team_row = find_team_row(raw_team_stat_split, team_cols)
        team_rows_list.append(pd.DataFrame(rank_team_row, index=[1]))
    df = pd.concat(team_rows_list)
    df.set_index("ranker", inplace=True) # set index by rank
    return df[["team_name"] + team_cols[2:]] # reorder columns
# df = make_one_year_team_cols_df(2016, table_indicator="Opponent Stats Table") #test
