#!/bin/bash

# コピー先のパス
DEST_DIR="../mc_rtc_ws/install/share/hrpsys/samples/CHIDORI"
# コピーするファイルのパス
SOURCE_FILE="sim_mc_step.cnoid"

# ファイルが存在しない場合にコピーする
if [ ! -f "$DEST_DIR/$SOURCE_FILE" ]; then
    cp "$SOURCE_FILE" "$DEST_DIR"
fi

# copy BaselineWalkingController.yaml
DEST_DIR="/root/.config/mc_rtc/controllers/"
SOURCE_FILE="BaselineWalkingController.yaml"
cp "$SOURCE_FILE" "$DEST_DIR"

# cmake
cd cnoid_spring_customizer/build
make
make install

# userdirに戻る
cd ../..

# 環境変数設定
export SPRING_CUSTOMIZER_ROBOT=step_floor
export SPRING_CUSTOMIZER_CONF_FILE=/userdir/cnoid_spring_customizer/sample/SpringCustomizerSettings.yaml

