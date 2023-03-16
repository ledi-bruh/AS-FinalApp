from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, Response, BackgroundTasks
from pydantic import UUID4
import pandas as pd
from src.services.ml import MLService
from src.services.file import FileService
from src.services.auth import get_current_user
from api.utils.query_logger import QUERY_LOGGER

router = APIRouter(
    prefix='/ml',
    tags=['ml'],
    # dependencies=[Depends(get_current_user), Depends(QUERY_LOGGER)]
)


@router.post('/prepare', name='Предобработать данные')
def prepare_data(background_task: BackgroundTasks, file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    headers = {'Content-Disposition': f'attachment; filename=prepared_data.csv'}
    return Response(service.prepare_data(data).to_csv(), media_type='text/csv', headers=headers, background=background_task)


@router.post('/predict', name='Получить предсказания')
def predict_data(background_task: BackgroundTasks, file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    headers = {'Content-Disposition': f'attachment; filename=prepared_data.csv'}
    return Response(service.predict_data(data).to_csv(), media_type='text/csv', headers=headers, background=background_task)


@router.get('/quality', name='Узнать качество модели')
def get_quality(service: MLService = Depends()):
    return service.get_quality()
