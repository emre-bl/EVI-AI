import torch
from PIL import Image

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
        print("Model initialized.")
        return model
    
    """
    def _mask_and_save_nearest_object(self, depth_numpy, output_path = "output.png"):
    
        min_depth = depth_numpy.min()
        min_depth_index = np.where(depth_numpy == min_depth)
        min_depth_x, min_depth_y = min_depth_index[1][0], min_depth_index[0][0]

        # Flood fill algorithm to segment the nearest object (optional)
        if hasattr(self, "flood_fill"):  # Check if user-defined flood fill exists
            depth_numpy = self.flood_fill(depth_numpy, min_depth_x, min_depth_y)

        # Create a binary mask where only values close to the minimum depth are kept
        threshold = 0.2
        mask = np.zeros_like(depth_numpy)
        mask[depth_numpy >= min_depth - threshold] = 1

        # Apply the mask to the depth map
        masked_depth = depth_numpy * mask

        # Convert to binary image (255 for nearest object, 0 for background)
        binary_image = (masked_depth * 255).astype(np.uint8)

        # Save the binary image
        Image.fromarray(binary_image, mode="L").save(output_path)
        print(f"Image saved to {output_path}.")
    """
    

    def save_colored_depth(self, depth_numpy, output_path):
        colored = colorize(depth_numpy)
        Image.fromarray(colored).save(output_path)
        print("Image saved.")


    def get_nearest_object_position(self, depth_numpy): 
        min_depth = depth_numpy.min() # Depth haritasındaki en küçük değeri bulun
        
        min_depth_index = np.where(depth_numpy == min_depth) # En yakın nesnenin konumunu bulmak için minimum derinliğin indeksini alın
        print(f"Min depth: {min_depth}")
        print(f"Min depth index x: {min_depth_index[1][0]}, y: {min_depth_index[0][0]}")
        
        threshold = 0.05

        depth_numpy[depth_numpy < min_depth + threshold] = 0 # En yakın nesnenin etrafındaki küçük değerleri sıfırlayın

        self.save_colored_depth(depth_numpy, "outputtest.png") # Derinlik haritasını kaydedin

        image_width = depth_numpy.shape[1] # Görüntünün genişliğini alın
        image_center_x = image_width // 2 # Görüntünün yatay (x) merkezini hesaplayın
        nearest_object_x = min_depth_index[1][0] # En yakın nesnenin x (yatay) konumunu alın
        
        quarter = image_width // 4 # Görüntünün genişliğinin dörtte birini hesaplayın

        if nearest_object_x < image_center_x - quarter: # Nesnenin konumuna göre sol, hafif sol, karşı, hafif sağ veya sağ olduğunu belirleyin
            return "Sol"
        elif nearest_object_x < image_center_x:
            return "Hafif Sol"
        elif nearest_object_x > image_center_x + quarter:
            return "Sağ"
        elif nearest_object_x > image_center_x:
            return "Hafif Sağ"
        else:
            return "Karşı"

    

    def calculate_depthmap(self, image_path, output_path):
        image = Image.open(image_path).convert("RGB")
        print("Image read.")
        image = self.reduce_image_size(image)
        depth_numpy = self.model.infer_pil(image)
        depth_numpy = (depth_numpy - depth_numpy.min()) / (depth_numpy.max() - depth_numpy.min())
        depth_numpy = depth_numpy[0:(4*depth_numpy.shape[0]//5), :] # image'in alt kısmını kesmek için
        self.save_colored_depth(depth_numpy, output_path)
        print(self.get_nearest_object_position(depth_numpy))
        self._mask_and_save_nearest_object(depth_numpy, "output_masked.png")
        print("Depth map calculated and saved.")
    
    def reduce_image_size(self, image): # bunu hızlandırmak için ekledim. silinebilir.
        width, height = image.size
        new_width = width // 2
        new_height = height // 2
        return image.resize((new_width, new_height))
    
    def mirror_image(self, image): # get_nearest_object_position fonksiyonunu test etmek için ekledim. 
        return image.transpose(Image.FLIP_LEFT_RIGHT)

    
    
model = DepthEstimationModel()
model.calculate_depthmap("test5.png", "output5.png")


#Model ilk çalışırken biraz zaman alıyor. Ancak sonra çok seri okuyup işlem yapıyor.


