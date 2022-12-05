from lines import *
from convert import *
from crop_roi import crop_area
from interpolation import interpolate
import cv2
import numpy as np
import time
from Frame import Frame
from Instance import Instance
from setup_project import setup_project
from export import create_packet_map
from diffgram import Project
from process_video import process_video

video_path = r'C:\Users\79042\Downloads\видео\test.mp4'
annotation_path = r'C:\Users\79042\Downloads\diffgram_annotation.json'

process_video(video_path, annotation_path, 197, debag=False)
