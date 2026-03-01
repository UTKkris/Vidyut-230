import pandas as pd
import xgboost as xgb
import pickle
from sklearn.metrics import mean_squared_error

def train():
    df = pd.read_csv('grid_data.csv')
    
    normal_data = df[df['is_theft'] == 0]
    
    X = normal_data[['hour', 'temperature', 'base_load']]
    y = normal_data['expected_load']
    
    model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1)
    model.fit(X, y)
    
    predictions = model.predict(X)
    rmse = mean_squared_error(y, predictions, squared=False)
    print(f"trained Baseline RMSE: {rmse:.2f} kW")
    
    with open('vidyut.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Saved to vidut.pkl")

if __name__ == "__main__":
    train()