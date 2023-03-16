from fastapi import status, HTTPException, UploadFile
import pandas as pd


class FileService:
    def upload_csv(self, file: UploadFile, encoding: str = 'utf-8', sep: str = ',') -> pd.DataFrame:
        if file.content_type != 'text/csv':
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Файл должен быть в формате csv')
        return pd.read_csv(file.file, encoding=encoding, sep=sep)
    
    def download(self):
        ...
    
