from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks
from src.services.ml import MLService
from src.services.file import FileService
from src.dependencies import AUTHORIZED, QUERY_LOGGER


router = APIRouter(
    prefix='/ml',
    tags=['ml'],
    dependencies=[Depends(AUTHORIZED), Depends(QUERY_LOGGER)]
)


@router.post('/prepare', name='Предобработать данные')
def prepare_df(background_task: BackgroundTasks, file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    return file_service.download_csv(service.prepare_df(data), 'prepared_data', background_task)


@router.post('/fit', name='Обучить модель на предобработанных данных')
def fit_df(file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    return service.fit_df(data)


@router.post('/fit/prepare', name='Обучить модель на не предобработанных данных')
def fit_df_with_prepare(file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    file_service.save_df_to_csv(data, 'train_data')
    return service.fit_df_with_prepare(data)


@router.post('/predict', name='Получить предсказания на предобработанных данных')
def predict_df(background_task: BackgroundTasks, file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    return file_service.download_csv(service.predict_df(data), 'predicted_data', background_task)


@router.post('/predict/prepare', name='Получить предсказания на не предобработанных данных')
def predict_df_with_prepare(background_task: BackgroundTasks, file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    return file_service.download_csv(service.predict_df_with_prepare(data), 'predicted_data', background_task)


@router.post('/quality', name='Узнать качество модели по предобработанным данным')
def get_quality_df(file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    return service.get_quality_df(data)


@router.post('/quality/prepare', name='Узнать качество модели по не предобработанным данным')
def get_quality_df(file: UploadFile, encoding: str = 'utf-8', sep: str = ',', service: MLService = Depends(), file_service: FileService = Depends()):
    data = file_service.upload_csv(file, encoding=encoding, sep=sep)
    return service.get_quality_df_with_prepare(data)


@router.get('/train_data', name='Получить датасет')
def get_df(file_service: FileService = Depends()):
    return file_service.get_df_from_csv('train_data').to_json(orient='records')
