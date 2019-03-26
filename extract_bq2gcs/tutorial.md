# Cloud Functions (Cloud Storageトリガー) のチュートリアル

## 概要

Cloud Storage(以下GCS)にファイルを追加または更新することで起動する関数を作成し、GCSトリガーによるCloud Functionsの使用方法を学びます。

**所要時間**: 約 15 分

**次へ** ボタンを押し、チュートリアルを進めてください。


## プロジェクトの選択
関数を作成するプロジェクトを選択してください。
<walkthrough-project-billing-setup permissions="cloudfunctions.functions.create"></walkthrough-project-billing-setup>


## サービスアカウントの作成

Cloud Functionsにて関数を実行するためのサービスアカウントを作成します。

サービスアカウントの作成には、以下のコマンドを実行します:
```bash
gcloud iam service-accounts create \
  functions-executor \
  --display-name "functions-executor"
```
※右側のコピーボタンを押すと、直接Cloud Shellに貼り付けられます。


## サービスアカウントへの権限付与

functions-executor@{{project-id}}.iam.gserviceaccount.com に必要な権限を付与します。

必要な権限は以下の5つです。

*  BigQueryデータオーナー
*  BigQueryジョブユーザー
*  Cloud Function閲覧者
*  ログ書き込み
*  ストレージのオブジェクト管理者

[IAMと管理](https://console.cloud.google.com/iam-admin/iam?project={{project-id}})を開き、

functions-executor@{{project-id}}.iam.gserviceaccount.com を追加して

上記の権限を付与してください。


## Cloud Functionの関数デプロイ先となるGCSバケットを作成

バケットの作成には、以下のコマンドを実行します:
```bash
gsutil mb -b on gs://{{project-id}}-functions
```


## BigQueryからファイルを出力する先となるGCSバケットを作成

バケットの作成には、以下のコマンドを実行します:
```bash
gsutil mb -b on gs://{{project-id}}-output
```
今回作成する関数により、このバケットにファイルが作成されます。


## Pub/Subのトピックを設定
以下のコマンドを実行し、トピックを作成します:
```bash
gcloud pubsub topics create bq-query
```


## BigQueryデータセットの作成
以下のコマンドを実行し、データセットを作成します:
```bash
bq mk -d <任意のデータセット名>
```


## Schedule Queryの設定 - 1
* github_commiters_best100.sqlを開き、中のSELECT文をコピーします。
<walkthrough-editor-open-file filePath="github_commiters_best100.sql" text="サンプルSQLを開く">
</walkthrough-editor-open-file>
* [BigQuery旧UI](https://bigquery.cloud.google.com/scheduledqueries/{{project-id}})を開きます。
* **COMPOSE QUERY**をクリックし、入力欄にSELECT文を貼り付けます。


## Schedule Queryの設定 - 2
* ** Schedule Query** を押します。
* 追加された入力欄を以下のように設定します。
```
Display name: github_commiters_best100  
Schedule: every day 11:00  
Destination dataset: <作成したデータセット名>
Destination table: github_commiters_best100_{run_time|"%Y%m%d"}
Write preference: WRITE_TRUNCATE
Advanced > 
  Cloud Pub/Sub topic: projects/{{project-id}}/topics/bq-query
  Send email notifications: True
```
* **Add**を押します。


## リソースの修正
デプロイの前に、テキストエディタで環境変数ファイルを修正します。
<walkthrough-editor-open-file filePath="gcp-workshop-sample/extract_bq2gcs/env.yaml" text="env.yamlを開く">
</walkthrough-editor-open-file>
*  OUTPUT_BUCKET_NAMEの値を、次のように変更します。
```
OUTPUT_BUCKET_NAME : {{project-id}}-output
```


## リソースのデプロイ

関数をデプロイするため、以下のコマンドを実行します:
```bash
cd ~
ls -l
cd gcp-workshop-sample/extract_bq2gcs
gcloud beta functions deploy extract_bq2gcs \
  --runtime python37 \
  --timeout 180s \
  --env-vars-file env.yaml \
  --service-account functions-executor@g{{project-id}}.iam.gserviceaccount.com \
  --stage-bucket {{project-id}}-functions \
 --trigger-topic bq-query
```


## Schedule Queryを手動実行
先ほどデプロイした関数の動作を確認するため、Schedule Queryを実行します。
* [BigQuery旧UI](https://bigquery.cloud.google.com/scheduledqueries/{{project-id}})で、先ほど作成したSchedule Queryを選びます。
* **Start manual runs**を押します。
* マークが緑に変わったら実行完了です。


## 結果の確認
以下のコマンドを実行し、ファイルが作成されていることを確認します。
```bash
gsutil ls ./sample.csv gs://{{project-id}}-output/
```


## チュートリアル完了

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

関数が動いたことを確認したら、このチュートリアルは完了です。
