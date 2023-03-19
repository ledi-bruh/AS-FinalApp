from fastapi import APIRouter, Depends, UploadFile, Response, BackgroundTasks
from src.services.ml import MLService
from src.services.file import FileService
from src.services.auth import get_current_user
from src.api.utils.query_logger import QUERY_LOGGER


router = APIRouter(
    prefix='/ml',
    tags=['ml'],
    dependencies=[Depends(get_current_user), Depends(QUERY_LOGGER)]
)


@router.post('/prepare', name='Предобработать данные')
def prepare_df(background_task: BackgroundTasks, file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    headers = {'Content-Disposition': f'attachment; filename=prepared_data.csv'}
    return Response(service.prepare_df(data).to_csv(index=False), media_type='text/csv', headers=headers, background=background_task)


@router.post('/fit', name='Обучить модель на предобработанных данных')
def fit_df(file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    return service.fit_df(data)


@router.post('/fit/prepare', name='Обучить модель на не предобработанных данных')
def fit_df_with_prepare(file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    return service.fit_df_with_prepare(data)


@router.post('/predict', name='Получить предсказания на предобработанных данных')
def predict_df(background_task: BackgroundTasks, file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    headers = {'Content-Disposition': f'attachment; filename=predicted_data.csv'}
    return Response(service.predict_df(data).to_csv(index=False), media_type='text/csv', headers=headers, background=background_task)


@router.post('/predict/prepare', name='Получить предсказания на не предобработанных данных')
def predict_df_with_prepare(background_task: BackgroundTasks, file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    headers = {'Content-Disposition': f'attachment; filename=predicted_data.csv'}
    return Response(service.predict_df_with_prepare(data).to_csv(index=False), media_type='text/csv', headers=headers, background=background_task)


@router.post('/quality', name='Узнать качество модели по предобработанным данным')
def get_quality_df(file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    return service.get_quality_df(data)


@router.post('/quality/prepare', name='Узнать качество модели по предобработанным данным')
def get_quality_df(file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    return service.get_quality_df_with_prepare(data)
