import base64
import json
import datetime
import os
from google.cloud import bigquery

def extract_bq2gcs(data, context):
    """BigQuery上のスケジュールクエリにより送られたPub/Subメッセージをトリガーにして、
       対象テーブルの中身をGCSにファイルとして出力する。
    Args:
         data (dict): Cloud Functionsのイベントペイロード
         context (google.cloud.functions.Context): イベントのメタデータ
    Returns:
        None
    """
    # 出力処理の実行
    
    # json形式のメッセージをパース
    message_dict = json.loads(base64.b64decode(data['data']).decode('utf-8'))
    
    bucket_name = os.environ['OUTPUT_BUCKET_NAME']
    dataset_id = message_dict['destinationDatasetId']
    
    # 日付のsuffixを置き換えてテーブル名とする
    table_name_template = message_dict['params']['destination_table_name_template']
    execution_date = datetime.datetime.fromisoformat(
            message_dict['runTime'].replace('Z', '')
            ).strftime('%Y%m%d')
    table_id = table_name_template.replace('{run_time|"%Y%m%d"}',execution_date)
    
    query_result = message_dict['state']
    if query_result == 'SUCCEEDED':
        print('Exporting {}.{}...'.format(dataset_id, table_id))
        client = bigquery.Client()
        destination_uri = 'gs://{}/{}.csv'.format(bucket_name, table_id)
        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        
        # 出力ジョブを実行
        extract_job = client.extract_table(
            table_ref,
            destination_uri,
            # Location must match that of the source table.
            location='US')  # API request
            
        # ジョブの完了まで待機
        extract_job.result()
        
        print('Exported {}.{} to {}'.format(
            dataset_id, table_id, destination_uri))
        
    else:
        query_name = message_dict['name']
        print('The Query {} failed.'.format(query_name))