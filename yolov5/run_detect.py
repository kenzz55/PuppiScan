import pathlib
pathlib.PosixPath = pathlib.WindowsPath

import sys
import torch
from pathlib import Path
import os
from PIL import Image
from matplotlib import pyplot as plt

from models.common import DetectMultiBackend
from utils.dataloaders import LoadImages
from utils.general import non_max_suppression, scale_boxes
from utils.torch_utils import select_device
from ultralytics.utils.plotting import Annotator, colors

def detect_disease(image_path: str) -> tuple[str, float | None]:
    """
    YOLOv5를 이용해 이미지에서 질병 감지 후 결과 이미지 저장 및 병명 + confidence 반환.

    :param image_path: 추론할 이미지 경로
    :return: (감지된 병명, confidence score) 튜플
    """

    # 모델 경로
    base_dir = Path(__file__).resolve().parent
    weights_path = base_dir / "best.pt"
    save_path = base_dir.parent / "static" / "result" / "result.jpg"

    device = select_device('cpu')
    model = DetectMultiBackend(weights_path, device=device, dnn=False)
    stride, names, pt = model.stride, model.names, model.pt
    img_size = 640

    dataset = LoadImages(image_path, img_size=img_size, stride=stride, auto=True)
    conf_thres = 0.25
    iou_thres = 0.45

    disease = None
    confidence = None  # 새로 추가

    for path, img, im0s, vid_cap, s in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float() / 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = model(img, augment=False, visualize=False)
        pred = non_max_suppression(pred, conf_thres, iou_thres)

        for det in pred:
            if len(det):
                det = det[det[:, 4].argmax()].unsqueeze(0)
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0s.shape).round()

                for *xyxy, conf, cls in det:
                    label = f'{names[int(cls)]} {conf:.2f}'
                    disease = names[int(cls)]
                    confidence = float(conf.item())  # confidence score 추출

                    annotator = Annotator(im0s, line_width=3)
                    annotator.box_label(xyxy, label, color=(255, 0, 0))
                    im0s = annotator.result()

        os.makedirs(save_path.parent, exist_ok=True)
        Image.fromarray(im0s[:, :, ::-1]).save(save_path)
        print(f"결과 이미지 저장: {save_path}")

    return disease, confidence
