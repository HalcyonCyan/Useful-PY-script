import torch
from ultralytics import YOLO
import cv2
import ultralytics
print(f"Ultralytics version: {ultralytics.__version__}")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
#print(f"Ultralytics version: {YOLO.__version__}")
print(f"OpenCV version: {cv2.__version__}")