# NPMIによる再帰型フレーズ認識
1. 連続する2つの形態素について、フレーズらしさをNPMIによって判定する
2. フレーズ認識した形態素列と、その１つあとの形態素について1.と同様にフレーズ判定する
3. 2.を再帰的に繰り返す。NPMIの閾値(0.5)を超えるフレーズが検出できなくなったら再帰を終了

実装
[pmi_recursive_bow.py](pmi_recursive_bow.py)
インスタンス：PMI = pmi_recursive_bow.pmi(データ中の総形態素数)
フレーズ認識の実行：n_grams_bow,n_gramed_phrases_byn = PMI.exec_pmi(n_gram,bow_unigrams)
- n_gram:フレーズ認識したい形態素数のスタート値（１で固定でOK）
- bow_unigrams：形態素解析済の文書（1行1データの2次元配列）
- n_grams_bow：再帰フレーズ認識終了時点でのフレーズ化した文書（bow_unigramsの各行を最大フレーズで認識したもの　スペース区切り）
- n_gramed_phrases_byn：再帰の回数毎（n_gram毎）に認識されたフレーズ集
- 69行目のnpmi閾値を大きくするとフレーズ認識の再帰回数が制限的になる

実行の手順
[test_pmi_bow.py](test_pmi_bow.py)
このプログラムに読み込むcsvを変えると、pmi_recursive_bow.pyを実行して、結果をcsvに書き出す。
1. データの読み込み
- 45行目:csvファイル名を変更
- 46行目:読み込んだcsvでフレーズ認識したいデータのcolumn名
2. データの書き出し
- 67行目:再帰毎のフレーズ一覧を書き出す（レイアウトは、npmi_bow.csvを参照）
- 77行目:1.で読んだcsvの最終列に、フレーズ認識した単語列をスペース区切りで連結したファイルを書き出す（レイアウトは、tsukurepo_npmi_phrased.csvを参照）
- もし、max gramでのフレーズではないフレーズ認識をしたい場合は、npmi_bow.csvを辞書として参照する

