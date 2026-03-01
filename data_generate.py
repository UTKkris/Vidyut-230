import pandas as pd
import numpy as np

def generate_grid_data(days=30):
    np.random.seed(42)
    hours = days * 24
    
    time_of_day = np.tile(np.arange(24), days)
    temperature = 25 + 10 * np.sin(np.pi * time_of_day / 12) + np.random.normal(0, 2, hours)
    base_load = 100 + 50 * np.sin(np.pi * (time_of_day - 6) / 12)
    
    expected_load = base_load + (temperature * 0.5) 
    
    reported_load = expected_load.copy()
    
    theft_indices = np.random.choice(hours, size=int(hours * 0.05), replace=False)
    reported_load[theft_indices] *= np.random.uniform(0.6, 0.8, size=len(theft_indices))
    
    df = pd.DataFrame({
        'hour': time_of_day,
        'temperature': temperature,
        'base_load': base_load,
        'expected_load': expected_load,
        'reported_load': reported_load,
        'is_theft': np.isin(np.arange(hours), theft_indices).astype(int)
    })
    
    df.to_csv('grid_data.csv', index=False)
    print("Generated grid_data.csv with simulated theft patterns.")

if __name__ == "__main__":
    generate_grid_data()