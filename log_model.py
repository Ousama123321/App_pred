# log_model_only.py
import mlflow
import mlflow.tensorflow

mlflow.set_experiment("Ventes LSTM - versioning")

with mlflow.start_run():
    mlflow.log_param("model_type", "LSTM")
    mlflow.log_param("version", "production-1")
    mlflow.tensorflow.log_model(tf_saved_model_dir="lstm_sales_model.h5", artifact_path="model")
    mlflow.log_artifact("scale.save")
    print("Modèle versionné avec MLflow ✅")
