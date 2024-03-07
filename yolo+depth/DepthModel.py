import time
import torch
from PIL import Image, ImageDraw, ImageFont
from misc import colorize
import numpy as np

class DepthEstimationModel:
    def __init__(self) -> None:
        self.device = self._get_device()
        self.model = self._initialize_model(
            model_repo="isl-org/ZoeDepth", model_name="ZoeD_N"
        ).to(self.device)

    def _get_device(self):
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _initialize_model(self, model_repo="isl-org/ZoeDepth", model_name="ZoeD_N"):
        torch.hub.help("intel-isl/MiDaS", "DPT_BEiT_L_384", force_reload=True)
        model = torch.hub.load(
            model_repo, model_name, pretrained=True, skip_validation=False
        )
        model.eval()
        return model
    
    def save_colored_depth(self, depth_numpy, output_path):
        colored = colorize(depth_numpy)
        image = Image.fromarray(colored)
        image.save(output_path)

        
    def make_image_3_4(self, image):
        width, height = image.size
        if width > height:
            new_width = 4 * height // 3
            left = (width - new_width) // 2
            right = width - left
            image = image.crop((left, 0, right, height))
        else:
            new_height = 3 * width // 4
            top = (height - new_height) // 2
            bottom = height - top
            image = image.crop((0, top, width, bottom))
        return image
    

    def calculate_depthmap(self, pil_image, output_path): 
        image = pil_image.convert("RGB")
        image = self.make_image_3_4(image)
        depth_numpy = self.model.infer_pil(image)
        self.save_colored_depth(depth_numpy, output_path)
        return depth_numpy

    def reduce_image_size(self, image): # bunu hızlandırmak için ekledim. silinebilir.
        width, height = image.size
        return image.resize((width // 4, height // 4))
  

    