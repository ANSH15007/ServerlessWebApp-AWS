import boto3
import pandas as pd
from datetime import datetime
import os

class ETLService:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.glue = boto3.client('glue')
        self.data_bucket = os.environ['DATA_BUCKET']

    def trigger_etl_job(self, job_name: str):
        try:
            response = self.glue.start_job_run(
                JobName=job_name,
                Arguments={
                    '--job-timestamp': datetime.now().isoformat()
                }
            )
            return response['JobRunId']
        except Exception as e:
            print(f"Error triggering ETL job: {e}")
            return None

    def process_customer_segments(self, data):
        # Example segmentation logic based on purchase history
        df = pd.DataFrame(data)
        df['total_spent'] = pd.to_numeric(df['total_spent'])
        
        segments = {
            'premium': df[df['total_spent'] > 1000],
            'regular': df[(df['total_spent'] >= 100) & (df['total_spent'] <= 1000)],
            'new': df[df['total_spent'] < 100]
        }
        
        return segments