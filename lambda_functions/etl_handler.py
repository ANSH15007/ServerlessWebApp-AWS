import json
import boto3
from services.etl_service import ETLService

def handler(event, context):
    etl_service = ETLService()
    
    try:
        # Trigger ETL job
        job_run_id = etl_service.trigger_etl_job('CustomerDataETL')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'ETL job triggered successfully',
                'jobRunId': job_run_id
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error triggering ETL job: {str(e)}'
            })
        }