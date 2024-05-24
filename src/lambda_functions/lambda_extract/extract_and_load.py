import requests
import json
import os
import sys

utils_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../utilities'))
if utils_dir not in sys.path:
    sys.path.append(utils_dir)

from db_helpers import create_table_if_not_exists, truncate_table, drop_table, store_data_in_rds, run_query
    
def fetch_data(URL):    
    # Fetch content from the URL
    response = requests.get(URL)

    if response.status_code == 200:
        return  response.json()  # Assuming the content is JSON
    else:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Failed to fetch content from {URL}. Status code: {response.status_code}")
        }
    
def get_fixtures_data():

    URL = 'https://fantasy.premierleague.com/api/fixtures/'
    
    # Fetch content from the URL
    response = requests.get(URL)

    if response.status_code == 200:
        content = response.json()  # Assuming the content is JSON
    else:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Failed to fetch content from {URL}. Status code: {response.status_code}")
        }
        
    fixtures_data = []
    for i in range(len(content)):
        code = content[i]['code']
        event = content[i]['event']
        finished = content[i]['finished']
        finished_provisional = content[i]['finished_provisional']
        id = content[i]['id']
        kickoff_time = content[i]['kickoff_time']
        minutes = content[i]['minutes']
        provisional_start_time = content[i]['provisional_start_time']
        started = content[i]['started']
        team_a = content[i]['team_a']
        team_a_score = content[i]['team_a_score']
        team_h = content[i]['team_h']
        team_h_score = content[i]['team_h_score']
        team_h_difficulty = content[i]['team_h_difficulty']
        team_a_difficulty = content[i]['team_a_difficulty']
        pulse_id = content[i]['pulse_id']

        # Clean-up boolean data
        finished = str(finished)
        finished_provisional = str(finished_provisional)
        kickoff_time = str(kickoff_time)
        provisional_start_time = str(provisional_start_time)
        started = str(started)

        fixture_data =  {
            "code": code,
            "event": event,
            "finished": finished,
            "finished_provisional": finished_provisional,
            "id": id,
            "kickoff_time": kickoff_time,
            "minutes": minutes,
            "provisional_start_time": provisional_start_time,
            "started": started,
            "team_a": team_a,
            "team_a_score": team_a_score,
            "team_h": team_h,
            "team_h_score": team_h_score,
            "team_h_difficulty": team_h_difficulty,
            "team_a_difficulty": team_a_difficulty,
            "pulse_id": pulse_id
        }
                
        # Append the data
        fixtures_data.append(fixture_data)
    
    return fixtures_data

def get_teams_data():

    URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    
    # Fetch content from the URL
    response = requests.get(URL)

    if response.status_code == 200:
        content = response.json()  # Assuming the content is JSON
    else:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Failed to fetch content from {URL}. Status code: {response.status_code}")
        }
    
    teams = content['teams']

    teams_data = []
    for i in range(len(teams)):
        code = teams[i]['code']
        draw = teams[i]['draw']
        form = teams[i]['form']
        id = teams[i]['id']
        loss = teams[i]['loss']
        name = teams[i]['name']
        played = teams[i]['played']
        points = teams[i]['points']
        position = teams[i]['position']
        short_name = teams[i]['short_name']
        strength = teams[i]['strength']
        team_division = teams[i]['team_division']
        unavailable = teams[i]['unavailable']
        win = teams[i]['win']
        strength_overall_away = teams[i]['strength_overall_away']
        strength_attack_home =  teams[i]['strength_attack_home']
        strength_overall_home = teams[i]['strength_overall_home']
        strength_attack_away = teams[i]['strength_attack_away']
        strength_defence_home = teams[i]['strength_defence_home']
        strength_defence_away = teams[i]['strength_defence_away']
        pulse_id = teams[i]['pulse_id']

        team_data =  {
            "code": code,
            "draw": draw,
            "form": form,
            "id": id,
            "loss": loss,
            "name": name,
            "played": played,
            "points": points,
            "position": position,
            "short_name": short_name,
            "strength": strength,
            "team_division": team_division,
            "unavailable": unavailable,
            "win": win,
            "strength_overall_away": strength_overall_away,
            "strength_attack_home": strength_attack_home,
            "strength_overall_home": strength_overall_home,
            "strength_attack_away": strength_attack_away,
            "strength_defence_home": strength_defence_home,
            "strength_defence_away": strength_defence_away,
            "pulse_id": pulse_id
        }
                
        # Append the data
        teams_data.append(team_data)
    return teams_data

def get_players_data():

    URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    
    # Fetch content from the URL
    response = requests.get(URL)

    if response.status_code == 200:
        content = response.json()  # Assuming the content is JSON
    else:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Failed to fetch content from {URL}. Status code: {response.status_code}")
        }
        
    players = content['elements']

    players_data = []
    for i in range(len(players)):
        chance_of_playing_next_round = players[i]['chance_of_playing_next_round']
        chance_of_playing_this_round = players[i]['chance_of_playing_this_round']
        code = players[i]['code']
        cost_change_event = players[i]['cost_change_event']
        cost_change_event_fall = players[i]['cost_change_event_fall']
        cost_change_start = players[i]['cost_change_start']
        cost_change_start_fall = players[i]['cost_change_start_fall']
        dreamteam_count = players[i]['dreamteam_count']
        element_type = players[i]['element_type']
        ep_next = players[i]['ep_next']
        ep_this = players[i]['ep_this']
        event_points = players[i]['event_points']
        first_name = players[i]['first_name']
        form = players[i]['form']
        id = players[i]['id']
        in_dreamteam = players[i]['in_dreamteam']
        news = players[i]['news']
        news_added = players[i]['news_added']
        now_cost = players[i]['now_cost']
        photo = players[i]['photo']
        points_per_game = players[i]['points_per_game']
        second_name = players[i]['second_name']
        selected_by_percent = players[i]['selected_by_percent']
        special = players[i]['special']
        squad_number = players[i]['squad_number']
        status = players[i]['status']
        team = players[i]['team']
        team_code = players[i]['team_code']
        total_points = players[i]['total_points']
        transfers_in = players[i]['transfers_in']
        transfers_in_event = players[i]['transfers_in_event']
        transfers_out = players[i]['transfers_out']
        transfers_out_event = players[i]['transfers_out_event']
        value_form = players[i]['value_form']
        value_season = players[i]['value_season']
        web_name = players[i]['web_name']
        minutes = players[i]['minutes']
        goals_scored = players[i]['goals_scored']
        assists = players[i]['assists']
        clean_sheets = players[i]['clean_sheets']
        goals_conceded = players[i]['goals_conceded']
        own_goals = players[i]['own_goals']
        penalties_saved = players[i]['penalties_saved']
        penalties_missed = players[i]['penalties_missed']
        yellow_cards = players[i]['yellow_cards']
        red_cards = players[i]['red_cards']
        saves = players[i]['saves']
        bonus = players[i]['bonus']
        bps = players[i]['bps']
        influence = players[i]['influence']
        creativity = players[i]['creativity']
        threat = players[i]['threat']
        ict_index = players[i]['ict_index']
        starts = players[i]['starts']
        expected_goals = players[i]['expected_goals']
        expected_assists = players[i]['expected_assists']
        expected_goal_involvements = players[i]['expected_goal_involvements']
        expected_goals_conceded = players[i]['expected_goals_conceded']
        influence_rank = players[i]['influence_rank']
        influence_rank_type = players[i]['influence_rank_type']
        creativity_rank = players[i]['creativity_rank']
        creativity_rank_type = players[i]['creativity_rank_type']
        threat_rank = players[i]['threat_rank']
        threat_rank_type = players[i]['threat_rank_type']
        ict_index_rank = players[i]['ict_index_rank']
        ict_index_rank_type = players[i]['ict_index_rank_type']
        corners_and_indirect_freekicks_order = players[i]['corners_and_indirect_freekicks_order']
        corners_and_indirect_freekicks_text = players[i]['corners_and_indirect_freekicks_text']
        direct_freekicks_order = players[i]['direct_freekicks_order']
        direct_freekicks_text = players[i]['direct_freekicks_text']
        penalties_order = players[i]['penalties_order']
        penalties_text = players[i]['penalties_text']
        expected_goals_per_90 = players[i]['expected_goals_per_90']
        saves_per_90 = players[i]['saves_per_90']
        expected_assists_per_90 = players[i]['expected_assists_per_90']
        expected_goal_involvements_per_90 = players[i]['expected_goal_involvements_per_90']
        expected_goals_conceded_per_90 = players[i]['expected_goals_conceded_per_90']
        goals_conceded_per_90 = players[i]['goals_conceded_per_90']
        now_cost_rank = players[i]['now_cost_rank']
        now_cost_rank_type = players[i]['now_cost_rank_type']
        form_rank = players[i]['form_rank']
        form_rank_type = players[i]['form_rank_type']
        points_per_game_rank = players[i]['points_per_game_rank']
        points_per_game_rank_type = players[i]['points_per_game_rank_type']
        selected_rank = players[i]['selected_rank']
        selected_rank_type = players[i]['selected_rank_type']
        starts_per_90 = players[i]['starts_per_90']
        clean_sheets_per_90 = players[i]['clean_sheets_per_90']

        # Clean-up data
        in_dreamteam= str(in_dreamteam)
        special = str(special)
        influence = float(influence)
        creativity = float(creativity)
        threat = float(threat)
        ict_index = float(ict_index)
        expected_goals = float(expected_goals)
        expected_assists = float(expected_assists)
        expected_goal_involvements = float(expected_goal_involvements)
        expected_goals_conceded = float(expected_goals_conceded)

        player_data = {
            "chance_of_playing_next_round": chance_of_playing_next_round,
            "chance_of_playing_this_round": chance_of_playing_this_round,
            "code": code,
            "cost_change_event": cost_change_event,
            "cost_change_event_fall": cost_change_event_fall,
            "cost_change_start": cost_change_start,
            "cost_change_start_fall": cost_change_start_fall,
            "dreamteam_count": dreamteam_count,
            "element_type": element_type,
            "ep_next": ep_next,
            "ep_this": ep_this,
            "event_points": event_points,
            "first_name": first_name,
            "form": form,
            "id": id,
            "in_dreamteam": in_dreamteam,
            "news": news,
            "news_added": news_added,
            "now_cost": now_cost,
            "photo": photo,
            "points_per_game": points_per_game,
            "second_name": second_name,
            "selected_by_percent": selected_by_percent,
            "special": special,
            "squad_number": squad_number,
            "status": status,
            "team": team,
            "team_code": team_code,
            "total_points": total_points,
            "transfers_in": transfers_in,
            "transfers_in_event": transfers_in_event,
            "transfers_out": transfers_out,
            "transfers_out_event": transfers_out_event,
            "value_form": value_form,
            "value_season": value_season,
            "web_name": web_name,
            "minutes": minutes,
            "goals_scored": goals_scored,
            "assists": assists,
            "clean_sheets": clean_sheets,
            "goals_conceded": goals_conceded,
            "own_goals": own_goals,
            "penalties_saved": penalties_saved,
            "penalties_missed": penalties_missed,
            "yellow_cards": yellow_cards,
            "red_cards": red_cards,
            "saves": saves,
            "bonus": bonus,
            "bps": bps,
            "influence": influence,
            "creativity": creativity,
            "threat": threat,
            "ict_index": ict_index,
            "starts": starts,
            "expected_goals": expected_goals,
            "expected_assists": expected_assists,
            "expected_goal_involvements": expected_goal_involvements,
            "expected_goals_conceded": expected_goals_conceded,
            "influence_rank": influence_rank,
            "influence_rank_type": influence_rank_type,
            "creativity_rank": creativity_rank,
            "creativity_rank_type": creativity_rank_type,
            "threat_rank": threat_rank,
            "threat_rank_type": threat_rank_type,
            "ict_index_rank": ict_index_rank,
            "ict_index_rank_type": ict_index_rank_type,
            "corners_and_indirect_freekicks_order": corners_and_indirect_freekicks_order,
            "corners_and_indirect_freekicks_text": corners_and_indirect_freekicks_text,
            "direct_freekicks_order": direct_freekicks_order,
            "direct_freekicks_text": direct_freekicks_text,
            "penalties_order": penalties_order,
            "penalties_text": penalties_text,
            "expected_goals_per_90": expected_goals_per_90,
            "saves_per_90": saves_per_90,
            "expected_assists_per_90": expected_assists_per_90,
            "expected_goal_involvements_per_90": expected_goal_involvements_per_90,
            "expected_goals_conceded_per_90": expected_goals_conceded_per_90,
            "goals_conceded_per_90": goals_conceded_per_90,
            "now_cost_rank": now_cost_rank,
            "now_cost_rank_type": now_cost_rank_type,
            "form_rank": form_rank,
            "form_rank_type": form_rank_type,
            "points_per_game_rank": points_per_game_rank,
            "points_per_game_rank_type": points_per_game_rank_type,
            "selected_rank": selected_rank,
            "selected_rank_type": selected_rank_type,
            "starts_per_90": starts_per_90,
            "clean_sheets_per_90": clean_sheets_per_90
        }

        # Append the data
        players_data.append(player_data)
    return players_data

def get_players_historical_data():

    URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    
    # Fetch content from the URL
    response = requests.get(URL)

    if response.status_code == 200:
        content = response.json()  # Assuming the content is JSON
    else:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Failed to fetch content from {URL}. Status code: {response.status_code}")
        }
        
    number_of_players = len(content['elements'])

    URL_BASE = 'https://fantasy.premierleague.com/api/element-summary/'

    players_historical_data = []
    
    for i in range(number_of_players):
        print(f'player {i}')
        URL_PLAYER = URL_BASE + str(i)

        # Fetch content from the URL
        response = requests.get(URL_PLAYER)
        if response.status_code == 200:
            content = response.json()

            try:
                history = content['history']
                number_of_history_records = len(history)
                for j in range(number_of_history_records):
                    element = history[j]["element"]
                    fixture = history[j]["fixture"]
                    opponent_team = history[j]["opponent_team"]
                    total_points = history[j]["total_points"]
                    was_home = history[j]["was_home"]
                    kickoff_time = history[j]["kickoff_time"]
                    team_h_score = history[j]["team_h_score"]
                    team_a_score = history[j]["team_a_score"]
                    round = history[j]["round"]
                    minutes = history[j]["minutes"]
                    goals_scored = history[j]["goals_scored"]
                    assists = history[j]["assists"]
                    clean_sheets = history[j]["clean_sheets"]
                    goals_conceded = history[j]["goals_conceded"]
                    own_goals = history[j]["own_goals"]
                    penalties_saved = history[j]["penalties_saved"]
                    penalties_missed = history[j]["penalties_missed"]
                    yellow_cards = history[j]["yellow_cards"]
                    red_cards = history[j]["red_cards"]
                    saves = history[j]["saves"]
                    bonus = history[j]["bonus"]
                    bps = history[j]["bps"]
                    influence = history[j]["influence"]
                    creativity = history[j]["creativity"]
                    threat = history[j]["threat"]
                    ict_index = history[j]["ict_index"]
                    starts = history[j]["starts"]
                    expected_goals = history[j]["expected_goals"]
                    expected_assists = history[j]["expected_assists"]
                    expected_goal_involvements = history[j]["expected_goal_involvements"]
                    expected_goals_conceded = history[j]["expected_goals_conceded"]
                    value = history[j]["value"]
                    transfers_balance = history[j]["transfers_balance"]
                    selected = history[j]["selected"]
                    transfers_in = history[j]["transfers_in"]
                    transfers_out = history[j]["transfers_out"]

                    # Clean data
                    was_home = str(was_home)
                    influence = float(influence)
                    creativity = float(creativity)
                    threat = float(threat)
                    ict_index = float(ict_index)
                    expected_goals = float(expected_goals)
                    expected_assists = float(expected_assists)
                    expected_goal_involvements = float(expected_goal_involvements)
                    expected_goals_conceded = float(expected_goals_conceded)

                    player_historical_data =  {
                        "element": element,
                        "fixture": fixture,
                        "opponent_team": opponent_team,
                        "total_points": total_points,
                        "was_home": was_home,
                        "kickoff_time": kickoff_time,
                        "team_h_score": team_h_score,
                        "team_a_score": team_a_score,
                        "round": round,
                        "minutes": minutes,
                        "goals_scored": goals_scored,
                        "assists": assists,
                        "clean_sheets": clean_sheets,
                        "goals_conceded": goals_conceded,
                        "own_goals": own_goals,
                        "penalties_saved": penalties_saved,
                        "penalties_missed": penalties_missed,
                        "yellow_cards": yellow_cards,
                        "red_cards": red_cards,
                        "saves": saves,
                        "bonus": bonus,
                        "bps": bps,
                        "influence": influence,
                        "creativity": creativity,
                        "threat": threat,
                        "ict_index": ict_index,
                        "starts": starts,
                        "expected_goals": expected_goals,
                        "expected_assists": expected_assists,
                        "expected_goal_involvements": expected_goal_involvements,
                        "expected_goals_conceded": expected_goals_conceded,
                        "value": value,
                        "transfers_balance": transfers_balance,
                        "selected": selected,
                        "transfers_in": transfers_in,
                        "transfers_out": transfers_out
                    }
                            
                    # Append the data
                    players_historical_data.append(player_historical_data)
            except:
                print(f'No historical records for player {i}')

    return players_historical_data

def get_element_type_data():

    URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    
    # Fetch content from the URL
    response = requests.get(URL)

    if response.status_code == 200:
        content = response.json()  # Assuming the content is JSON
    else:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Failed to fetch content from {URL}. Status code: {response.status_code}")
        }
    
    elements = content['element_types']

    elements_data = []
    for i in range(len(elements)):
        id = elements[i]['id']
        plural_name = elements[i]['plural_name']
        plural_name_short = elements[i]['plural_name_short']
        singular_name = elements[i]['singular_name']
        singular_name_short = elements[i]['singular_name_short']
        squad_select = elements[i]['squad_select']
        squad_min_play = elements[i]['squad_min_play']
        squad_max_play = elements[i]['squad_max_play']
        ui_shirt_specific = elements[i]['ui_shirt_specific']
        element_count = elements[i]['element_count']

        # Clean data
        ui_shirt_specific = str(ui_shirt_specific)

        element_data =  {
            'id': id,
            'plural_name': plural_name,
            'plural_name_short': plural_name_short,
            'singular_name': singular_name,
            'singular_name_short': singular_name_short,
            'squad_select': squad_select,
            'squad_min_play': squad_min_play,
            'squad_max_play': squad_max_play,
            'ui_shirt_specific': ui_shirt_specific,
            'element_count': element_count
        }
                
        # Append the data
        elements_data.append(element_data)

    return elements_data

def update_element_types():
    """
    Update element_types data.
    """

    TABLE_NAME = 'raw_element_types'
    CREATE_TABLE_QUERY = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER,
        plural_name VARCHAR(50),
        plural_name_short VARCHAR(10),
        singular_name VARCHAR(50),
        singular_name_short VARCHAR(10),
        squad_select INTEGER,
        squad_min_play INTEGER,
        squad_max_play INTEGER,
        ui_shirt_specific VARCHAR(10),
        element_count INTEGER
    );
    '''

    INSERT_QUERY = f'''
    INSERT INTO 
        {TABLE_NAME} (
            id,
            plural_name,
            plural_name_short,
            singular_name,
            singular_name_short,
            squad_select,
            squad_min_play,
            squad_max_play,
            ui_shirt_specific,
            element_count
            )
    VALUES (
            :id,
            :plural_name,
            :plural_name_short,
            :singular_name,
            :singular_name_short,
            :squad_select,
            :squad_min_play,
            :squad_max_play,
            :ui_shirt_specific,
            :element_count
            )'''

    drop_table(TABLE_NAME)
    create_table_if_not_exists(CREATE_TABLE_QUERY)
    
    elements_data = get_element_type_data()
    truncate_table(TABLE_NAME)

    store_data_in_rds(INSERT_QUERY, elements_data)

def update_fixtures():
    """
    Update fixtures data.
    """

    TABLE_NAME = 'raw_fixtures'
    CREATE_TABLE_QUERY = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        code INTEGER,
        event INTEGER,
        finished VARCHAR(10),
        finished_provisional VARCHAR(10),
        id INTEGER,
        kickoff_time VARCHAR(50),
        minutes INTEGER,
        provisional_start_time VARCHAR(50),
        started VARCHAR(10),
        team_a INTEGER,
        team_a_score INTEGER,
        team_h INTEGER,
        team_h_score INTEGER,
        team_h_difficulty INTEGER,
        team_a_difficulty INTEGER,
        pulse_id INTEGER
    );
    '''

    INSERT_QUERY = f'''
    INSERT INTO 
        {TABLE_NAME} (
            code,
            event,
            finished,
            finished_provisional,
            id,
            kickoff_time,
            minutes,
            provisional_start_time,
            started,
            team_a,
            team_a_score,
            team_h,
            team_h_score,
            team_h_difficulty,
            team_a_difficulty,
            pulse_id
            )
    VALUES (
            :code,
            :event,
            :finished,
            :finished_provisional,
            :id,
            :kickoff_time,
            :minutes,
            :provisional_start_time,
            :started,
            :team_a,
            :team_a_score,
            :team_h,
            :team_h_score,
            :team_h_difficulty,
            :team_a_difficulty,
            :pulse_id
            )'''

    drop_table(TABLE_NAME)
    create_table_if_not_exists(CREATE_TABLE_QUERY)
    
    fixtures_data = get_fixtures_data()
    # fixtures_data = dummy_fixture_data()
    truncate_table(TABLE_NAME)

    store_data_in_rds(INSERT_QUERY, fixtures_data)


def update_teams():
    """
    Update teams data.
    """

    TABLE_NAME = 'raw_teams'
    CREATE_TABLE_QUERY = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        code INTEGER,
        draw INTEGER,
        form INTEGER,
        id INTEGER,
        loss INTEGER,
        name VARCHAR(20),
        played INTEGER,
        points INTEGER,
        position INTEGER,
        short_name VARCHAR(20),
        strength INTEGER,
        team_division INTEGER,
        unavailable VARCHAR(10),
        win INTEGER,
        strength_overall_away INTEGER,
        strength_attack_home INTEGER,
        strength_overall_home INTEGER,
        strength_attack_away INTEGER,
        strength_defence_home INTEGER,
        strength_defence_away INTEGER,
        pulse_id INTEGER
    );
    '''

    INSERT_QUERY = f'''
    INSERT INTO 
        {TABLE_NAME} (
        code,
        draw,
        form,
        id,
        loss,
        name,
        played,
        points,
        position,
        short_name,
        strength,
        team_division,
        unavailable,
        win,
        strength_overall_away,
        strength_attack_home,
        strength_overall_home,
        strength_attack_away,
        strength_defence_home,
        strength_defence_away,
        pulse_id
        )
    VALUES (
        :code,
        :draw,
        :form,
        :id,
        :loss,
        :name,
        :played,
        :points,
        :position,
        :short_name,
        :strength,
        :team_division,
        :unavailable,
        :win,
        :strength_overall_away,
        :strength_attack_home,
        :strength_overall_home,
        :strength_attack_away,
        :strength_defence_home,
        :strength_defence_away,
        :pulse_id
        )'''

    drop_table(TABLE_NAME)
    create_table_if_not_exists(CREATE_TABLE_QUERY)
    
    teams_data = get_teams_data()
    truncate_table(TABLE_NAME)

    store_data_in_rds(INSERT_QUERY, teams_data)

def update_player_data():
    """
    Update player data.
    """

    TABLE_NAME = 'raw_player_static'
    CREATE_TABLE_QUERY = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        chance_of_playing_next_round INTEGER,
        chance_of_playing_this_round INTEGER,
        code INTEGER,
        cost_change_event INTEGER,
        cost_change_event_fall INTEGER,
        cost_change_start INTEGER,
        cost_change_start_fall INTEGER,
        dreamteam_count INTEGER,
        element_type INTEGER,
        ep_next VARCHAR(10),
        ep_this VARCHAR(10),
        event_points INTEGER,
        first_name VARCHAR(50),
        form VARCHAR(10),
        id INTEGER,
        in_dreamteam VARCHAR(10),
        news VARCHAR(500),
        news_added VARCHAR(50),
        now_cost INTEGER,
        photo VARCHAR(20),
        points_per_game VARCHAR(10),
        second_name VARCHAR(50),
        selected_by_percent VARCHAR(10),
        special VARCHAR(10),
        squad_number INTEGER,
        status VARCHAR(10),
        team INTEGER,
        team_code INTEGER,
        total_points INTEGER,
        transfers_in INTEGER,
        transfers_in_event INTEGER,
        transfers_out INTEGER,
        transfers_out_event INTEGER,
        value_form VARCHAR(10),
        value_season VARCHAR(10),
        web_name VARCHAR(50),
        minutes INTEGER,
        goals_scored INTEGER,
        assists INTEGER,
        clean_sheets INTEGER,
        goals_conceded INTEGER,
        own_goals INTEGER,
        penalties_saved INTEGER,
        penalties_missed INTEGER,
        yellow_cards INTEGER,
        red_cards INTEGER,
        saves INTEGER,
        bonus INTEGER,
        bps INTEGER,
        influence REAL,
        creativity REAL,
        threat REAL,
        ict_index REAL,
        starts INTEGER,
        expected_goals REAL,
        expected_assists REAL,
        expected_goal_involvements REAL,
        expected_goals_conceded REAL,
        influence_rank INTEGER,
        influence_rank_type INTEGER,
        creativity_rank INTEGER,
        creativity_rank_type INTEGER,
        threat_rank INTEGER,
        threat_rank_type INTEGER,
        ict_index_rank INTEGER,
        ict_index_rank_type INTEGER,
        corners_and_indirect_freekicks_order INTEGER,
        corners_and_indirect_freekicks_text VARCHAR(250),
        direct_freekicks_order INTEGER,
        direct_freekicks_text VARCHAR(250),
        penalties_order INTEGER,
        penalties_text VARCHAR(250),
        expected_goals_per_90 INTEGER,
        saves_per_90 INTEGER,
        expected_assists_per_90 INTEGER,
        expected_goal_involvements_per_90 INTEGER,
        expected_goals_conceded_per_90 INTEGER,
        goals_conceded_per_90 INTEGER,
        now_cost_rank INTEGER,
        now_cost_rank_type INTEGER,
        form_rank INTEGER,
        form_rank_type INTEGER,
        points_per_game_rank INTEGER,
        points_per_game_rank_type INTEGER,
        selected_rank INTEGER,
        selected_rank_type INTEGER,
        starts_per_90 INTEGER,
        clean_sheets_per_90 INTEGER
    );
    '''

    INSERT_QUERY = f'''
    INSERT INTO 
        {TABLE_NAME} (
        chance_of_playing_next_round,
        chance_of_playing_this_round,
        code,
        cost_change_event,
        cost_change_event_fall,
        cost_change_start,
        cost_change_start_fall,
        dreamteam_count,
        element_type,
        ep_next,
        ep_this,
        event_points,
        first_name,
        form,
        id,
        in_dreamteam,
        news,
        news_added,
        now_cost,
        photo,
        points_per_game,
        second_name,
        selected_by_percent,
        special,
        squad_number,
        status,
        team,
        team_code,
        total_points,
        transfers_in,
        transfers_in_event,
        transfers_out,
        transfers_out_event,
        value_form,
        value_season,
        web_name,
        minutes,
        goals_scored,
        assists,
        clean_sheets,
        goals_conceded,
        own_goals,
        penalties_saved,
        penalties_missed,
        yellow_cards,
        red_cards,
        saves,
        bonus,
        bps,
        influence,
        creativity,
        threat,
        ict_index,
        starts,
        expected_goals,
        expected_assists,
        expected_goal_involvements,
        expected_goals_conceded,
        influence_rank,
        influence_rank_type,
        creativity_rank,
        creativity_rank_type,
        threat_rank,
        threat_rank_type,
        ict_index_rank,
        ict_index_rank_type,
        corners_and_indirect_freekicks_order,
        corners_and_indirect_freekicks_text,
        direct_freekicks_order,
        direct_freekicks_text,
        penalties_order,
        penalties_text,
        expected_goals_per_90,
        saves_per_90,
        expected_assists_per_90,
        expected_goal_involvements_per_90,
        expected_goals_conceded_per_90,
        goals_conceded_per_90,
        now_cost_rank,
        now_cost_rank_type,
        form_rank,
        form_rank_type,
        points_per_game_rank,
        points_per_game_rank_type,
        selected_rank,
        selected_rank_type,
        starts_per_90,
        clean_sheets_per_90
        )
    VALUES (
        :chance_of_playing_next_round,
        :chance_of_playing_this_round,
        :code,
        :cost_change_event,
        :cost_change_event_fall,
        :cost_change_start,
        :cost_change_start_fall,
        :dreamteam_count,
        :element_type,
        :ep_next,
        :ep_this,
        :event_points,
        :first_name,
        :form,
        :id,
        :in_dreamteam,
        :news,
        :news_added,
        :now_cost,
        :photo,
        :points_per_game,
        :second_name,
        :selected_by_percent,
        :special,
        :squad_number,
        :status,
        :team,
        :team_code,
        :total_points,
        :transfers_in,
        :transfers_in_event,
        :transfers_out,
        :transfers_out_event,
        :value_form,
        :value_season,
        :web_name,
        :minutes,
        :goals_scored,
        :assists,
        :clean_sheets,
        :goals_conceded,
        :own_goals,
        :penalties_saved,
        :penalties_missed,
        :yellow_cards,
        :red_cards,
        :saves,
        :bonus,
        :bps,
        :influence,
        :creativity,
        :threat,
        :ict_index,
        :starts,
        :expected_goals,
        :expected_assists,
        :expected_goal_involvements,
        :expected_goals_conceded,
        :influence_rank,
        :influence_rank_type,
        :creativity_rank,
        :creativity_rank_type,
        :threat_rank,
        :threat_rank_type,
        :ict_index_rank,
        :ict_index_rank_type,
        :corners_and_indirect_freekicks_order,
        :corners_and_indirect_freekicks_text,
        :direct_freekicks_order,
        :direct_freekicks_text,
        :penalties_order,
        :penalties_text,
        :expected_goals_per_90,
        :saves_per_90,
        :expected_assists_per_90,
        :expected_goal_involvements_per_90,
        :expected_goals_conceded_per_90,
        :goals_conceded_per_90,
        :now_cost_rank,
        :now_cost_rank_type,
        :form_rank,
        :form_rank_type,
        :points_per_game_rank,
        :points_per_game_rank_type,
        :selected_rank,
        :selected_rank_type,
        :starts_per_90,
        :clean_sheets_per_90
        )'''

    drop_table(TABLE_NAME)
    create_table_if_not_exists(CREATE_TABLE_QUERY)
    
    players_data = get_players_data()
    truncate_table(TABLE_NAME)

    store_data_in_rds(INSERT_QUERY, players_data)


def update_player_historical_data():
    """
    Update player historical data.
    """

    TABLE_NAME = 'raw_player_history'
    CREATE_TABLE_QUERY = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        element INTEGER,
        fixture INTEGER,
        opponent_team INTEGER,
        total_points INTEGER,
        was_home VARCHAR(10),
        kickoff_time VARCHAR(50),
        team_h_score INTEGER,
        team_a_score INTEGER,
        round INTEGER,
        minutes INTEGER,
        goals_scored INTEGER,
        assists INTEGER,
        clean_sheets INTEGER,
        goals_conceded INTEGER,
        own_goals INTEGER,
        penalties_saved INTEGER,
        penalties_missed INTEGER,
        yellow_cards INTEGER,
        red_cards INTEGER,
        saves INTEGER,
        bonus INTEGER,
        bps INTEGER,
        influence REAL,
        creativity REAL,
        threat REAL,
        ict_index REAL,
        starts INTEGER,
        expected_goals REAL,
        expected_assists REAL,
        expected_goal_involvements REAL,
        expected_goals_conceded REAL,
        value INTEGER,
        transfers_balance INTEGER,
        selected INTEGER,
        transfers_in INTEGER,
        transfers_out INTEGER
    );
    '''

    INSERT_QUERY = f'''
    INSERT INTO 
        {TABLE_NAME} (
            element,
            fixture,
            opponent_team,
            total_points,
            was_home,
            kickoff_time,
            team_h_score,
            team_a_score,
            round,
            minutes,
            goals_scored,
            assists,
            clean_sheets,
            goals_conceded,
            own_goals,
            penalties_saved,
            penalties_missed,
            yellow_cards,
            red_cards,
            saves,
            bonus,
            bps,
            influence,
            creativity,
            threat,
            ict_index,
            starts,
            expected_goals,
            expected_assists,
            expected_goal_involvements,
            expected_goals_conceded,
            value,
            transfers_balance,
            selected,
            transfers_in,
            transfers_out
            )
    VALUES (
            :element,
            :fixture,
            :opponent_team,
            :total_points,
            :was_home,
            :kickoff_time,
            :team_h_score,
            :team_a_score,
            :round,
            :minutes,
            :goals_scored,
            :assists,
            :clean_sheets,
            :goals_conceded,
            :own_goals,
            :penalties_saved,
            :penalties_missed,
            :yellow_cards,
            :red_cards,
            :saves,
            :bonus,
            :bps,
            :influence,
            :creativity,
            :threat,
            :ict_index,
            :starts,
            :expected_goals,
            :expected_assists,
            :expected_goal_involvements,
            :expected_goals_conceded,
            :value,
            :transfers_balance,
            :selected,
            :transfers_in,
            :transfers_out
            )'''

    drop_table(TABLE_NAME)
    create_table_if_not_exists(CREATE_TABLE_QUERY)
    
    fixtures_data = get_players_historical_data()
    # fixtures_data = dummy_fixture_data()
    truncate_table(TABLE_NAME)

    store_data_in_rds(INSERT_QUERY, fixtures_data)

if __name__ == '__main__':
    update_fixtures()
    update_element_types()
    # update_teams()
    # update_player_data()
    # update_player_historical_data()

    # Define the raw SQL query
    # raw_sql = "SELECT * FROM player_historical_data"
    # run_query(raw_sql)