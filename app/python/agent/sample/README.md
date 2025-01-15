# サンプルアプリ

## できること



## 実行手順

### 1. リクルートWEBサービス API キーを取得

[リクルートWEBサービス 新規登録ページ](https://webservice.recruit.co.jp/register)にご自身のメールアドレスを入力し、API キーを取得。

※ リクルートWEBサービスは、株式会社リクルート様が保有するデータベースを外部から利用するためのWeb APIを一括提供されているサービスです。[利用規約](https://cdn.p.recruit.co.jp/terms/rws-t-1001/index.html)をお読みいただき、ルールに沿った利用をすることを前提としています。

### 2. Entra ID アプリケーションの作成・権限セット

Entra ID [アプリの登録] からアプリケーション（サービスプリンシパル）を登録し、リソースグループをスコープとして以下の権限をセット。

- Azure AI Developer
- ストレージ BLOB データ共同作成者

### 3. 環境変数を設定

`server/asssitant_manager_sample`ディレクトリに`.env`ファイルを作成し、`.env.sample`の内容をコピーし、それぞれの値をセット。

### 4. ローカル実行

サーバーを起動。

```
cd ./server/assistant_manager_sample
docker build -t agent:0.0.1 .
docker run -p 8000:8000 agent:0.0.1
```

クライアント (`./client/test.http`) からリクエストを実行。