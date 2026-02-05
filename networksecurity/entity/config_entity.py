from datetime import datetime
import os

# Constantes globales del pipeline
# Aquí normalmente están nombres de carpetas, archivos, thresholds, etc.
from networksecurity.constant import training_pipeline


# Debug: imprime el nombre del pipeline y la carpeta base de artifacts
print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)


# ==============================
# CONFIGURACIÓN GENERAL DEL PIPELINE
# ==============================
class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        # Convertimos el timestamp a string para usarlo en paths
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")

        # Nombre lógico del pipeline (ej: network_security)
        self.pipeline_name = training_pipeline.PIPELINE_NAME

        # Carpeta base donde se guardan TODOS los artifacts
        self.artifact_name = training_pipeline.ARTIFACT_DIR

        # Carpeta raíz de esta ejecución concreta del pipeline
        # Ej: artifacts/01_25_2026_10_30_15/
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)

        # Guardamos el timestamp como string
        self.timestamp: str = timestamp


# ==============================
# DATA INGESTION CONFIG
# ==============================
class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Carpeta: artifacts/<timestamp>/data_ingestion/
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )

        # Archivo crudo (feature store)
        # Ej: data_ingestion/feature_store/data.csv
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )

        # Archivo de entrenamiento
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        # Archivo de test
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        # Proporción train/test (ej: 0.2)
        self.train_test_split_ratio: float = (
            training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        )

        # Fuente de datos (MongoDB)
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME


# ==============================
# DATA VALIDATION CONFIG
# ==============================
class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Carpeta: artifacts/<timestamp>/data_validation/
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
        )

        # Datos válidos
        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR
        )

        # Datos inválidos
        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR
        )

        # Paths de archivos válidos
        self.valid_train_file_path: str = os.path.join(
            self.valid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )
        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )

        # Paths de archivos inválidos
        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )
        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )

        # Reporte de data drift
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )


# ==============================
# DATA TRANSFORMATION CONFIG
# ==============================
class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Carpeta: artifacts/<timestamp>/data_transformation/
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )

        # Datos transformados (numpy arrays)
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),
        )

        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"),
        )

        # Objeto de preprocesamiento (scaler, encoder, etc.)
        self.transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,
        )


# ==============================
# MODEL TRAINER CONFIG
# ==============================
class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Carpeta: artifacts/<timestamp>/model_trainer/
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.MODEL_TRAINER_DIR_NAME
        )

        # Modelo entrenado (.pkl)
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir,
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
            training_pipeline.MODEL_FILE_NAME
        )

        # Métrica mínima esperada
        self.expected_accuracy: float = (
            training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        )

        # Umbral para detectar overfitting / underfitting
        self.overfitting_underfitting_threshold = (
            training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD
        )


# ==============================
# MODEL EVALUATION CONFIG
# ==============================
class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Carpeta: artifacts/<timestamp>/model_evaluation/
        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.MODEL_EVALUATION_DIR_NAME
        )

        # Reporte de evaluación
        self.report_file_path = os.path.join(
            self.model_evaluation_dir,
            training_pipeline.MODEL_EVALUATION_REPORT_NAME
        )

        # Umbral mínimo de mejora para aceptar el modelo
        self.change_threshold = (
            training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
        )


# ==============================
# MODEL PUSHER CONFIG
# ==============================
class ModelPusherConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Carpeta: artifacts/<timestamp>/model_pusher/
        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.MODEL_PUSHER_DIR_NAME
        )

        # Path del modelo dentro del pipeline
        self.model_file_path = os.path.join(
            self.model_evaluation_dir,
            training_pipeline.MODEL_FILE_NAME
        )

        # Timestamp UNIX para versionar modelos en producción
        timestamp = round(datetime.now().timestamp())

        # Path final del modelo en producción
        # Ej: saved_models/1706202301/model.pkl
        self.saved_model_path = os.path.join(
            training_pipeline.SAVED_MODEL_DIR,
            f"{timestamp}",
            training_pipeline.MODEL_FILE_NAME
        )
