import pandas as pd
import numpy as np
from transform_helpers import create_lagged_sums, create_pct_of_max, create_cumulative_pct_of_max
import os
import sys

utils_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../utilities'))
if utils_dir not in sys.path:
    sys.path.append(utils_dir)

from db_helpers import connect_rds, create_table_if_not_exists, truncate_table, drop_table, run_query, create_table_from_df, inspect_tables, save_table_to_csv
    
def create_player_static_data():
    '''
    Create player static data.
    '''

    TABLE_NAME ='transformed_player_static'
    CREATE_TABLE_QUERY = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME}
    AS SELECT   a.id, 
                a.first_name || ' ' || a.second_name as player_name, 
                b.name, 
                c.singular_name as position,
                a.element_type, 
                a.now_cost as value, 
                a.selected_by_percent as selected_nr, 
                a.transfers_in_event as transfers_in_nr, 
                a.transfers_out_event as transfers_out_nr, 
                (a.transfers_in_event - a.transfers_out_event) as transfers_balance_nr, 
                a.ict_index as ict_index_nr, 
                a.ep_next, 
                a.total_points, 
                a.event_points, 
                a.points_per_game 
    FROM        raw_player_static a 
    LEFT JOIN   raw_teams b 
    ON          a.team_code = b.code
    LEFT JOIN   raw_element_types c 
    ON          a.element_type = c.id
    ;
   '''

    drop_table(TABLE_NAME)
    create_table_if_not_exists(CREATE_TABLE_QUERY)

def team_data_transformations():

    engine = connect_rds()

    teams_query = 'SELECT * FROM raw_teams'

    # Load the data into a Pandas DataFrame
    df = pd.read_sql(teams_query, engine)
    team_ids = df['id'].unique()

    all_team_data = pd.DataFrame()

    print(df.head())

    for team_id in team_ids:
        fixtures_query = f'''
        SELECT      *
        FROM        raw_fixtures
        WHERE       team_a = {team_id} OR team_h = {team_id}
        '''

        # Table extract string
        team_fixtures = pd.read_sql(fixtures_query, engine)

        team_data = pd.DataFrame()

        #create team data variables
        team_data['id'] = [team_id] * team_fixtures.shape[0] 
        team_data['fixture'] = team_fixtures['id']
        team_data['gw'] = team_fixtures['event']
        team_data['opponent'] = np.where(team_fixtures['team_a'] == team_id, team_fixtures['team_h'], team_fixtures['team_a'])
         
        team_data['opponent_difficulty'] = np.where(team_fixtures['team_a'] == team_id, team_fixtures['team_a_difficulty'], team_fixtures['team_h_difficulty'])
        team_data['team_difficulty'] = np.where(team_fixtures['team_a'] == team_id, team_fixtures['team_h_difficulty'], team_fixtures['team_a_difficulty']) 
        
        team_data['home_game'] = np.where(team_fixtures['team_a'] == team_id, 0, 1)
        team_data['finished'] = team_fixtures['finished']
        
        team_data['goals_for'] = np.where(team_fixtures['team_a'] == team_id, team_fixtures['team_a_score'], team_fixtures['team_h_score'])
        team_data['goals_againt'] = np.where(team_fixtures['team_a'] == team_id, team_fixtures['team_h_score'], team_fixtures['team_a_score'])    

        team_data['goal_difference'] = team_data['goals_for'] - team_data['goals_againt']
        team_data['difficulty_difference'] = team_data['team_difficulty'] \
                                        - team_data['opponent_difficulty']                    
        team_data['team_points'] = np.where(team_data['goal_difference'] > 0, 3, (np.where(team_data['goal_difference'] == 0, 1, 0)))
        
        team_data['cum_points'] = team_data['team_points'].cumsum()
        team_data['cum_goal_difference'] = team_data['goal_difference'].cumsum()
        
        team_data['team_points_round'] = team_data['cum_points']/team_data['gw']
        team_data['goal_difference_round'] = team_data['cum_goal_difference']/team_data['gw']
        
        team_data['team_points_l3r'] = team_data.groupby('id')['team_points'].rolling(window=3, min_periods=1).sum().reset_index(drop=True) #transform(lambda x: pd.rolling_sum(x, window=3, min_periods=1))
        team_data['goal_difference_l3r'] = team_data.groupby('id')['goal_difference'].rolling(window=3, min_periods=1).sum().reset_index(drop=True) #transform(lambda x: pd.rolling_sum(x, window=3, min_periods=1))
        team_data['avg_opp_difficulty_l3r'] = team_data.groupby('id')['opponent_difficulty'].rolling(window=3, min_periods=1).mean().reset_index(drop=True) #transform(lambda x: pd.rolling_mean(x, window=3, min_periods=1))

        for i in range(1, 7):
           team_data['opp_round_' + str(i)] = team_data['opponent'].shift(-i)
           team_data['fixture_round_' + str(i)] = team_data['fixture'].shift(-i)
        
        # Stack dataframes on top of eachother
        all_team_data = pd.concat([all_team_data, team_data], ignore_index=True)
    
    # Create ranking vars
    all_team_data['table_rank'] = all_team_data.groupby('gw')['cum_points'].rank(method='dense', ascending=False)
      
    # Replace all missing values with zero
    all_team_data = all_team_data.replace([np.inf, -np.inf, np.nan], 0)

    return all_team_data

def create_transformed_team_data():
    TABLE_NAME = 'transformed_team_data'

    drop_table(TABLE_NAME)
    all_team_data = team_data_transformations()
    create_table_from_df(TABLE_NAME, all_team_data)

def create_transformed_player_history_data():
    '''
    Create transformed player data.
    '''
    # Table extract string
    TABLE_NAME = 'transformed_player_history'
    CREATE_TABLE_QUERY = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME}  
    AS SELECT       a.element, 
                    a.round, 
                    a.assists, 
                    a.bonus, 
                    a.bps, 
                    a.clean_sheets, 
                    a.creativity, 
                    a.fixture, 
                    a.goals_conceded, 
                    a.goals_scored, 
                    a.ict_index, 
                    a.influence, 
                    a.kickoff_time, 
                    a.minutes, 
                    a.opponent_team, 
                    a.own_goals, 
                    a.penalties_missed, 
                    a.penalties_saved, 
                    a.red_cards, 
                    a.saves, 
                    a.selected, 
                    a.team_a_score, 
                    a.team_h_score, 
                    a.threat, 
                    a.total_points, 
                    a.transfers_balance, 
                    a.transfers_in, 
                    a.transfers_out, 
                    a.value, 
                    CASE    WHEN UPPER(a.was_home) = 'TRUE' THEN 1
                            ELSE 0 
                    END     AS was_home, 
                    a.yellow_cards, 
                    c.id as team_id,
                    d.code as team_code,
                    b.first_name,
                    b.second_name,
                    b.web_name,
                    b.element_type as position_code,
                    d.name as team_name,
                    b1.singular_name_short as position, 
                    c.opp_round_1,
                    c.opp_round_2,
                    c.opp_round_3,
                    c.opp_round_4,
                    c.opp_round_5,
                    c.opp_round_6 
    FROM            raw_player_history a 
    LEFT JOIN       raw_player_static b 
    ON              a.element = b.id 
    LEFT JOIN       raw_element_types b1 
    ON              b.element_type = b1.id 
    LEFT JOIN       transformed_team_data c 
    ON              a.opponent_team = c.opponent 
    AND             a.fixture = c.fixture 
    LEFT JOIN       raw_teams d 
    ON              c.id = d.id
    ''' 
    drop_table(TABLE_NAME)
    create_table_if_not_exists(CREATE_TABLE_QUERY)
          
def modelling_data_transformations():

    engine = connect_rds()

    query = 'SELECT * FROM transformed_player_history'

    # Load the data into a Pandas DataFrame
    player_temp = pd.read_sql(query, engine)

    #----------------------------------------------------------------------
    # 1. Generate team level features
    #----------------------------------------------------------------------
    print("1. Generate team level features")
    # Dictionary for team data aggregation
    team_dict = {'total_points': 'sum',
                 'value': 'sum',
                 'transfers_balance': 'sum',
                 'selected': 'sum',
                 'transfers_in': 'sum',
                 'transfers_out': 'sum',
                 'ict_index': 'sum',
                 'minutes': 'sum',
                 'goals_scored': 'sum',
                 'assists': 'sum',
                 'clean_sheets': 'max',
                 'goals_conceded': 'max',
                 'own_goals': 'sum',
                 'penalties_saved': 'sum',
                 'penalties_missed': 'sum',
                 'yellow_cards': 'sum',
                 'red_cards': 'sum',
                 'saves': 'sum',
                 'bonus': 'sum',
                 'bps': 'sum',
                 'influence': 'sum',
                 'creativity': 'sum',
                 'threat': 'sum',
                 'was_home': 'max'}
    
    # Assuming player_temp and team_dict are defined elsewhere
    team_data = player_temp.groupby(['team_name', 'team_id', 'round']).agg(team_dict).reset_index()
    team_data['goal_difference'] = team_data['goals_scored'] - team_data['goals_conceded']

    # Create lagged sum features
    team_vars_list_1 = team_data.columns.difference(['team_name', 'team_id', 'round'], sort=False).to_list()
    team_data = create_lagged_sums(team_data, 'team_name', team_vars_list_1, [3, 6])

    # Create percentage of max features
    team_vars_list_2 = team_data.columns.difference(['team_name', 'team_id', 'round'], sort=False).to_list()
    team_data = create_cumulative_pct_of_max(team_data, 'team_name', team_vars_list_2)

    # Create ratio features
    new_features = []
    for col in team_vars_list_1:
        if col in team_data.columns.to_list():
            new_col_name = f'{col}_l3r_l6r_cum_pct_of_max_ratio'
            ratio_feature = team_data[f'{col}_sum_l3r_cum_pct_of_max'] / team_data[f'{col}_sum_l6r_cum_pct_of_max']
            new_features.append(pd.DataFrame(ratio_feature, columns=[new_col_name]))

    team_data = pd.concat([team_data] + new_features, axis=1)
    team_data.columns = team_data.columns + '_team'

    #----------------------------------------------------------------------
    # 2. Generate opposition level features
    #----------------------------------------------------------------------
    print("2. Generate opposition level features")
    opp_dict = {'opp_round_1': 'max',
                'opp_round_2': 'max',
                'opp_round_3': 'max',
                'opp_round_4': 'max',
                'opp_round_5': 'max',
                'opp_round_6': 'max'}

    # Assuming player_temp, team_data1, and opp_dict are defined elsewhere
    opponent_data = player_temp.groupby(['team_name', 'team_id', 'round']).agg(opp_dict).reset_index()

    # Define opponent features based on the transformed team data
    opp_features = [
        'team_id_team', 
        'round_team'
        # 'total_points_sum_l3r_cum_pct_of_max_team', 'value_sum_l3r_cum_pct_of_max_team',
        # 'transfers_balance_sum_l3r_cum_pct_of_max_team', 'selected_cum_pct_of_max_team', 'transfers_in_sum_l3r_cum_pct_of_max_team',
        # 'transfers_out_sum_l3r_cum_pct_of_max_team', 'ict_index_sum_l3r_cum_pct_of_max_team', 'minutes_sum_l3r_cum_pct_of_max_team',
        # 'goals_scored_sum_l3r_cum_pct_of_max_team', 'assists_sum_l3r_cum_pct_of_max_team', 'clean_sheets_sum_l3r_cum_pct_of_max_team',
        # 'goals_conceded_sum_l3r_cum_pct_of_max_team', 'own_goals_sum_l3r_cum_pct_of_max_team', 'penalties_saved_sum_l3r_cum_pct_of_max_team',
        # 'penalties_missed_sum_l3r_cum_pct_of_max_team', 'yellow_cards_sum_l3r_cum_pct_of_max_team', 'red_cards_sum_l3r_cum_pct_of_max_team',
        # 'saves_sum_l3r_cum_pct_of_max_team', 'bonus_sum_l3r_cum_pct_of_max_team', 'bps_sum_l3r_cum_pct_of_max_team',
        # 'influence_sum_l3r_cum_pct_of_max_team', 'creativity_sum_l3r_cum_pct_of_max_team', 'threat_sum_l3r_cum_pct_of_max_team',
        # 'was_home_sum_l3r_cum_pct_of_max_team'
    ]

    # Merging opponent data
    for r in range(1, 7):
        tmp = team_data[opp_features].copy()
        tmp.columns = [f'{col}_opp{r}' for col in tmp.columns]

        opponent_data = pd.merge(
            opponent_data, tmp,
            left_on=[f'opp_round_{r}', 'round'],
            right_on=[f'team_id_team_opp{r}', f'round_team_opp{r}'],
            how='left'
        )

    # Generate features for the next 3 and 6 opponents
    new_features = []
    for feature in opp_features[2:]:  # Skip 'team_id_team' and 'round_team'
        for num_rounds in (3, 6):
            cols = [f'{feature}_opp{i}' for i in range(1, num_rounds + 1)]
            opp_avg = opponent_data[cols].mean(axis=1)
            opp_min = opponent_data[cols].min(axis=1)
            opp_max = opponent_data[cols].max(axis=1)

            new_features.append(pd.DataFrame(opp_avg, columns=[f'{feature}_opp_avg_n{num_rounds}r']))
            new_features.append(pd.DataFrame(opp_min, columns=[f'{feature}_opp_min_n{num_rounds}r']))
            new_features.append(pd.DataFrame(opp_max, columns=[f'{feature}_opp_max_n{num_rounds}r']))

            if num_rounds == 6:  # Drop after the largest range calculations
                opponent_data.drop(cols, axis=1, inplace=True)

    # Concatenate all new features with the original player_data_lags DataFrame
    opponent_data = pd.concat([opponent_data] + new_features, axis=1)

    # Drop auxiliary merge features
    opponent_data.drop(columns=[f'{feat}{r}' for feat in ['opp_round_', 'team_id_team_opp', 'round_team_opp'] for r in range(1, 7)], axis=1, inplace=True)

    #----------------------------------------------------------------------     
    # 3. Generate player level features
    #----------------------------------------------------------------------
    print("3. Generate player level features")

    vars_list = [
        'total_points', 'value', 'transfers_balance', 'selected', 'transfers_in', 'transfers_out', 'ict_index', 'minutes',
        'goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed',
        'yellow_cards', 'red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat', 'was_home'
    ]

    vars_core = player_temp.columns.difference(vars_list, sort=False).to_list()
    lag_list = [3, 6]

    player_core = player_temp.copy()[vars_core]
    player_data = player_temp.copy()[['element', 'round'] + vars_list]
    
    # Create lagged sum features
    player_data = create_lagged_sums(player_data, 'element', vars_list, [3, 6])

    # Create percentage of max features
    vars_list_2 = player_data.columns.difference(['element', 'round'], sort=False).to_list()
    player_data = create_pct_of_max(player_data, vars_list_2)
    player_data = create_cumulative_pct_of_max(player_data, 'element', vars_list_2)

    # Calculate and store ratio features for both raw lags and pct_of_max lags in the list
    new_features = []
    for var in vars_list:
        ratio_raw = player_data[f'{var}_sum_l3r'] / player_data[f'{var}_sum_l6r']
        ratio_pct_of_max = player_data[f'{var}_sum_l3r_cum_pct_of_max'] / player_data[f'{var}_sum_l6r_cum_pct_of_max']

        # Prepare DataFrames and add them to the list
        new_features.append(pd.DataFrame(ratio_raw, columns=[f'{var}_sum_r_l3r_l6r']))
        new_features.append(pd.DataFrame(ratio_pct_of_max, columns=[f'{var}_max_r_l3r_l6r']))

    # Concatenate all new features with the original player_data_lags DataFrame
    player_data = pd.concat([player_data] + new_features, axis=1)

    # Merge with core data
    player_data = pd.merge(
        player_core, player_data,
        left_on=['element', 'round'],
        right_on=['element', 'round'],
        how='left',
        sort=False
    )

    #----------------------------------------------------------------------
    # 4. Merge DataFrames and create final modelling data
    #----------------------------------------------------------------------
    print("4. Merge DataFrames and create final modelling data")

    # Merge player_data with team_data for final modeling data
    modelling_data = pd.merge(
        player_data, team_data,
        left_on=['team_name', 'round'],
        right_on=['team_name_team', 'round_team'],
        how='left',
        sort=False
    )

    modelling_data = pd.merge(
        modelling_data, opponent_data, 
        left_on=['team_name', 'round'],
        right_on=['team_name', 'round'], 
        how='left', 
        sort=False
    )

    modelling_data['player_name'] = modelling_data['first_name'] + " " + modelling_data['second_name']
    modelling_data.sort_values(['element', 'round'], inplace=True)

    #----------------------------------------------------------------------
    # 5. Targets
    #----------------------------------------------------------------------
    print('5. Create target features')
    # Assuming 'modelling_data' is already defined
    # Group by 'element' once and reuse this grouped object
    grouped = modelling_data.groupby('element')

    # Cumulative sum can be directly calculated without apply
    modelling_data['total_points_cum'] = grouped['total_points'].cumsum()
    
    # Instead of reversing and then rolling, we directly calculate the future rolling sum by shifting first
    shifted_data = modelling_data[::-1].groupby('element')['total_points'].transform(lambda x: x.shift(1))
    modelling_data['total_points_sum_nr'] = shifted_data
    modelling_data['total_points_sum_n3r'] = shifted_data.rolling(window=3, min_periods=1).sum()
    modelling_data['total_points_sum_n6r'] = shifted_data.rolling(window=6, min_periods=1).sum()

    # 'total_points_cum' max for each 'element'
    modelling_data['total_points_sum_all'] = grouped['total_points_cum'].transform('max')

    # Calculating points per game week forward
    modelling_data['total_points_per_gw_forward'] = (modelling_data['total_points_sum_all'] - modelling_data['total_points_cum']) / (38 - modelling_data['round'])

    grouped = modelling_data.groupby('element')
    modelling_data['value_nr'] = grouped['value'].shift(-1)

    columns_to_replace = [
        'total_points_sum_nr', 'total_points_sum_n3r', 'total_points_sum_n6r',
        'total_points_sum_all', 'total_points_per_gw_forward', 'value_nr'
    ]

    # Replace [np.inf, -np.inf, np.nan] with 0 in specified columns in one go
    modelling_data[columns_to_replace] = modelling_data[columns_to_replace].replace([np.inf, -np.inf, np.nan], 0)

    # Calculate 'value_change_nr' directly without change
    modelling_data['value_change_nr'] = modelling_data['value_nr'] - modelling_data['value']

    #----------------------------------------------------------------------
    # Data snooping features :) :) :)
    #----------------------------------------------------------------------
    print('6. Generate data snooping features')
    
    # Since the window size is 1, the rolling sum is equivalent to the value itself,
    # so we can simplify this to just shifting the values by 1 for the 'next' row.
    modelling_data['selected_nr'] = grouped['selected'].shift(-1)
    modelling_data['transfers_in_nr'] = grouped['transfers_in'].shift(-1)
    modelling_data['transfers_out_nr'] = grouped['transfers_out'].shift(-1)
    modelling_data['transfers_balance_nr'] = grouped['transfers_balance'].shift(-1)
    modelling_data['ict_index_nr'] = grouped['ict_index'].shift(-1)

    columns_to_replace = [
        'selected_nr', 'transfers_in_nr', 'transfers_out_nr',
        'transfers_balance_nr', 'ict_index_nr'
    ]

    # Replace [np.inf, -np.inf, np.nan] with 0 in specified columns in one go
    modelling_data[columns_to_replace] = modelling_data[columns_to_replace].replace([np.inf, -np.inf, np.nan], 0)

    # Drop features
    features_to_drop = ['kickoff_time', 'opponent_team', 'team_a_score', 'team_h_score', 'web_name',
                        'team_name_team', 'team_id_team', 'round_team', 'team_id_x', 'team_id_y',
                        'first_name', 'second_name']
    modelling_data.drop(features_to_drop, axis=1, inplace=True)

    # Adjust column order
    columns_to_move = ['element', 'round', 'fixture', 'team_name', 'player_name', 'position', 'position_code']  # Columns you want to move to the start
    remaining_columns = [col for col in modelling_data.columns if col not in columns_to_move]  # All other columns

    # New column order
    new_order = columns_to_move + remaining_columns

    # Reindex the DataFrame with the new column order
    modelling_data = modelling_data[new_order]

    # modelling_data.rename(columns={'element': 'player_id', 'round': 'gw'}, inplace=True)

    # Save a sample
    # modelling_data[modelling_data['element']==5].to_csv('test.csv')

    return modelling_data

def create_modelling_data():
    TABLE_NAME = 'modelling_data'

    drop_table(TABLE_NAME)
    modelling_data = modelling_data_transformations()
    create_table_from_df(TABLE_NAME, modelling_data)

if __name__ == '__main__':

    inspect_tables()

    run_query("SELECT * FROM raw_teams;")
    
    # run_query("SELECT 'total rows: ' || count(*) FROM raw_player_history;")
    # run_query("SELECT 'total rows: ' || count(*) FROM raw_player_history;")
    # all_team_data = team_data_transformations()

    # create_player_static_data()
    # create_transformed_team_data()
    # create_transformed_player_history_data()
    # create_modelling_data()

    # inspect_tables()