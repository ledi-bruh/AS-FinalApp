import os
import joblib
import numpy as np
import pandas as pd
from math import sqrt
from fastapi import status, HTTPException
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, FunctionTransformer
from xgboost import XGBRegressor


class MLService:
    def __init__(self):
        self.target: str = 'Consumption (GAL)'

        self.numeric_cols: list = ['# days', 'TDS #', 'Current Charges', 'EDP']

        self.categorical_cols: list = ['Development Name', 'Borough', 'Account Name', 'Meter AMR', 'RC Code',
                                       'Funding Source', 'AMP #', 'Vendor Name', 'Meter Number', 'Estimated', 'Revenue Month']
    
    def fit_preprocessor(self, data: pd.DataFrame) -> None:
        cols_to_drop: list = ['index', 'Location', 'Meter Scope',
                              'UMIS BILL ID', 'Service Start Date', 'Service End Date']

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
        ])

        preprocessor = ColumnTransformer(transformers=[
            ('drop', FunctionTransformer(
                pd.DataFrame.drop,
                kw_args={'columns': cols_to_drop}), cols_to_drop),
            ('num', numeric_transformer, self.numeric_cols),
            ('cat', categorical_transformer, self.categorical_cols)
        ], remainder='passthrough')
        
        X_df = data.drop([self.target], axis=1) if self.target in data.columns else data
        preprocessor.fit(X_df)
        
        with open('data/models/preprocessor.joblib', 'wb') as f:
            joblib.dump(preprocessor, f, compress=3)

    def prepare_df(self, data: pd.DataFrame) -> pd.DataFrame:
        if not os.path.isfile('data/models/preprocessor.joblib'):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Нет файла для предобработки')
            
        with open('data/models/preprocessor.joblib', 'rb') as f:
            preprocessor: ColumnTransformer = joblib.load(f)
        
        y_df = data[self.target] if self.target in data.columns else None
        X_df = data.drop([self.target], axis=1) if self.target in data.columns else data
        data = pd.DataFrame(preprocessor.transform(X_df), columns=self.numeric_cols+self.categorical_cols)
        if y_df is not None:
            data[self.target] = y_df
        return data

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        model = XGBRegressor(seed=73, max_depth=7)
        model.fit(X_train, y_train)

        with open('data/models/model.joblib', 'wb') as f:
            joblib.dump(model, f, compress=3)

    def fit_df(self, data: pd.DataFrame) -> None:
        y = data[self.target]
        X = data.drop([self.target], axis=1)
        self.fit(np.array(X), np.array(y))

    def fit_df_with_prepare(self, data: pd.DataFrame) -> None:
        self.fit_preprocessor(data)
        self.fit_df(self.prepare_df(data))

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not os.path.isfile('data/models/model.joblib'):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Нет файла с моделью')

        with open('data/models/model.joblib', 'rb') as f:
            model: XGBRegressor = joblib.load(f)

        return model.predict(X)

    def predict_df(self, data: pd.DataFrame) -> pd.DataFrame:
        X = data.drop([self.target], axis=1) if self.target in data.columns else data
        return pd.DataFrame(self.predict(np.array(X)), columns=[self.target])

    def predict_df_with_prepare(self, data: pd.DataFrame) -> pd.DataFrame:
        X = self.prepare_df(data)
        X = X.drop([self.target], axis=1) if self.target in X.columns else X
        return self.predict_df(X)

    def get_quality(self, y_test: np.ndarray, y_pred: np.ndarray) -> dict:
        return {
            'R^2': r2_score(y_test, y_pred),
            'MAE': mean_absolute_error(y_test, y_pred),
            'MSE': mean_squared_error(y_test, y_pred),
            'RMSE': sqrt(mean_squared_error(y_test, y_pred)),
            'MAPE': mean_absolute_percentage_error(y_test, y_pred),
        }

    def get_quality_df(self, data: pd.DataFrame) -> dict:
        y = data[self.target]
        X = data.drop([self.target], axis=1)
        return self.get_quality(y, self.predict(X))

    def get_quality_df_with_prepare(self, data: pd.DataFrame) -> dict:
        y = data[self.target]
        X = self.prepare_df(data.drop([self.target], axis=1))
        return self.get_quality(y, self.predict(X))
