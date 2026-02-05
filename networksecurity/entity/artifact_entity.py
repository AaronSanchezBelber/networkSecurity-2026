from dataclasses import dataclass


# ==============================
# DATA INGESTION ARTIFACT
# ==============================
@dataclass
class DataIngestionArtifact:
    """
    Resultado del paso Data Ingestion.

    Contiene las rutas a los archivos generados
    después de traer los datos desde la fuente (ej: MongoDB)
    y separarlos en train y test.
    """
    trained_file_path: str   # Path al archivo de entrenamiento
    test_file_path: str      # Path al archivo de prueba


# ==============================
# DATA VALIDATION ARTIFACT
# ==============================
@dataclass
class DataValidationArtifact:
    """
    Resultado del paso Data Validation.

    Indica si los datos son válidos, dónde quedaron los datos
    aceptados y rechazados, y el reporte de data drift.
    """
    validation_status: bool             # ¿Pasó la validación?
    valid_train_file_path: str           # Train válido
    valid_test_file_path: str            # Test válido
    invalid_train_file_path: str         # Train inválido
    invalid_test_file_path: str          # Test inválido
    drift_report_file_path: str           # Reporte de drift


# ==============================
# DATA TRANSFORMATION ARTIFACT
# ==============================
@dataclass
class DataTransformationArtifact:
    """
    Resultado del paso Data Transformation (feature engineering).

    Contiene los datos transformados y el objeto de preprocesamiento
    que se usará en entrenamiento y predicción.
    """
    transformed_object_file_path: str    # Scaler / Encoder serializado
    transformed_train_file_path: str     # Train transformado (.npy)
    transformed_test_file_path: str      # Test transformado (.npy)


# ==============================
# METRICS ARTIFACT
# ==============================
@dataclass
class ClassificationMetricArtifact:
    """
    Artifact reutilizable para métricas de clasificación.
    """
    f1_score: float
    precision_score: float
    recall_score: float


# ==============================
# MODEL TRAINER ARTIFACT
# ==============================
@dataclass
class ModelTrainerArtifact:
    """
    Resultado del paso Model Trainer.

    Contiene el modelo entrenado y las métricas
    tanto en train como en test.
    """
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact


# ==============================
# MODEL EVALUATION ARTIFACT
# ==============================
@dataclass
class ModelEvaluationArtifact:
    """
    Resultado del paso Model Evaluation.

    Decide si el nuevo modelo es mejor que el actual
    y guarda la comparación de métricas.
    """
    is_model_accepted: bool                     # ¿Se acepta el modelo nuevo?
    improved_accuracy: float                    # Mejora respecto al anterior
    best_model_path: str                        # Path del mejor modelo histórico
    trained_model_path: str                     # Path del modelo recién entrenado
    train_model_metric_artifact: ClassificationMetricArtifact
    best_model_metric_artifact: ClassificationMetricArtifact


# ==============================
# MODEL PUSHER ARTIFACT
# ==============================
@dataclass
class ModelPusherArtifact:
    """
    Resultado del paso Model Pusher (deployment).

    Indica dónde quedó el modelo final listo para producción.
    """
    saved_model_path: str       # Path final en prod / saved_models
    model_file_path: str        # Path del modelo dentro del pipeline
