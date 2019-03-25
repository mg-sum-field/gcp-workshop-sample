


<!-- 
# デモ2


# サービスアカウントの作成

# Pub/Subのトピックを設定
gcloud pubsub topics create bq-query

# Schedule Queryの設定
Display name: github_commiters_best100
Schedule: every day 11:00
Destination dataset: gcp_demo
Destination table: github_commiters_best100_{run_time|"%Y%m%d"}
Write preference: WRITE_TRUNCATE
Advanced > 
  Cloud Pub/Sub topic: projects/gcp-demo-20190326/topics/bq-query
  Send email notifications: True

# Functionソース配置先GCSバケットを作成

# 出力先GCSバケットを作成
gsutil mb -b on gs://gcp-demo-20190326-output



## リソースの修正
デプロイの前に、テキストエディタでCloud Function資材を修正します。


*  <walkthrough-cloud-shell-editor-icon></walkthrough-cloud-shell-editor-icon>このアイコンをクリックして、エディタを起動します。
*  `gcp-workshop-sample/load_gcs2bq/env.yaml`を開きます。
*  OUTPUT_BUCKET_NAMEの値を、次のように変更します。
```
OUTPUT_BUCKET_NAME : {{project-id}}-output
DATASET_NAME : **<任意のデータセット名>**
```




# Cloud Shellにて資材のデプロイ
cd ~
ls -l
cd gcp-workshop-sample/extract_bq2gcs
gcloud beta functions deploy extract_bq2gcs \
  --runtime python37 \
  --timeout 180s \
  --env-vars-file env.yaml \
  --service-account functions-executor@gcp-demo-20190326.iam.gserviceaccount.com \
  --stage-bucket gcp-demo-20190326-functions \
 --trigger-topic bq-query

# Schedule Queryを手動実行

-->










<!-- 

### Add underlying items to a step

To list items that are part of a tutorial step under a particular step heading, add them as such:

```
### This is an item under your first step
```

The tutorial engine also supports Markdown features like links and images. Note, **including HTML is not supported**.

To recap, a **title** is marked with a **level 1** heading, a **step** with a **level 2** heading, and an **item** with a **level 3** heading.


### Restart to see changes

To see your changes, restart the tutorial by running:
```bash
cloudshell launch-tutorial -d tutorial.md
```

Next up, adding helpful links and icons to your tutorial.


## Special tutorial features

In the Markdown for your tutorial, you may include special directives that are specific to the tutorial engine. These allow you to include helpful shortcuts to actions that you may ask a user to perform.


### Trigger file actions in the text editor
To include a link to <walkthrough-editor-open-file filePath="cloud-shell-tutorials/tutorial.md">open a file for editing</walkthrough-editor-open-file>, use:

```
<walkthrough-editor-open-file
    filePath="cloud-shell-tutorials/tutorial.md">
    open a file for editing
</walkthrough-editor-open-file>
```


### Highlight a UI element

You can also direct the user’s attention to an element on the screen that you want them to interact with.

You may want to show people where to find the web preview icon to view the web server running in their Cloud Shell virtual machine in a new browser tab.

Display the web preview icon <walkthrough-web-preview-icon></walkthrough-web-preview-icon> by including this in your tutorial’s Markdown:

```
<walkthrough-web-preview-icon>
</walkthrough-web-preview-icon>
```

To create a link that shines a <walkthrough-spotlight-pointer spotlightId="devshell-web-preview-button">spotlight on the web preview icon</walkthrough-spotlight-pointer>, add the following:

```
<walkthrough-spotlight-pointer
    spotlightId="devshell-web-preview-button">
    spotlight on the web preview icon
</walkthrough-spotlight-pointer>
```

You can find a list of supported spotlight targets in the [documentation for Cloud Shell Tutorials](https://cloud.google.com/shell/docs/tutorials).

You've now built a tutorial to help onboard users!

Next, you’ll create a button that allows users to launch your tutorial in Cloud Shell.


## Creating a button for your site

Here is how you can create a button for your website, blog, or open source project that will allow users to launch the tutorial you just created.


### Creating an HTML Button

To build a link for the 'Open in Cloud Shell' feature, start with this base HTML and replace the following:

**`YOUR_REPO_URL_HERE`** with the project repository URL that you'd like cloned for your users in their launched Cloud Shell environment.

**`TUTORIAL_FILE.md`** with your tutorial’s Markdown file. The path to the file is relative to the root directory of your project repository.

```
<a  href="https://console.cloud.google.com/cloudshell/open?git_repo=YOUR_REPO_URL_HERE&tutorial=TUTORIAL_FILE.md">
    <img alt="Open in Cloud Shell" src="http://gstatic.com/cloudssh/images/open-btn.png">
</a>
```

Once you've edited the above HTML with the appropriate values for `git_repo` and `tutorial`, use the HTML snippet to generate the 'Open in Cloud Shell' button for your project.


### Creating a Markdown Button

If you are posting the 'Open in Cloud Shell' button in a location that accepts Markdown instead of HTML, use this example instead:

```
[![Open this project in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=YOUR_REPO_URL_HERE&page=editor&tutorial=TUTORIAL_FILE.md)
```

Likewise, once you've replaced `YOUR_REPO_URL_HERE` and `TUTORIAL_FILE.md` in the 'Open in Cloud Shell' URL as described above, the resulting Markdown snippet can be used to create your button.

-->





