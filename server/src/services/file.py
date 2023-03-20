from fastapi import status, HTTPException, UploadFile, Response, BackgroundTasks
import pandas as pd


class FileService:
    def upload_csv(self, file: UploadFile, encoding: str = 'utf-8', sep: str = ',') -> pd.DataFrame:
        return pd.read_csv(file.file, encoding=encoding, sep=sep)

    def download_csv(self, data: pd.DataFrame, filename: str, background_task: BackgroundTasks = None) -> Response:
        headers = {'Content-Disposition': f'attachment; filename={filename}.csv'}
        return Response(data.to_csv(index=False), media_type='text/csv', headers=headers, background=background_task)
