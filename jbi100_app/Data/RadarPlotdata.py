import pandas as pd

# Assuming your DataFrame is named 'df'
# If not, you can read the data using pd.read_csv or pd.read_excel, depending on your data source

# Sample data

df = pd.read_csv('C:/Users/20203541/Documents/Studie/JBI100/Github int/Visualization/jbi100_app/Data/MatchExtraInfo.csv')

# Extracting the relevant columns
formation_column = df['home_formation'].unique()
goals_column = []
goals_against_column = []
possession_column = []
crosses_column = []
shot_on_column = []
shot_off_column = []
shot_on_against_column = []
shot_off_against_column = []

print(len(formation_column))

for i in range(len(formation_column)):
    goals = 0
    goals_against = 0
    possession = 0
    crosses = 0
    shot_on = 0
    shot_off = 0
    shot_on_against = 0
    shot_off_against = 0
    count = 0
    for j in range(df.shape[0]):
        if (df['home_formation'][j] == formation_column[i]):
            goals = goals+int(df['score_home'][j])
            goals_against = goals_against+int(df['score_away'][j])
            possession = possession+int(df['home_possession'][j])
            crosses = crosses+int(df['home_cross'][j])
            shot_on = shot_on+int(df["home_shot_on"][j])
            shot_off = shot_off+int(df["home_shot_off"][j])
            shot_on_against = shot_on_against+int(df["away_shot_on"][j])
            shot_off_against = shot_off_against+int(df["away_shot_off"][j] )
        elif df['away_formation'][j] == formation_column[i]:
            goals += int(df['score_away'][j])
            goals_against += int(df['score_home'][j])
            possession += int(df['away_possession'][j])
            crosses += int(df['away_cross'][j])
            shot_on += int(df["away_shot_on"][j])
            shot_off += int(df["away_shot_off"][j])
            shot_on_against += int(df["home_shot_on"][j])
            shot_off_against += int(df["home_shot_off"][j])
        count = count+1
    goals_column.append(goals / count)
    goals_against_column.append(goals_against / count)
    possession_column.append(possession / count)
    crosses_column.append(crosses / count)
    shot_on_column.append(shot_on / count)
    shot_off_column.append(shot_off / count)
    shot_on_against_column.append(shot_on_against / count)
    shot_off_against_column.append(shot_off_against / count)


# Creating a new DataFrame with the transformed columns
transformed_df = pd.DataFrame({
    'Formation': formation_column,
    'Goals': goals_column,
    'Goals Against': goals_against_column,
    'Possession': possession_column,
    'Crosses': crosses_column,
    'Shot On': shot_on_column,
    'Shot Off': shot_off_column,
    'Shot On Against': shot_on_against_column,
    'Shot Off Against': shot_off_against_column
})

# Display the transformed DataFrame
columns_to_scale = ["Goals", "Goals Against", "Possession", "Crosses", "Shot On", "Shot Off", "Shot On Against", "Shot Off Against"]

# Perform Min-Max scaling for each specified column
for column in columns_to_scale:
    min_value = transformed_df[column].min()
    max_value = transformed_df[column].max()
    transformed_df[column] = (transformed_df[column] - min_value) / (max_value - min_value)


print(transformed_df)

transformed_df.to_csv('jbi100_app/Data/RadarPlotZ.csv', sep=',', index=False, encoding='utf-8')