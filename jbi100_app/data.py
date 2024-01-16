import pandas as pd
import plotly.express as px

def get_data():

    # Read data
    df_match_data = pd.read_csv('jbi100_app/Data/FIFA World Cup 2022 Match Data/data.csv', delimiter=',')
    df_extra_match_data = pd.read_csv('jbi100_app/Data/Match formations.csv')
    
    df_match_data['score'] = df_match_data['score'].str.replace(r"\(.\)","")           
    df_match_data[['score_home', 'score_away']] = df_match_data.score.str.split("–", expand=True,)
    df_match_data['score_home'] = df_match_data['score_home'].str.replace(" ","")
    df_match_data['score_away'] = df_match_data['score_away'].str.replace(" ","")

    df_all_match_data = pd.concat([df_match_data, df_extra_match_data],  join="inner", ignore_index=True)

    missing_values = df_all_match_data.isnull()
    missing_counts = missing_values.sum()
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    winning_formation = []
    losing_formation = []
    for i in range(len(df_match_data)) :
        if len(df_match_data["score_home"][i]) == 1:
            if(df_match_data["score_home"][i][0] < df_match_data["score_away"][i][0]):
                winning_formation.append(df_match_data["away_formation"][i])
                losing_formation.append(df_match_data["home_formation"][i])
            elif (df_match_data["score_home"][i][0] > df_match_data["score_away"][i][0]):
                winning_formation.append(df_match_data["home_formation"][i])
                losing_formation.append(df_match_data["away_formation"][i])
            elif (df_match_data["score_home"][i][0] == df_match_data["score_away"][i][0]):
                winning_formation.append(None)
                losing_formation.append(None)
            elif (df_match_data["score_home"][i][1] > df_match_data["score_away"][i][3]):
                winning_formation.append(df_match_data["home_formation"][i])
                losing_formation.append(df_match_data["away_formation"][i])
            elif (df_match_data["score_home"][i][1] < df_match_data["score_away"][i][3]):
                winning_formation.append(df_match_data["away_formation"][i])
                losing_formation.append(df_match_data["home_formation"][i])
        else:
            winning_formation.append(None)
            losing_formation.append(None)

    for i in range(len(df_match_data), len(df_all_match_data)) :
        if(df_all_match_data["score_home"][i] < df_all_match_data["score_away"][i]):
                winning_formation.append(df_all_match_data["away_formation"][i])
                losing_formation.append(df_all_match_data["home_formation"][i])
        elif(df_all_match_data["score_home"][i] > df_all_match_data["score_away"][i]):
                winning_formation.append(df_all_match_data["home_formation"][i])
                losing_formation.append(df_all_match_data["away_formation"][i])
        else:
            winning_formation.append(None)
            losing_formation.append(None)

    df_wins_losses = pd.DataFrame({
    'winning_formation': winning_formation,
    'losing_formation': losing_formation
    })

    df = df_all_match_data

        # Drop rows with NaN values (None in the formations)
    df_wins_losses = df_wins_losses.dropna()

    # Set a threshold count for formations
    threshold_count = 50

    # Count occurrences of each formation pair
    formation_counts = df_wins_losses.groupby(['winning_formation', 'losing_formation']).size()
    
    # Filter formation pairs by the threshold count
    valid_formations = formation_counts[formation_counts >= threshold_count]

    # Get only rows with valid formations
    filtered_data = df_wins_losses[
        df_wins_losses.apply(lambda row: (row['winning_formation'], row['losing_formation']) in valid_formations.index, axis=1)
    ]

    # Count occurrences of filtered formation pairs
    filtered_counts = filtered_data.groupby(['winning_formation', 'losing_formation']).size().unstack(fill_value=0)

    # Calculate win/lose ratios
    formation_ratios = filtered_counts.div(filtered_counts.sum(axis=1), axis=0)

    return formation_ratios