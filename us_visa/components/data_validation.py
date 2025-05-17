
import json
import sys

import pandas as pd
from evidently.report import Report  # Changed from model_profile to report
from evidently.metric_preset import DataDriftPreset # Changed from DataDriftProfileSection to DataDriftPreset
from pandas import DataFrame

from us_visa.exceptions import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e, sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """
        Method Name :  validate_number_of_columns
        Description :  This method validates the number of columns

        Output       :  Returns bool value based on validation results
        On Failure  :  Write an exception log and then raise an exception
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise USvisaException(e, sys)

    def is_column_exist(self, df: DataFrame) -> bool:
        """
        Method Name :  is_column_exist
        Description :  This method validates the existence of a numerical and categorical columns

        Output       :  Returns bool value based on validation results
        On Failure  :  Write an exception log and then raise an exception
        """
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns) > 0:
                logging.info(f"Missing numerical column: {missing_numerical_columns}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns) > 0:
                logging.info(f"Missing categorical column: {missing_categorical_columns}")

            return False if len(missing_categorical_columns) > 0 or len(missing_numerical_columns) > 0 else True
        except Exception as e:
            raise USvisaException(e, sys) from e

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys)

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame, ) -> bool:
        """
        Method Name :  detect_dataset_drift
        Description :  This method validates if drift is detected

        Output       :  Returns bool value based on validation results
        On Failure  :  Write an exception log and then raise an exception
        """
        try:
            # Initialize a Report with the Data Drift preset.
            data_drift_report = Report(metrics=[
                DataDriftPreset(),
            ])

            # Run the report on the data
            data_drift_report.run(reference_data=reference_df, current_data=current_df)

            # Get the report as a JSON string.
            report = data_drift_report.json()
            json_report = json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

            # Extract relevant information from the JSON report.  Adjust the path to the metrics as needed.  This may require inspection of the json_report structure.
            n_features = json_report.get("summary", {}).get("metrics", {}).get("n_features", 0) # Example, adjust as necessary
            n_drifted_features = json_report.get("summary", {}).get("metrics", {}).get("n_drifted_features", 0) # Example
            drift_status = json_report.get("summary", {}).get("dataset_drift", False) # Example.

            logging.info(f"{n_drifted_features}/{n_features} drift detected.")
            return drift_status
        except Exception as e:
            raise USvisaException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Method Name :  initiate_data_validation
        Description :  This method initiates the data validation component for the pipeline

        Output       :  Returns bool value based on validation results
        On Failure  :  Write an exception log and then raise an exception
        """

        try:
            validation_error_msg = ""
            logging.info("Starting data validation")
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                             DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."
            status = self.validate_number_of_columns(dataframe=test_df)

            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            status = self.is_column_exist(df=train_df)

            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."
            status = self.is_column_exist(df=test_df)

            if not status:
                validation_error_msg += f"columns are missing in test dataframe."

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"Validation_error: {validation_error_msg}")

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e


'''


import json
import sys

import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from pandas import DataFrame

from us_visa.exceptions import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config =read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e,sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """
        Method Name :   validate_number_of_columns
        Description :   This method validates the number of columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise USvisaException(e, sys)

    def is_column_exist(self, df: DataFrame) -> bool:
        """
        Method Name :   is_column_exist
        Description :   This method validates the existence of a numerical and categorical columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical column: {missing_numerical_columns}")


            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical column: {missing_categorical_columns}")

            return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True
        except Exception as e:
            raise USvisaException(e, sys) from e

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys)

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        """
        Method Name :   detect_dataset_drift
        Description :   This method validates if drift is detected using Evidently's DataDriftPreset.
        
        Output      :   Returns bool value based on validation results (True if drift is detected, False otherwise)
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Starting dataset drift detection.")
            # Create a DataDriftPreset report
            data_drift_report = Report(metrics=[DataDriftPreset(),])

            # Run the report
            # For DataDriftPreset, current_data is the new data, reference_data is the baseline (e.g., training data)
            data_drift_report.run(current_data=current_df, reference_data=reference_df, column_mapping=None)

            # Get the report as a dictionary
            report_dict = data_drift_report.as_dict()

            # Save the drift report to a file (e.g., YAML or JSON)
            # The content being written is a dictionary, which write_yaml_file should handle.
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=report_dict)

            # Extracting drift information from the report dictionary
            # The structure of the dictionary depends on the metrics used.
            # For DataDriftPreset, the results are typically in the first metric's 'result' field.
            drift_metrics = report_dict['metrics'][0]['result'] # Assuming DataDriftPreset is the first/only metric

            n_features = drift_metrics.get('number_of_columns')
            n_drifted_features = drift_metrics.get('number_of_drifted_columns')
            dataset_drift_detected = drift_metrics.get('dataset_drift') # This is a boolean

            if n_features is not None and n_drifted_features is not None:
                logging.info(f"Drift detection summary: {n_drifted_features} out of {n_features} features drifted.")
            else:
                logging.warning("Could not extract number of features or drifted features from the report.")
            
            if dataset_drift_detected is None:
                logging.error("Dataset drift status (boolean) not found in the report. Assuming no drift as a fallback.")
                return False # Fallback or raise an error

            logging.info(f"Dataset drift detected: {dataset_drift_detected}")
            return dataset_drift_detected

        except KeyError as e:
            logging.error(f"KeyError accessing drift report details: {e}. Report structure might have changed or metric failed.")
            raise USvisaException(f"Error parsing drift report: {e}", sys) from e
        except Exception as e:
            logging.error(f"An error occurred during dataset drift detection: {e}")
            raise USvisaException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            validation_error_msg = ""
            logging.info("Starting data validation")
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."
            status = self.validate_number_of_columns(dataframe=test_df)

            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            status = self.is_column_exist(df=train_df)

            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."
            status = self.is_column_exist(df=test_df)

            if not status:
                validation_error_msg += f"columns are missing in test dataframe."

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"Validation_error: {validation_error_msg}")
                

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e


'''