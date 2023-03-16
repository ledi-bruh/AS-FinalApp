import os
from fastapi import status, HTTPException
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
from math import sqrt
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
import joblib

class MLService:
    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data.set_index('index', inplace=True)
        data.drop(columns=['Meter Scope', 'Location', 'UMIS BILL ID', 'Service Start Date', 'Service End Date'], inplace=True)
        
        for col in ('Meter AMR', 'Funding Source', 'AMP #'):
            data[col].fillna(data[col].mode()[0], inplace=True)
        
        for col in ('Development Name', 'Borough', 'Account Name', 'Meter AMR', 'RC Code', 'Funding Source',
                    'AMP #', 'Vendor Name', 'Revenue Month', 'Meter Number', 'Estimated'):
            data[col] = data[col].map({v: k+1 for k, v in enumerate(data[col].unique())})
        # ! надо запоминать соответствия
        
        return data
        
    
    def fit(self, X_train, y_train, seed: int = 42) -> None:
        model = XGBRegressor(max_depth=7, n_estimators=110, seed=seed).fit(X_train, y_train)
        
        with open('model.sav', 'wb') as f:
            joblib.dump(model, f, compress=3)
    
    def get_quality(self, model):
        y_test: object
        y_pred = self.predict_data()
        return {
            'MAE': mean_absolute_error(y_test, y_pred),
            'MSE': mean_squared_error(y_test, y_pred),
            'RMSE': sqrt(mean_squared_error(y_test, y_pred)),
            'MAPE': mean_absolute_percentage_error(y_test, y_pred),
            'R^2': r2_score(y_test, y_pred),
        }
    
    def predict_data(self, X_test) -> pd.DataFrame:
        if not os.path.isfile('model.sav'):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='Отсутствует файл с моделью')
        
        with open('model.sav', 'rb') as f:
            model: XGBRegressor = joblib.load(f)
        
        # if not model:
        #     raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='Модель не обучена')
        
        return pd.DataFrame(model.predict(X_test))
