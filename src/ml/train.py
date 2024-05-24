import pandas as pd
import numpy as np
import lightgbm as lgb
import sys
import os
import json

# Hack to use relative imports
utils_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../utilities'))
if utils_dir not in sys.path:
    sys.path.append(utils_dir)

# Now you can import the module from the parent directory
from db_helpers import connect_rds, create_table_from_df

CONFIG_FILE = 'config.json'

def rmse(y_actual, y_predictions):
    """
    Calculate the Root Mean Squared Error between actual and predicted values.

    Parameters:
    - y_actual (array-like): The actual values.
    - y_predictions (array-like): The predicted values.

    Returns:
    - float: The calculated RMSE.
    """
    y_actual = np.array(y_actual)
    y_predictions = np.array(y_predictions)
    
    # Calculate the Mean Squared Error (MSE)
    mse = np.mean((y_actual - y_predictions) ** 2)
    
    # Return the square root of MSE to get RMSE
    return np.sqrt(mse)

def train_test_split_pandas(X, y, test_size=0.25, random_state=None):
    """
    Split X (features) and y (labels) into train and test sets.

    Parameters:
    - X (DataFrame): The features of the dataset (Pandas DataFrame).
    - y (Series): The labels of the dataset (Pandas Series).
    - test_size (float or int): If float, it represents the proportion of the dataset to include in the test split.
                                If int, it represents the absolute number of test samples.
    - random_state (int, optional): A seed value to make the shuffle deterministic.

    Returns:
    - X_train (DataFrame): The training set of features.
    - X_test (DataFrame): The testing set of features.
    - y_train (Series): The training set of labels.
    - y_test (Series): The testing set of labels.
    """
    
    # Set the seed for reproducibility
    if random_state is not None:
        np.random.seed(random_state)
    
    # Generate random indices
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    
    # Determine the number of test samples
    if isinstance(test_size, float):
        test_size = int(X.shape[0] * test_size)
    
    # Split indices into training and testing
    test_indices = indices[:test_size]
    train_indices = indices[test_size:]
    
    # Split the data into training and testing sets
    X_train = X.iloc[train_indices]
    X_test = X.iloc[test_indices]
    y_train = y.iloc[train_indices]
    y_test = y.iloc[test_indices]
    
    return X_train, X_test, y_train, y_test


def create_holdout_set(df):
    '''
    The holdout set is the latest gameweek for which we want to make predictions for.
    '''
    # Select the last row for each 'id'
    holdout = df.groupby('element').tail(1)

    # To avoid dealing with merge suffixes, we can use an alternative approach:
    # Create a boolean mask that marks the last rows of each group
    mask = df.groupby('element').cumcount(ascending=False) == 0

    # Use the mask to filter rows
    non_holdout = df[~mask]

    return holdout, non_holdout

def train_model():

    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)

    QUERY = 'SELECT * FROM modelling_data'

    # Load config
    TARGET_FEATURE = config['target_feature']
    ID_FEATURES = config['id_features']
    HOLDOUT_FEATURES = config['holdout_features']
    FEATURES_TO_DROP = config['features_to_drop']
    N_ESTIMATORS = config['n_estimators']
    TEST_SIZE = config['test_size']
    RANDOM_STATE = config['random_state']
    TOP_N_FEATURES = config['top_n_features']
    MIN_CHILD_SAMPLES = config['min_child_samples']
    
    engine = connect_rds()

    # Load the data into a Pandas DataFrame
    df = pd.read_sql(QUERY, engine)

    # Check shape
    print(df.shape)
    print(df.isna().sum().sum())

    # Handle null and inf values
    df = df.fillna(0.0)
    df.replace([np.inf, -np.inf], 0.0, inplace=True)

    performance_dict = {}

    x_holdout, x = create_holdout_set(df)

    print(x.head())

    # Assuming you have a DataFrame 'df' with your data
    # Let's say 'target' is the column you want to predict, and the rest are the features
    y = x[TARGET_FEATURE]
    x = x.drop(FEATURES_TO_DROP, axis=1)

    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split_pandas(x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

    # Preserve id features
    # ids_train = x_train[ID_FEATURES]
    # ids_test = x_test[ID_FEATURES]

    x_train.drop(ID_FEATURES, axis=1, inplace=True)
    x_test.drop(ID_FEATURES, axis=1, inplace=True)

    print(f'Target averages\nTrain: {y_train.mean()}\nTest: {y_test.mean()}')

    #----------------------------------------------------------------------
    # Light GBM
    #----------------------------------------------------------------------

    # Initialize the LightGBM Regressor
    lgb_regressor = lgb.LGBMRegressor(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE, min_child_samples=MIN_CHILD_SAMPLES)

    # Fit the model on the training data
    lgb_regressor.fit(x_train, y_train)

    # Predict on the testing set (optional, for model evaluation)
    train_preds = lgb_regressor.predict(x_train)
    test_preds = lgb_regressor.predict(x_test)

    # Output the feature importances
    feature_importances = lgb_regressor.feature_importances_

    # Create a DataFrame to view the feature importances more easily
    lgb_features_df = pd.DataFrame({'Feature': x_train.columns, 'Importance': feature_importances})

    # Sort the DataFrame to see the most important features at the top
    lgb_features_df.sort_values(by='Importance', ascending=False, inplace=True)

    performance_dict['lgb - train'] = rmse(y_train, train_preds)
    performance_dict['lgb - test'] = rmse(y_test, test_preds)

    #----------------------------------------------------------------------
    # Evaluation
    #----------------------------------------------------------------------
    top_lgb_features = lgb_features_df[:TOP_N_FEATURES]

    print(top_lgb_features)
    print(performance_dict)

    #----------------------------------------------------------------------
    # Second pass training run with best features
    #----------------------------------------------------------------------
    x_train_lgb = x_train[top_lgb_features['Feature']]
    x_test_lgb = x_test[top_lgb_features['Feature']]

    # Fit the model on the training data
    lgb_regressor.fit(x_train_lgb, y_train)

    # Predict on the testing set (optional, to evaluate the model)
    train_preds = lgb_regressor.predict(x_train_lgb)
    test_preds = lgb_regressor.predict(x_test_lgb)

    performance_dict['lgb - train feature reduction'] = rmse(y_train, train_preds)
    performance_dict['lgb - test feature reduction'] = rmse(y_test, test_preds)

    print(performance_dict)


    #----------------------------------------------------------------------
    # Update holdout sample and create table
    #----------------------------------------------------------------------
    preds_holdout = lgb_regressor.predict(x_holdout[top_lgb_features['Feature']])

    holdout = x_holdout[ID_FEATURES + HOLDOUT_FEATURES]
    holdout['predicted_points_n3r'] = np.round(preds_holdout, 2)

    print(holdout.head(20))

    create_table_from_df('player_points_predictions', holdout)

if __name__ == '__main__':
    train_model()