import pandas as pd
import numpy as np

np.random.seed(42)
data = {
    'user_id': range(1, 101),
    'mock_exam_score_before': np.random.randint(30, 70, 100),
    'mock_exam_score_after': np.random.randint(50, 100, 100),
    'requests_count': np.random.randint(50, 250, 100),
    'time_spent_hours': np.round(np.random.uniform(5, 30, 100), 1)
}

df = pd.DataFrame(data)
df.to_csv('data/synthetic_data.csv', index=False)
print("Синтетические данные сгенерированы: data/synthetic_data.csv")