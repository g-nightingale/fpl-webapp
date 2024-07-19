import pandas as pd
from sklearn.preprocessing import StandardScaler

test_data = {
    'element': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
    'round': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    'feature_1': [1, 2, 3, 4, 5, 2, 4, 6, 8, 10, 1, 8, 27, 64, 125]

}

def create_lagged_sums(df, grouping_feature, features_list, lags, name_prefix=''):
    grouped_by = df.groupby(grouping_feature)

    for lag in lags:
        for feature in  features_list:
            lag_feature_name = f'{name_prefix}{feature}_sum_l{lag}r'
            df[lag_feature_name] = grouped_by[feature].rolling(window=lag, min_periods=1).sum().reset_index(drop=True)

    return df

def create_pct_of_max(df, features_list, name_prefix=''):
        
    # Calculate the max of the cumulative sums for each 'round'
    # This needs to be done in a way that respects the original DataFrame structure
    group_by_round = df.groupby('round')
    
    new_features = []
    for feature in features_list:
        new_feature_name = f'{name_prefix}{feature}_pct_of_max'
        
        max_round = group_by_round[feature].transform('max')
        
        # Calculate the percentage of the cumulative sum relative to its round-wise maximum
        pct_of_max = df[feature] / max_round
        pct_of_max.name = new_feature_name

        # Prepare DataFrames and add them to the list
        new_features.append(pd.DataFrame(pct_of_max, columns=[new_feature_name]))

    # Concatenate all new features with the original player_data_lags DataFrame
    df = pd.concat([df] + new_features, axis=1)

    return df

def create_cumulative_pct_of_max(df, grouping_feature, features_list, name_prefix=''):
    # Calculate cumulative sum for each feature within 'element' groups
    group_by = df.groupby(grouping_feature)

    new_features = []
    for feature in features_list:
        new_feature_name = f'{feature}_cum'

        col_cum_sum = group_by[feature].cumsum()
        col_cum_sum.name = new_feature_name
        new_features.append(pd.DataFrame(col_cum_sum, columns=[new_feature_name]))

    df = pd.concat([df] + new_features, axis=1)
        
    # Calculate the max of the cumulative sums for each 'round'
    # This needs to be done in a way that respects the original DataFrame structure
    group_by_round = df.groupby('round')
    
    new_features = []
    for feature in features_list:
        cum_feature_name = f'{feature}_cum'
        new_feature_name = f'{name_prefix}{feature}_cum_pct_of_max'
        
        # Directly calculate max of cumulated sums over 'round' without an intermediate groupby object
        max_round = group_by_round[cum_feature_name].transform('max')
        
        # Calculate the percentage of the cumulative sum relative to its round-wise maximum
        cum_pct_of_max = df[cum_feature_name] / max_round
        cum_pct_of_max.name = new_feature_name

        # Prepare DataFrames and add them to the list
        new_features.append(pd.DataFrame(cum_pct_of_max, columns=[new_feature_name]))

    # Concatenate all new features with the original player_data_lags DataFrame
    df = pd.concat([df] + new_features, axis=1)

    # Optionally, drop the intermediate columns if they are not needed
    df.drop(columns=[f'{feature}_cum' for feature in features_list], inplace=True)

    return df

def scale_features(df, features_to_scale, name_suffix='_stdsclr'):
    # Initialize the StandardScaler
    scaler = StandardScaler()

    # Fit and transform the selected features
    scaled_features = scaler.fit_transform(df[features_to_scale])

    # Create a DataFrame with the scaled features, appending "_scl" to the column names
    scaled_features_df = pd.DataFrame(scaled_features, columns=[f"{col}{name_suffix}" for col in features_to_scale])

    # Concatenate the scaled features DataFrame to the original DataFrame
    df = pd.concat([df, scaled_features_df], axis=1)

    return df

def main():
    df = pd.DataFrame(test_data)
    print(df.head(20), '\n')

    features_list = ['feature_1']
    name_prefix = 'player_'
    df = create_lagged_sums(df, 'element', features_list, [3], name_prefix=name_prefix)
    df = create_pct_of_max(df, features_list, name_prefix=name_prefix)
    df = create_cumulative_pct_of_max(df, 'element', features_list, name_prefix=name_prefix)
    df = scale_features(df, features_list)
    # df['pct_of_max'] = create_cumulative_pct_of_max(grouped_by_element, grouped_by_round, 'feature_1')
    print(df.head(20), '\n')

if __name__ == '__main__':
    main()

