
# CHIDORI 起動手順

このドキュメントでは、CHIDORIのセットアップおよび起動手順について説明します。

## 1. セットアップ

まず、`setup.bash`を実行して初期設定を行います。これにより、`steo_floor`の地形をChoreonoidに設定します。初回起動時に必ず実行してください。

```bash
source setup.bash
```

## 2. 起動

次に、2つのターミナルを使用して、ChoreonoidとROSの起動を行います。

- **ターミナル1**：`coreonoid_step.bash` を実行してChoreonoidを起動します。
  
```bash
bash coreonoid_step.bash
```

- **ターミナル2**：`roslaunch.bash` を実行してROSを起動します。

```bash
bash roslaunch.bash
```

## 3. パラメータ変更

必要に応じて、`update_param_yaml.py`スクリプトを使用してパラメータを変更します。変更する定数をスクリプト内で編集した後、以下のコマンドでスクリプトを実行してください。

```bash
python update_param_yaml.py
```

## 4. 実行中のパラメータの取得

実行中のパラメータをログに出力する場合は、`make_param_log.py`スクリプトを実行します。出力は`param_log.txt`に保存されます。

```bash
python make_param_log.py
```

出力先：`param_log.txt`

---

以上で、CHIDORIの起動手順は完了です。何か問題があれば適宜設定やスクリプトを見直してください。