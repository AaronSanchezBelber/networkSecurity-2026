from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logger.logger import logging 
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):
        """
        Constructor de la clase DataValidation.
        Inicializa los artefactos de ingestión y configuración de validación
        y carga el esquema desde el archivo YAML.
        """
        try:
            # Artefacto generado por Data Ingestion
            self.data_ingestion_artifact = data_ingestion_artifact

            # Configuración específica de Data Validation
            self.data_validation_config = data_validation_config

            # Cargar el esquema (columnas, tipos, etc.) desde el archivo YAML
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            # Manejo centralizado de excepciones
            raise NetworkSecurityException(e, sys)
    
    
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Valida que el número de columnas del dataframe
        coincida con el definido en el esquema.
        """
        try:
            # Número de columnas requeridas según el esquema
            number_of_columns = len(self._schema_config["columns"])

            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")

            # Comparación entre columnas esperadas y columnas reales
            if len(dataframe.columns) == number_of_columns:
                return True
            
            return False

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        """
        Verifica que todas las columnas numéricas definidas
        en el esquema existan en el dataframe.
        """
        try:
            # Columnas numéricas esperadas según el esquema
            numerical_columns = self._schema_config["numerical_columns"]

            # Columnas presentes en el dataframe
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_columns = []

            # Validar existencia de cada columna numérica
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_columns.append(num_column)
            
            logging.info(f"Missing numerical columns: {missing_numerical_columns}")

            return numerical_column_present

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Lee un archivo CSV y lo devuelve como DataFrame.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    

    def detect_dataset_drift(
        self,
        base_df: pd.DataFrame,
        current_df: pd.DataFrame,
        threshold: float = 0.05
    ) -> bool:
        """
        Detecta data drift usando el test estadístico KS (Kolmogorov-Smirnov).
        Retorna True si NO hay drift significativo.
        """
        try:
            status = True  # Indica si el dataset es válido (sin drift)
            report = {}    # Reporte de drift por columna

            for column in base_df.columns:
                # Distribuciones de la columna en ambos datasets
                d1 = base_df[column]
                d2 = current_df[column]

                # Prueba KS
                is_same_dist = ks_2samp(d1, d2)

                # Comparación del p-value con el umbral
                if is_same_dist.pvalue >= threshold:
                    is_found = False  # No hay drift
                else:
                    is_found = True   # Hay drift
                    status = False

                # Guardar resultados por columna
                report[column] = {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }

            # Ruta donde se guardará el reporte de drift
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Crear directorio si no existe
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Guardar reporte en formato YAML
            write_yaml_file(
                file_path=drift_report_file_path,
                content=report
            )

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)
         

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Orquesta todo el proceso de validación de datos:
        - Lectura de datos
        - Validación de columnas
        - Detección de data drift
        - Generación del artefacto de validación
        """
        try:
            # Rutas de los archivos generados en Data Ingestion
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Lectura de datasets
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            # Validar número de columnas en train
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = "Train dataframe does not contain all columns.\n"

            # Validar número de columnas en test
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = "Test dataframe does not contain all columns.\n"
            
            # Detección de data drift
            status = self.detect_dataset_drift(
                base_df=train_dataframe,
                current_df=test_dataframe
            )
            
            # Crear directorio para los archivos validados
            dir_path = os.path.dirname(
                self.data_validation_config.valid_train_file_path
            )
            os.makedirs(dir_path, exist_ok=True)
            
            # Guardar datasets validados
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True
            )

            # Crear artefacto de salida de Data Validation
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

# ¿Qué es data drift?

# Data drift ocurre cuando los datos que llegan al modelo cambian con el tiempo respecto a los datos con los que fue entrenado.

# 👉 El modelo sigue siendo el mismo
# 👉 El código sigue siendo el mismo
# ❌ Pero los datos ya no se parecen

# Resultado: el rendimiento del modelo se degrada.