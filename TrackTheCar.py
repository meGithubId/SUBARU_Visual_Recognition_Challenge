import os
import cv2
import json
import numpy as np

def obtainTgts(annotation_path):

    TgtXPos_LeftUp = int(annotation['sequence'][0]['TgtXPos_LeftUp'])
    TgtYPos_LeftUp = int(annotation['sequence'][0]['TgtYPos_LeftUp'])
    TgtWidth = int(annotation['sequence'][0]['TgtWidth'])
    TgtHeight = int(annotation['sequence'][0]['TgtHeight'])

    tracker = cv2.TrackerCSRT_create()
    video = cv2.VideoCapture(video_path)
    ok, frame = video.read()

    bbox = (TgtXPos_LeftUp, TgtYPos_LeftUp, TgtWidth, TgtHeight)

    ok = tracker.init(frame, bbox)

    list_tgt = []
    dict = {"TgtXPos_LeftUp": TgtXPos_LeftUp, "TgtYPos_LeftUp": TgtYPos_LeftUp, "TgtWidth": TgtWidth, "TgtHeight": TgtHeight}
    list_tgt.append(dict)
    while True:
        ok, frame = video.read()
        if not ok:
            break
        ok, bbox = tracker.update(frame)
        if ok:
            (x, y, w, h) = [int(v) for v in bbox]
            dict = {"TgtXPos_LeftUp": x, "TgtYPos_LeftUp": y, "TgtWidth": w, "TgtHeight": h}
            list_tgt.append(dict)
            # cv2.rectangle(frame, (x, y), (x+w, y+ h), (0,255,0), 2, 1)
        else:
            cv2.putText(frame, 'Error', (100, 0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        # cv2.imshow('Tracking', frame)
        if cv2.waitKey(1) & 0XFF == 27:
            break
    cv2.destroyAllWindows()
    return list_tgt


def obtainJson(list_tgt):
    num_frame = len(annotation['sequence'])
    for frame in range(num_frame):
        annotation['sequence'][frame].update(list_tgt[frame])
    with open(transfer_path, 'w', encoding = 'utf-8') as file:
        json.dump(annotation, file, ensure_ascii = False)
    return annotation

def disparityToDistance(annotation):
    num_frame = len(annotation['sequence'])
    for frame in range(num_frame):
        disparity_image_path = './test_videos/%.3d/disparity/%.8df.raw' % (video_no, frame)
        with open(disparity_image_path, 'rb') as f:
            disparity_image = f.read()
        inf_DP = annotation['sequence'][frame]['inf_DP']
        TgtXPos_LeftUp = annotation['sequence'][frame]['TgtXPos_LeftUp']
        TgtYPos_LeftUp = annotation['sequence'][frame]['TgtYPos_LeftUp']
        TgtWidth = annotation['sequence'][frame]['TgtWidth']
        TgtHeight = annotation['sequence'][frame]['TgtHeight']
        list = []

        # 全画素に対して距離を算出
        for right_i in range(int(TgtXPos_LeftUp + TgtWidth / 10 * 3), int(TgtXPos_LeftUp + TgtWidth / 10 * 7)):
            for right_j in range(int(TgtYPos_LeftUp + TgtHeight / 10 * 3), int(TgtYPos_LeftUp + TgtHeight / 10 * 7)):
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

        distance_ref = sum(list) / len(list)
        dict_dis = {"Distance_ref": distance_ref}
        annotation['sequence'][frame].update(dict_dis)
    with open(new_path, 'w', encoding = 'utf-8') as file:
        json.dump(annotation, file, ensure_ascii = False)


if __name__ == '__main__':
    right_image_height = 420
    right_image_width = 1000
    disparity_image_width = 256

    for video_no in range(0, 241):
        video_path = './test_videos/%.3d/Right.mp4' % video_no
        annotation_path = './test_annotations/%.3d.json' % video_no
        transfer_path = './test_annotations_transfer/%.3d.json' % video_no
        new_path = './test_annotations_new/%.3d.json' % video_no
        with open(annotation_path, encoding = 'UTF-8') as f:
            annotation = json.load(f)

        list_tgt = obtainTgts(annotation_path)
        annotation = obtainJson(list_tgt)
        disparityToDistance(annotation)
