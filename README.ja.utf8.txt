Android Log Matcher - logcatの出力を確認するためのPythonモジュール

概要：

    Android Log Matcherを使用すると、文字列もしくは正規表現パターンにマッチする文字列が
    「adb logcat」の出力に現れるかチェックできます。例えば、Activityの起動を確認するために
    「START {act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER]」
    がログに出力されるかどうかを調べるには、以下のように書きます。

        import logmatcher

        logmatcher.start()

        # ... (Activityの起動)

        print logmatcher.wait(
            'START {act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER]')

    この場合、上記の文字列がログに現れた場合、logmatcher.wait()はTrueを返します。

必要なソフトウェア：

    * Android SDK Tools Revision 20以上。 (http://developer.android.com/)

    * 以下のリストの中でどれかひとつ。

        * Python 2.7

        * monkeyrunner

        * Jython 2.5

使い方：

    1. logmatcher.pyを、Android Log Matcherを使用するスクリプトと同じディレクトリに
       入れてください。

    2. そのスクリプトに、logmatcherモジュールをインポートしてください。

        import logmatcher

    3. ログの出力を確認したい処理の直前で、logmatcher.start()を呼び出してください。

    4. ログの出力を確認したい処理のあとで、logmatcher.wait()もしくは
       logmatcher.waitPattern()を呼び出してください。なお、logmatcher.wait()は
       文字列の出力を確認する際に使用し、logmatcher.waitPattern()は正規表現パターンに
       マッチする文字列が出力にあるか確認します。

    5. 4の関数からの出力を確認してください。logmatcher.wait()は、指定の文字列がログに
       見つかればTrueを返します。logmatcher.waitPattern()は、指定の正規表現パターンに
       マッチする文字列がログに見つかれば、Matchオブジェクトを返します。

APIリファレンス：

    logmatcher.start(logcatArgument = u'')

        logcatの監視を開始します。

        引数：

            logcatArgument :
                adb logcatのコマンドライン引数を表す、strもしくはunicode値。

    logmatcher.wait(match, timeout = defaultTimeout)

        指定の文字列がログに現れるまで待機します。

        引数：

            match : ログに現れるまで待機する文字列を表す、str値もしくはunicode値。

            timeout : タイムアウトまでの秒数を表すfloat値。

        戻り値：

            タイムアウトまでに指定の文字列がログに現れればTrue、現れなければFalse。

    logmatcher.waitPattern(pattern, timeout = defaultTimeout)

        指定の正規表現パターンがマッチする文字列がログに現れるまで待機します。

        引数：

            pattern : ログに現れるまで待機する文字列にマッチする、コンパイル済みの
                正規表現パターン、もしくは正規表現パターンを表すstr値かunicode値。

            timeout : タイムアウトまでの秒数を表すfloat値。

        戻り値：

            タイムアウトまでに指定の正規表現パターンにマッチする文字列がログに現れれば
            Matchオブジェクト、現れなければNone。

    logmatcher.defaultTimeout

        タイムアウトまでの秒数を表すfloat値。

        デフォルト値は5（秒）。

ヒント：

    ・正確さと処理速度を確保するために、logcat.startの引数logcatArgumentでlogcatの
      フォーマットの指定をおすすめします。
