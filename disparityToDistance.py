import json

right_image_height = 420
right_image_width = 1000
disparity_image_width = 256

video_no = 0
frame_no = 1

disparity_image_path = './train_videos/%.3d/disparity/%.8df.raw' % (video_no, frame_no)
annotation_path = './train_annotations/%.3d.json' % video_no

with open(disparity_image_path, 'rb') as f:
    disparity_image = f.read()
with open(annotation_path, encoding = 'UTF-8') as f:
    annotation = json.load(f)
inf_DP = annotation['sequence'][frame_no]['inf_DP']
TgtXPos_LeftUp = annotation['sequence'][frame_no]['TgtXPos_LeftUp']
TgtYPos_LeftUp = annotation['sequence'][frame_no]['TgtYPos_LeftUp']
TgtWidth = annotation['sequence'][frame_no]['TgtWidth']
TgtHeight = annotation['sequence'][frame_no]['TgtHeight']
list = []

# 全画素に対して距離を算出
for right_i in range(int(TgtXPos_LeftUp + TgtWidth / 4), int(TgtXPos_LeftUp + TgtWidth / 4 * 3)):
    for right_j in range(int(TgtYPos_LeftUp + TgtHeight / 10 * 2), int(TgtYPos_LeftUp + TgtHeight / 10 * 8)):
        # 右画像座標位置に対応する視差画像座標を求める
        # 視差画像と右画像は原点が左下と左上で違うため上下反転
        disparity_j = int((right_image_height - right_j - 1) / 4) # 縦座標
        disparity_i = int(right_i / 4) # 横座標

        # 視差を読み込む
        # 整数視差読み込み
        disparity_int = disparity_image[(disparity_j * disparity_image_width + disparity_i) * 2]
        # 小数視差読み込み
        disparity_float = disparity_image[(disparity_j * disparity_image_width + disparity_i) * 2 + 1] / 256
        disparity = disparity_int + disparity_float
        # 視差距離へ変換
        if disparity > 0: # disparity = 0 は距離情報がない
            distance = 560 / (disparity - inf_DP)
            if distance > 0:
                list.append(distance)

print('distance = ', sum(list) / len(list))
