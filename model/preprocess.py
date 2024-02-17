import torch
from PIL import Image, ImageOps
import numpy as np

def preprocess_for_yolo(image, input_dim=416):
    """
    Preprocess an image for YOLO model.
    Args:
        image (PIL.Image): The image to preprocess.
        input_dim (int): The input dimension expected by the YOLO model.
    Returns:
        torch.Tensor: The preprocessed image tensor.
    """
    # Resize image with unchanged aspect ratio using padding
    orig_size = image.size
    ratio = float(input_dim) / max(orig_size)
    new_size = tuple([int(x * ratio) for x in orig_size])
    image = image.resize(new_size, Image.ANTIALIAS)
    
    # Add padding to make the image square
    canvas = Image.new('RGB', (input_dim, input_dim), (128, 128, 128))
    canvas.paste(image, ((input_dim - new_size[0]) // 2,
                         (input_dim - new_size[1]) // 2))
    
    # Convert image to tensor and normalize
    image_tensor = torch.FloatTensor(np.array(canvas) / 255.0).permute(2, 0, 1).unsqueeze(0)
    
    return image_tensor


def preprocess_for_monodepth(image, input_size=(640, 192)):
    """
    Preprocess an image for MonoDepth2 model.
    Args:
        image (PIL.Image): The image to preprocess.
        input_size (tuple): The input size expected by the MonoDepth2 model.
    Returns:
        torch.Tensor: The preprocessed image tensor.
    """
    # Resize image to the specified input size
    image = image.resize(input_size, Image.ANTIALIAS)
    
    # Convert image to tensor
    image_tensor = torch.FloatTensor(np.array(image)).permute(2, 0, 1)
    
    # Normalize the image tensor using the mean and standard deviation from the MonoDepth2 training setup
    mean = torch.FloatTensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    std = torch.FloatTensor([0.229, 0.224, 0.225]).view(3, 1, 1)
    image_tensor = (image_tensor / 255.0 - mean) / std
    
    # Add a batch dimension
    image_tensor = image_tensor.unsqueeze(0)
    
    return image_tensor
