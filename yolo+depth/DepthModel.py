import time
import torch
from PIL import Image, ImageDraw, ImageFont
from misc import colorize
import numpy as np
from zoedepth.models.builder import build_model
from zoedepth.utils.config import get_config

class DepthEstimationModel:
    def __init__(self) -> None:
        self.device = self._get_device() 
        self.conf = get_config("zoedepth", "infer", config_version="kitti")
        self.model = build_model(self.conf)    

    def _get_device(self):
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _initialize_model(self, model_repo="isl-org/ZoeDepth", model_name="DPT_BEiT_L_384"):
        model = torch.hub.load(
            model_repo, model_name, source="local", pretrained=True)
        model.eval()
        return model

    def calculate_depthmap(self, image): 
        depth_numpy = self.model.infer_pil(image)
        return depth_numpy
   
  

    