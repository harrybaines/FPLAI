from flask import Blueprint, render_template, request
from random import randint
import app.fpl.predictor as fpl

home = Blueprint('home', __name__)


@home.route('/home')
@home.route('/', methods=['GET', 'POST'])
def homepage():
    elements_df = fpl.get_player_data()
    elements_df_sorted = elements_df.sort_values('value', ascending=False).reset_index(drop=True)
    team = fpl.predict_best_value_team(elements_df_sorted)
    team_cost = 0
    for i, gk_row_idx in enumerate(team['Goalkeeper']): # NOTE: return Player objects instead of row ID's
        player = elements_df_sorted.iloc[gk_row_idx]
        team['Goalkeeper'][i] = player
        team_cost += player['now_cost']
    for i, df_row_idx in enumerate(team['Defender']): # NOTE: return Player objects instead of row ID's
        player = elements_df_sorted.iloc[df_row_idx]
        team['Defender'][i] = player
        team_cost += player['now_cost']
    for i, md_row_idx in enumerate(team['Midfielder']): # NOTE: return Player objects instead of row ID's
        player = elements_df_sorted.iloc[md_row_idx]
        team['Midfielder'][i] = player
        team_cost += player['now_cost']
    for i, fd_row_idx in enumerate(team['Forward']): # NOTE: return Player objects instead of row ID's
        player = elements_df_sorted.iloc[fd_row_idx]
        team['Forward'][i] = player
        team_cost += player['now_cost']
    return render_template('home.html', title='Home', team=team, team_cost=team_cost)


@home.route('/about')
def about():
    return render_template('about.html', title='About')
