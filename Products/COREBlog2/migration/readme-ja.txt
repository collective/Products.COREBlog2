COREBlogからCOREBlog2へ，コンテンツをマイグレーションするためのスクリプト類。

・coreblogexport.dtml.txt
マイグレーションに先立ち，COREBlogからエントリをテキストに書き出すためのDTMLです。

・port.py
テキスト書きだししたファイルを元に，COREBlog2のエントリ，カテゴリ，コメント，トラックバックを再構築するスクリプトです。

・rdf91_xml.dtml.txt
COREBlog上で提供していたRDFを，COREBlog2でも提供したい人向けDTML。portal_skins/custom以下などに設置して利用して下さい。

・rdf10_xml.dtml.txt
同上。

■エクスポート用DTMLの設置

coreblogexport.dtml.txtというテキストもとに，移行元のCOREBlogインスタンスの「コンテンツ(contents)」タブ上にDTML Methodを作ります。これをviewすると，エントリやコメントをテキスト形式で書き出します。
テキストは，エディタなどでエンコードをUTF-8に変換しておいて下さい。

■インポート用スクリプトの設置

Plone上にCOREBlog2インスタンスを作ります。その後，ZMIでportal_skins/customを表示します。ここにport.pyを元に"port"というScript(Python)オブジェクトを設置します。
また，先に書き出されたエクスポートファイルを，同じくportal_skins/custom以下にCOREBlog_Exportという名前でFileオブジェクトとして追加します。

ここまで終わったら，Plone上のCOREBlog2インスタンスをWebブラウザで表示します。URLに続けて"〜/port"というURLにアクセスします。
しばらく待つと，エントリ，コメント，トラックバックが取り込めているはずです。


■注意

カテゴリ名にマルチバイト文字列を使ったカテゴリがあると移行ができません。ASCII文字列(英文)に書き換えた上で，旧COREBlogのエントリをエクスポートして下さい。
画像ファイルや，カスタマイズしたモジュールなどは，手動で移行してください。
