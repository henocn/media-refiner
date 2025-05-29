import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from skimage import restoration, exposure
import os




#------------------------------------------------------------------#
#                       Image Processor                           #
#------------------------------------------------------------------#
class ImageProcessor:
    def __init__(self, config):
        self.config = config
        self.image_params = config.get_image_params()


    # Amélioration de la netteté
    def enhance_sharpness(self, image):
        if isinstance(image, np.ndarray):
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            return cv2.filter2D(image, -1, kernel)
        else:
            enhancer = ImageEnhance.Sharpness(image)
            return enhancer.enhance(1.5)


    # Réduction du bruit
    def denoise_image(self, image):
        if isinstance(image, np.ndarray):
            return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        else:
            return image.filter(ImageFilter.MedianFilter(size=3))


    # Amélioration du contraste
    def enhance_contrast(self, image):
        if isinstance(image, np.ndarray):
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            enhanced = cv2.merge([l, a, b])
            return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        else:
            enhancer = ImageEnhance.Contrast(image)
            return enhancer.enhance(1.2)


    # Amélioration de la luminosité
    def enhance_brightness(self, image):
        if isinstance(image, np.ndarray):
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv[:,:,2] = cv2.add(hsv[:,:,2], 10)
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        else:
            enhancer = ImageEnhance.Brightness(image)
            return enhancer.enhance(1.1)


    # Amélioration de la saturation
    def enhance_saturation(self, image):
        if isinstance(image, np.ndarray):
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv[:,:,1] = cv2.multiply(hsv[:,:,1], 1.2)
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        else:
            enhancer = ImageEnhance.Color(image)
            return enhancer.enhance(1.15)


    # Upscaling de l'image
    def upscale_image(self, image, scale_factor=2):
        if isinstance(image, np.ndarray):
            height, width = image.shape[:2]
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        else:
            width, height = image.size
            new_size = (int(width * scale_factor), int(height * scale_factor))
            return image.resize(new_size, Image.LANCZOS)


    # Traitement principal de l'image
    def process_image(self, input_path: str, output_path: str) -> bool:
        try:
            image = cv2.imread(input_path)
            if image is None:
                return False
            
            processed = self.denoise_image(image)
            processed = self.enhance_contrast(processed)
            processed = self.enhance_brightness(processed)
            processed = self.enhance_saturation(processed)
            processed = self.enhance_sharpness(processed)
            
            if min(processed.shape[:2]) < 1080:
                scale = 1080 / min(processed.shape[:2])
                if scale <= 3:
                    processed = self.upscale_image(processed, scale)
            
            quality = self.image_params['quality']
            cv2.imwrite(output_path, processed, [cv2.IMWRITE_JPEG_QUALITY, quality])
            return True
            
        except Exception as e:
            return False


    # Traitement par lot
    def process_batch(self, file_paths: list, output_dir: str) -> dict:
        results = {'success': [], 'failed': []}
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_refined{ext}")
            
            if self.process_image(file_path, output_path):
                results['success'].append(output_path)
            else:
                results['failed'].append(file_path)
        
        return results
