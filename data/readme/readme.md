# 配布データの説明

動画データやアノテーションと応募用ファイルのフォーマットについて説明する.

## 動画データ

train_videos_1-4.zipを解凍するとtrain_videos, test_videos_1-2.zipを解凍するとtest_videosという名前のディレクトリが生成される. これらのディレクトリには, シーンID("000", "001"など)ごとに切られたディレクトリが含まれており, その配下に下記のデータが格納されている.

- Right.mp4
  - 右カメラ動画像.
  - (横, 縦)=(1000[pix], 420[pix]).
  - fps=10
- Left.mp4
  - 左カメラ動画像.
  - (横, 縦)=(1128[pix], 420[pix]).
  - fps=10
- disparity
  - 各フレームにおける視差情報が入ったrawデータ.
  - ファイル名がフレーム番号(00000000f.raw, 00000001f.raw, ...)となっている.
  - 視差値を変換することで距離情報が得られる.
- disparity_PNG
  - 各フレームにおける視差情報が入った画像データ(PNG形式).
  - ファイル名がフレーム番号(00000000f.png, 00000001f.png, ...)となっている.
  - disparityのモニタ用で、整数視差情報のみが入っている.

詳しくは別途同封してある"動画像データに関する補足.pptx"を参照すること.

## アノテーション

学習用データはtrain_annotations.zip, 評価用データはtest_annotations.zipを解凍すると, それぞれの動画データに対応したシーンのアノテーション情報が入った, シーンID("000", "001"など)を名前としたjsonファイルを格納したディレクトリが作成される(それぞれtrain_annotationsとtest_annotations). フォーマットは以下Discriptionの通り.

- Discription
  - attributes
    - 評価値計算時の重み付加: "有|無"
  - sequence []
    - OwnSpeed
    - StrDeg
    - inf_DP
    - Distance_ref
    - TgtSpeed_ref
    - TgtXPos_LeftUp
    - TgtYPos_LeftUp
    - TgtWidth
    - TgtHeight
- Notes
  - encodingは"utf-8".
  - "attributes"において, "評価値計算時の重み付加"について, "有"の場合は重み3, "無"の場合は重み1とする. 詳細はコンペティションページの評価方法を参照すること.
  - 評価用には"attributes"は含まれない.
  - "sequence"にはフレーム番号順に以下の情報が入っている.
    - OwnSpeed: 自車速度(km/h).
    - StrDeg: ハンドル角(deg). 右にハンドルを切った場合を正.
    - inf_DP: 各フレームの無限遠の視差(pix).
    - Distance_ref: 先行車距離(m).
      - 学習用にのみ存在する.
    - TgtSpeed_ref: 先行車速度(km/h).
      - 学習用にのみ存在する.
    - (TgtXPos_LeftUp, TgtYPos_LeftUp, TgtWidth, TgtHeight): 右カメラ動画像において左上を原点とした矩形座標(左上のX座標, 左上のY座標, 横の長さ, 縦の長さ).
      - 学習用にはすべてのフレームに入っているが, 評価用には最初の1フレーム目にのみ入っている.

## 応募用ファイル

評価用シーン全てに対して各フレームにおける先行車の速度を予測値として格納したjsonファイルを作成する. フォーマットは以下の通り.

- ファイル名
  - {好きな名前}.json
- Discription
  - scene_1 []
  - scene_2 []
  ...
- Notes
  - encodingは"utf-8".
  - 各評価シーンにおいて, 全てのフレームに対してフレーム番号順に先行車の速度を予測値として格納する.
  - 応募用サンプルファイルとして, sample_submit.jsonもあるので, 必要に応じて参照すること.
