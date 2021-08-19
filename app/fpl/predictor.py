import pandas as pd
import requests

FPL_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

class Player:
    def __init__(self, player_code):
        self.player_code = player_code
    
    @property
    def total_points(self):
        pass
    
    @property
    def cost(self):
        pass
    
    @property
    def team(self):
        pass

    def __str__(self):
        pass

def get_player_data():
    req = requests.get(FPL_URL)
    res_json = req.json()
    # res_json.keys()

    elements_df = pd.DataFrame(res_json["elements"])
    elements_types_df = pd.DataFrame(res_json["element_types"])
    teams_df = pd.DataFrame(res_json["teams"])

    # elements_df.columns

    slim_elements_df = elements_df[[
        'second_name','team','code','element_type','selected_by_percent','now_cost','minutes','transfers_in','value_season','total_points','photo'
    ]]
    slim_elements_df.rename(columns={'code':'player_code'}, inplace=True)
    slim_elements_df['position'] = slim_elements_df.element_type.map(elements_types_df.set_index('id').singular_name)
    slim_elements_df['team'] = slim_elements_df.team.map(teams_df.set_index('id').name)
    slim_elements_df['value'] = slim_elements_df.value_season.astype(float)
    slim_elements_df.now_cost = slim_elements_df.now_cost / 10
    slim_elements_df = slim_elements_df.drop(columns=['value_season', 'minutes', 'transfers_in', 'element_type', 'selected_by_percent'])
    slim_elements_df = slim_elements_df.sort_values('value', ascending=False)
    return slim_elements_df

def get_players_from_team(df, team_name):
    return df.loc[df.team == team_name]

def get_player(df, player_code):
    return df.loc[df.player_code == player_code]

def get_player_picture(df, player_code):
    player = get_player(df, player_code)
    photo_id = player.photo.item().replace('.jpg', '') # Move to top
    res = requests.get(f'https://resources.premierleague.com/premierleague/photos/players/110x140/p{photo_id}.png')
    return res.content

def predict_best_value_team(df):
    positions = {
        'Goalkeeper': [],
        'Defender': [],
        'Midfielder': [],
        'Forward': []
    }
    position_counts = {
        'Goalkeeper': 2,
        'Defender': 5,
        'Midfielder': 5,
        'Forward': 3
    }
    total_cost = 100
    team_count = 0
    for row_idx, row in df.iterrows():
        position = row['position']
        new_cost = total_cost - row['now_cost']
        if new_cost < 0:
            continue
        if len(positions[position]) < position_counts[position] and total_cost > 0:
            positions[position].append(row_idx)
            total_cost -= row['now_cost']
            team_count += 1
        if team_count == 15:
            break
    return positions