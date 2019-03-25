from google.cloud import bigquery
import os

def load_gcs2bq(data, context):
    """Cloud Storageに配置されたCSVファイルをもとに、
       BigQueryにテーブルを作成する。

    Args:
        data (dict): Cloud Functionsのイベントペイロード
        context (google.cloud.functions.Context): イベントのメタデータ
    Returns:
        None
    """
    
    # 対象のバケット名・ファイル名を取得
    bucket_name = data['bucket']
    file_name = data['name']
    
    if not file_name.endswith('/'):
        # ロード処理の実行
        
        # ロード対象ファイルのGCSパスを指定
        source_uri = 'gs://{}/{}'.format(bucket_name, file_name)
        
        print('Target File: {}'.format(source_uri))
        
        print('Event ID: {}'.format(context.event_id))
        print('Event type: {}'.format(context.event_type))

        print('Metageneration: {}'.format(data['metageneration']))
        print('Created: {}'.format(data['timeCreated']))
        print('Updated: {}'.format(data['updated']))
        
        client = bigquery.Client()
        
        # ロード先テーブルの指定
        dataset_id = os.environ['DATASET_NAME']
        table_id = os.path.splitext(file_name)[0]
        dataset_ref = client.dataset(dataset_id)
        job_config = bigquery.LoadJobConfig()
        
        # スキーマ自動認識を有効化
        job_config.autodetect = True
        
        # 同じ名前のファイルが更新された場合、スキーマも含めて上書き
        job_config.write_disposition = 'WRITE_TRUNCATE'
        
        # 以下のように列定義を指定することも可能
        # この場合、GCSに配置されたファイルに対応する名前のjsonスキーマファイルを引き当てる等が考えられる
        # job_config.schema = [
        #     bigquery.SchemaField('name', 'STRING'),
        #     bigquery.SchemaField('post_abbr', 'STRING')
        # ]
        
        # ヘッダ行なしのCSV形式に対応
        job_config.skip_leading_rows = 0
        job_config.source_format = bigquery.SourceFormat.CSV
        
        # ロードジョブを実行
        load_job = client.load_table_from_uri(
            source_uri,
            dataset_ref.table(table_id),
            job_config=job_config)  # API request
        print('Starting job {}'.format(load_job.job_id))
        
        # ジョブの完了まで待機
        load_job.result()
        
        print('Job finished.')
        destination_table = client.get_table(dataset_ref.table(table_id))
        print('Loaded {}.{} {} rows.'.format(dataset_id, table_id, destination_table.num_rows))
    
    else:
        # 対象がサブディレクトリ(末尾が/)の場合はロード処理に入らずに終了する
        print('{} is a sub directory'.format(file_name))
    