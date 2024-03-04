import sys
import os
from dataclasses import dataclass
import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder , StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformation()
        
    def get_data_transformer_object(self):
        # This function is responsible for data transformation
        try:
            numerical_columns = [
                'writing score','reading score'
                ]
            catagorical_column = [
                'gender',
                'race/ethnicity',
                'parental level of education',
                'lunch',
                'test preparation course'
            ]
            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy="median")),
                    ('scaler',StandardScaler())
                ]
            )
            
            logging.info("numerical columns scaling completed")
            
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy="most_frequent")),
                    ('one_hot_encoder',OneHotEncoder())
                    ('scaler',StandardScaler())
                ]
            )
            logging.info("catagorical columns encoding and scaling completed")
            
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns)
                    ("cat_pipeline",cat_pipeline,catagorical_column)
                ]
            )
            
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("read train test data completed")
            
            logging.info("Obtaining preprocessing object")
            
            
            preprocessing_obj = self.get_data_transformer_object()
            target_column_name = ['writing score','reading score']
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.fit_transform(input_feature_test_df)
            
            train_arr =np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            
            test_arr =np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)
            ]
            
            save_obj(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj =preprocessing_obj
            )
            
            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except:
            pass    
                