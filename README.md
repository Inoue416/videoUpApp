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
<br />
![home](https://user-images.githubusercontent.com/57441203/199726543-bbb34768-f1c1-4550-9018-5b30867dfda3.PNG)
<img src="https://user-images.githubusercontent.com/57441203/199726543-bbb34768-f1c1-4550-9018-5b30867dfda3.PNG" width=10 height=10>

### (字幕付きの録画機能)

　前処理をおこなったテキストデータを文章データとして用い、
