nba_range = range(2001, 2017)
df_by_year_off, df_by_year_def = {}, {}
for year in nba_range:
    df_by_year_off[year] = make_one_year_team_cols_df(year, table_indicator="Team Stats Table")
    df_by_year_def[year] = make_one_year_team_cols_df(year, table_indicator="Opponent Stats Table")
