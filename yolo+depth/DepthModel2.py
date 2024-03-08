import time
import torch
from PIL import Image, ImageDraw, ImageFont
from misc import colorize
import numpy as np

class DepthEstimationModel:
    def __init__(self) -> None:
        self.device = self._get_device()
        self.model, self.transform = self._initialize_model(
            model_repo="intel-isl/MiDaS", model_name="MiDaS_small"
        )

    def _get_device(self):
        #return "cuda" if torch.cuda.is_available() else "cpu"
        return "cpu"

    def _initialize_model(self, model_repo, model_name):
        # Download the MiDaS
        torch.hub.help("intel-isl/MiDaS", "MiDaS_small")
        model = torch.hub.load(
            model_repo, model_name, pretrained=True, skip_validation=False
        )
        model = model.to(self.device)
        model.eval()
        #input transformational pipeline
        transforms = torch.hub.load(model_repo, "transforms")
        transform = transforms.small_transform
        return model, transform
    
    def save_colored_depth(self, depth_numpy, output_path):
        colored = colorize(depth_numpy)
        image = Image.fromarray(colored)
        image.save(output_path)
        return image

        
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
    

    def calculate_depthmap(self, image):
        # convert image to PIL format
        imagebatch = self.transform(image).to(self.device)

        # make a prediction
        with torch.no_grad():
            depth = self.model(imagebatch)
            depth = torch.nn.functional.interpolate(
                depth.unsqueeze(1),
                size=image.size[::-1],
                mode="bicubic",
                align_corners=False,
            ).squeeze()
        # create a depth map
        depth_map = depth.squeeze().cpu().numpy()
        return depth_map

    def reduce_image_size(self, image): # bunu hızlandırmak için ekledim. silinebilir.
        width, height = image.size
        return image.resize((width // 4, height // 4))
  

    