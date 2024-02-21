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
        print("Model initialized.")
        return model
    

    def save_colored_depth(self, depth_numpy, output_path):
        # Derinlik haritasını renklendir
        colored = colorize(depth_numpy)
        image = Image.fromarray(colored)

        # ImageDraw ve ImageFont objelerini oluştur
        draw = ImageDraw.Draw(image)

        try:
            # Daha büyük ve özel bir font kullan (örneğin 20 piksel boyutunda)
            font = ImageFont.truetype("arial.ttf", 20)  # Sisteminizdeki bir font dosyasını kullanabilirsiniz
        except IOError:
            # Belirtilen font bulunamazsa veya yüklenemezse varsayılan fontu kullan
            font = ImageFont.load_default()

        # Derinlik değerlerini eşit aralıklarla işaretle
        intervals = np.linspace(0, depth_numpy.size, 33, endpoint=False, dtype=int)  # 32 eşit aralık
        for i in range(1, len(intervals)):
            start_index = intervals[i-1]
            end_index = intervals[i]
            middle_index = (start_index + end_index) // 2

            # Düz 1D dizine dönüştür ve orta indeksi hesapla
            flat_index = np.unravel_index(middle_index, depth_numpy.shape)
            depth_value = depth_numpy[flat_index]

            # Derinlik değerini yazdır
            draw.text((flat_index[1], flat_index[0]), f"{depth_value:.2f}", fill="white", font=font)

        # İşaretlenmiş görüntüyü kaydet
        image.save(output_path)

    def get_nearest_object_position(self, depth_numpy): 
        min_depth = depth_numpy.min() # Depth haritasındaki en küçük değeri bulun
        print("Min depth  : " , min_depth)
        print("Max depth  : " , depth_numpy.max())
        
        min_depth_index = np.where(depth_numpy == min_depth) # En yakın nesnenin konumunu bulmak için minimum derinliğin indeksini alın
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
    

    def calculate_depthmap(self, image_path, output_path):
        print("Device:", self.device)
        print("Calculating depth map for", image_path, "...")
        
        image = Image.open(image_path).convert("RGB")
        image = self.make_image_3_4(image)
        image = self.reduce_image_size(image)
        
        start = time.time()
        depth_numpy = self.model.infer_pil(image)
        end = time.time()
        print("Depth map calculated. Time:", end - start, "seconds.")
        self.save_colored_depth(depth_numpy, output_path)
        print(self.get_nearest_object_position(depth_numpy))

    def reduce_image_size(self, image): # bunu hızlandırmak için ekledim. silinebilir.
        width, height = image.size
        return image.resize((width // 4, height // 4))
    
    def mirror_image(self, image): # get_nearest_object_position fonksiyonunu test etmek için ekledim. 
        return image.transpose(Image.FLIP_LEFT_RIGHT)

    
    
model = DepthEstimationModel()
for i in range(1,5):
    model.calculate_depthmap(f"test_images/test{i}.png", f"outputs/{i}_depth.png")
    print("------------------------------------------------------")


#Model ilk çalışırken biraz zaman alıyor. Ancak sonra çok seri okuyup işlem yapıyor.


