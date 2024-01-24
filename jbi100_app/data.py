import pandas as pd
import numpy as np

def get_data():

    # Read data
    df_match_data = pd.read_csv('jbi100_app/Data/FIFA World Cup 2022 Match Data/data.csv', delimiter=',')
    df_extra_match_data = pd.read_csv('jbi100_app/Data/Match formations.csv')
    df_extra_shot_data = pd.read_csv('jbi100_app/Data/Match Shots.csv')
    df_extra_info = pd.read_csv('jbi100_app/Data/Match formation.csv')

    # Split the score into home and away scores
    df_match_data[['score_home', 'score_away']] = df_match_data['score'].str.split("–", expand=True)

    # Extract penalty scores if present
    df_match_data['penalty_score_home'] = df_match_data['score_home'].str.extract(r'\((\d+)\)', expand=False)
    df_match_data['penalty_score_away'] = df_match_data['score_away'].str.extract(r'\((\d+)\)', expand=False)

    # Replace scores with penalty scores if applicable
    df_match_data['score_home'] = df_match_data['penalty_score_home'].fillna(df_match_data['score_home'])
    df_match_data['score_away'] = df_match_data['penalty_score_away'].fillna(df_match_data['score_away'])

    # Remove spaces from home and away scores
    df_match_data['score_home'] = df_match_data['score_home'].str.replace(" ", "")
    df_match_data['score_away'] = df_match_data['score_away'].str.replace(" ", "")

    # Drop unnecessary columns
    df_match_data = df_match_data.drop(['penalty_score_home', 'penalty_score_away'], axis=1)

    df_all_match_data = pd.concat([df_match_data, df_extra_match_data],  join="inner", ignore_index=True)
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    winning_formation = []
    losing_formation = []

    for i in range(len(df_all_match_data)) :
        if(df_all_match_data["score_home"][i] < df_all_match_data["score_away"][i]):
                winning_formation.append(df_all_match_data["away_formation"][i])
                losing_formation.append(df_all_match_data["home_formation"][i])
        elif(df_all_match_data["score_home"][i] > df_all_match_data["score_away"][i]):
                winning_formation.append(df_all_match_data["home_formation"][i])
                losing_formation.append(df_all_match_data["away_formation"][i])
        else:
            winning_formation.append(df_all_match_data["away_formation"][i])
            losing_formation.append(df_all_match_data["home_formation"][i])
            winning_formation.append(df_all_match_data["home_formation"][i])
            losing_formation.append(df_all_match_data["away_formation"][i])

    df_wins_losses = pd.DataFrame({
    'winning_formation': winning_formation,
    'losing_formation': losing_formation
    })

    # Drop rows with NaN values (None in the formations)
    df_wins_losses = df_wins_losses.dropna()

    df_wins_losses = df_wins_losses[df_wins_losses['winning_formation'] != df_wins_losses['losing_formation']]

    # create list of dates to use for timeline graph
    date = []
    for i in range(len(df_all_match_data)):
        if(i<len(df_match_data)):
            date.append(df_match_data['match_time'][i])
            if (df_all_match_data["score_home"][i] == df_all_match_data["score_away"][i]):
                 date.append(df_match_data['match_time'][i])
        else:
            date.append(df_extra_match_data['date'][i-len(df_match_data)])
            if (df_all_match_data["score_home"][i] == df_all_match_data["score_away"][i]):
                 date.append(df_extra_match_data['date'][i-len(df_match_data)])
    
    # data for the timeline
    wl_date_df = pd.DataFrame({
    'date': date,
    'winning_formation': winning_formation,
    'losing_formation': losing_formation
    })
    
    wl_data_df_sorted = wl_date_df.sort_values(by='date')

    # all used formations (for timeline)
    # Extract unique formations and count occurrences from home_formation and away_formation columns
    formation_counts_home = df_all_match_data['home_formation'].value_counts()
    formation_counts_away = df_all_match_data['away_formation'].value_counts()

    # Combine and sum the counts for each unique formation
    all_formations_counts = formation_counts_home.add(formation_counts_away, fill_value=0)

    # Create a list of tuples containing formation and its count
    df_unique_formations_with_counts = pd.DataFrame(list(all_formations_counts.items()), columns=['Unique_Formation', 'Count'])

    # violinplot data is not implemented yet
    #first output is for heatmap, second for timeline, third for violinplot, fourth for radarplot
    return df_wins_losses, wl_data_df_sorted, df_extra_shot_data, df_extra_info, df_unique_formations_with_counts
