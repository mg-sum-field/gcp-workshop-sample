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


## BigQueryにロードするファイルの置き場となるGCSバケットを作成

バケットの作成には、以下のコマンドを実行します:
```bash
gsutil mb -b on gs://{{project-id}}-input
```
このバケットが、今回作成する関数のトリガーとなります。


## BigQueryデータセットの作成
以下のコマンドを実行し、データセットを作成します:
```bash
bq mk -d <任意のデータセット名>
```


## リソースの修正
デプロイの前に、テキストエディタで環境変数ファイルを修正します。
*  <walkthrough-cloud-shell-editor-icon></walkthrough-cloud-shell-editor-icon>このアイコンをクリックして、エディタを起動します。
*  `gcp-workshop-sample/load_gcs2bq/env.yaml`を開きます。
*  DATASET_NAMEの値を、次のように変更します。
```
DATASET_NAME : <作成したデータセット名>
```


## リソースのデプロイ

関数をデプロイするため、以下のコマンドを実行します:
```bash
cd ~
cd gcp-workshop-sample/load_gcs2bq
gcloud beta functions deploy load_gcs2bq \
  --runtime python37 \
  --timeout 180s \
  --env-vars-file env.yaml \
  --service-account functions-executor@{{project-id}}.iam.gserviceaccount.com \
  --stage-bucket {{project-id}}-functions \
  --trigger-bucket {{project-id}}-input
```


## 関数の実行

先ほどデプロイした関数の動作を確認するため、以下のコマンドを実行してGCSにファイルを配置します:
```bash
gsutil cp ./sample.csv gs://{{project-id}}-input/
```

## 結果の確認
[BigQueryコンソール](https://console.cloud.google.com/bigquery?project={{project-id}})を開き、  
env.yamlで指定したデータセットの中に  
**sample**というテーブルが作成されていることを確認してください。



## チュートリアル完了

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

関数が動いたことを確認したら、このチュートリアルは完了です。
