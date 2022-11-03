# 動画収集Webアプリケーション

# 1. 概要
　本Webアプリは字幕付き撮影機能が搭載されており、字幕を読み上げてもらった動画をサーバーへとアップロードしてもらいます。
その後、設定したGoogle Driveへと自動で転送、保存を行うアプリケーションとなっている。

# 2. 環境
## [仕様]
- HTML
- CSS
- Javascript
- Python3
- Flask
- Google API
- Heroku (私自身がサーバーとして使用していただけなので、変更も可能)
- Bootstrap
- PostgreSQL
- [ITAコーパス](https://github.com/mmorise/ita-corpus) (文章データ生成に使用)
- Twitter API (文章データ生成に使用)

# 3. 詳細
## [機能一覧]
- ログイン、サインアップのAuth機能
- 字幕付きの動画撮影機能
- Google Driveへのアップロード機能

## [詳細]
　本アプリケーションは自身が卒業研究で用いるためのデータを収集するために開発したアプリケーションである。
各機能の仕様について下記で説明する。

### (Auth機能)
　前提として学内での使用を行っていたため、それにあった仕様になっている。
IDを入力してもらいデータベースに存在しなければ、登録後、ログイン状態にする。また、IDをguestと入力することで、学外の人でも使用できるようになっている。

---
<img src="https://user-images.githubusercontent.com/57441203/199726543-bbb34768-f1c1-4550-9018-5b30867dfda3.PNG" width="20%"><img src="https://user-images.githubusercontent.com/57441203/199733701-0b58d7e1-63ea-4022-87de-ed9057264489.PNG" width="20%"><img src="https://user-images.githubusercontent.com/57441203/199733835-d774037f-d0ce-4713-b856-72b81b336251.PNG" width="20%">


### (字幕付きの録画機能)
　前処理をおこなったテキストデータを文章データとして用い、読み上げてほしい文章の字幕を表示し録画することが可能な機能である。また、録画後は録画内容の確認とダウンロードを行うことができる。

---
<img src="https://user-images.githubusercontent.com/57441203/199732099-5a14103e-4c8b-47be-8224-ea528485f7b4.jpg" width="20%"><img src="https://user-images.githubusercontent.com/57441203/199733099-b88cb4a4-5a9b-4389-8ab9-7991023a83a0.PNG" width="20%">

