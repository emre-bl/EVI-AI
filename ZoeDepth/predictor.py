import torch
from zoedepth.utils.misc import get_image_from_url, colorize
from PIL import Image
import matplotlib.pyplot as plt
import time

zoe = torch.hub.load(".", "ZoeD_N", source="local", pretrained=True)
img = Image.open("test6.png").convert("RGB")
img_rgb = img.convert('RGB')

start = time.time()
depth = zoe.infer_pil(img_rgb)
end = time.time()
print("Depth map calculated. Time:", end - start, "seconds.")

colored_depth = colorize(depth)
plt.imsave("colored_depth.png", colored_depth)