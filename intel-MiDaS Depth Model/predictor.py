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

    def save_colored_depth(self, depth_numpy, output_path):
        colored = colorize(depth_numpy)
        Image.fromarray(colored).save(output_path)
        print("Image saved.")


    #Aşağıdaki kod yapılan testlerime göre doğru çalışıyor. Yaptığı işlem, en yakın nesnenin konumunu bulmak.
    #Eğer nesne soldaysa "Sol", sağdaysa "Sağ", merkezdeyse "İleri" döndürüyor.
    def get_nearest_object_position(self, depth_numpy): 
        min_depth = depth_numpy.min() # Depth haritasındaki en küçük değeri bulun
        min_depth_index = np.where(depth_numpy == min_depth) # En yakın nesnenin konumunu bulmak için minimum derinliğin indeksini alın
        image_width = depth_numpy.shape[1] # Görüntünün genişliğini alın
        image_center_x = image_width // 2 # Görüntünün yatay (x) merkezini hesaplayın
        nearest_object_x = min_depth_index[1][0] # En yakın nesnenin x (yatay) konumunu alın
        
        if nearest_object_x < image_center_x: # Nesnenin konumuna göre göre sol, sağ veya ileri olduğunu belirleyin
            return "Sol"
        elif nearest_object_x > image_center_x:
            return "Sağ"
        else:
            return "İleri"

    def calculate_depthmap(self, image_path, output_path):
        image = Image.open(image_path).convert("RGB")
        print("Image read.")
        image = self.reduce_image_size(image)
        depth_numpy = self.model.infer_pil(image)
        self.save_colored_depth(depth_numpy, output_path)
        print(self.get_nearest_object_position(depth_numpy))
        return f"Image saved to {output_path}."
    
    def reduce_image_size(self, image): # bunu hızlandırmak için ekledim. silinebilir.
        width, height = image.size
        new_width = width // 2
        new_height = height // 2
        return image.resize((new_width, new_height))
    
    def mirror_image(self, image): # get_nearest_object_position fonksiyonunu test etmek için ekledim. 
        return image.transpose(Image.FLIP_LEFT_RIGHT)

    
    
model = DepthEstimationModel()
model.calculate_depthmap("test_image.png", "output.png")
model.calculate_depthmap("test2.png", "output2.png")


#Model ilk çalışırken biraz zaman alıyor. Ancak sonra çok seri okuyup işlem yapıyor.


