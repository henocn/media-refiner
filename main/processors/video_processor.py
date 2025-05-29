import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
import ffmpeg
import os
import tempfile


#------------------------------------------------------------------#
#                       Video Processor                           #
#------------------------------------------------------------------#
class VideoProcessor:
    def __init__(self, config):
        self.config = config
        self.video_params = config.get_video_params()
        self.audio_params = config.get_audio_params()


    # Amélioration de la netteté vidéo
    def enhance_frame_sharpness(self, frame):
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        return cv2.filter2D(frame, -1, kernel)


    # Réduction du bruit vidéo
    def denoise_frame(self, frame):
        return cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)


    # Amélioration du contraste
    def enhance_frame_contrast(self, frame):
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)


    # Stabilisation vidéo
    def stabilize_frame(self, frame, prev_frame, transform_params):
        if prev_frame is None:
            return frame, None
        
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30, blockSize=3)
        
        if prev_pts is not None:
            curr_pts, status, error = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None)
            
            if curr_pts is not None:
                idx = np.where(status == 1)[0]
                prev_pts = prev_pts[idx]
                curr_pts = curr_pts[idx]
                
                if len(prev_pts) > 10:
                    transform = cv2.estimateAffinePartial2D(prev_pts, curr_pts)[0]
                    if transform is not None:
                        stabilized = cv2.warpAffine(frame, transform, (frame.shape[1], frame.shape[0]))
                        return stabilized, transform
        
        return frame, None


    # Upscaling vidéo
    def upscale_frame(self, frame, target_width, target_height):
        return cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_CUBIC)


    # Amélioration de la saturation
    def enhance_frame_saturation(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = cv2.multiply(hsv[:,:,1], 1.2)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


    # Traitement d'une frame
    def process_frame(self, frame, prev_frame=None):
        processed = self.denoise_frame(frame)
        processed = self.enhance_frame_contrast(processed)
        processed = self.enhance_frame_saturation(processed)
        processed = self.enhance_frame_sharpness(processed)
        
        target_width = self.video_params['width']
        target_height = self.video_params['height']
        
        if processed.shape[1] < target_width or processed.shape[0] < target_height:
            processed = self.upscale_frame(processed, target_width, target_height)
        
        stabilized, transform = self.stabilize_frame(processed, prev_frame, None)
        return stabilized


    # Traitement vidéo avec OpenCV
    def process_video_opencv(self, input_path: str, output_path: str) -> bool:
        try:
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(self.video_params['width'])
            height = int(self.video_params['height'])
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            prev_frame = None
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                processed_frame = self.process_frame(frame, prev_frame)
                out.write(processed_frame)
                prev_frame = frame
                frame_count += 1
            
            cap.release()
            out.release()
            return True
            
        except Exception as e:
            return False


    # Traitement avec FFmpeg
    def process_video_ffmpeg(self, input_path: str, output_path: str) -> bool:
        try:
            temp_video = os.path.join(self.config.temp_dir, 'temp_video.mp4')
            
            stream = ffmpeg.input(input_path)
            video = stream.video.filter('scale', self.video_params['width'], self.video_params['height'])
            video = video.filter('unsharp', '5:5:1.0:5:5:0.0')
            video = video.filter('eq', contrast=1.1, brightness=0.05, saturation=1.1)
            audio = stream.audio.filter('highpass', f=80).filter('lowpass', f=15000)
            
            out = ffmpeg.output(video, audio, output_path, 
                              vcodec='libx264', 
                              acodec='aac',
                              video_bitrate=self.video_params['bitrate'],
                              audio_bitrate=self.audio_params['bitrate'])
            
            ffmpeg.run(out, overwrite_output=True, quiet=True)
            return True
            
        except Exception as e:
            return False


    # Traitement avec MoviePy
    def process_video_moviepy(self, input_path: str, output_path: str) -> bool:
        try:
            clip = VideoFileClip(input_path)
            
            def enhance_frame(get_frame, t):
                frame = get_frame(t)
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                processed = self.process_frame(frame_bgr)
                return cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
            
            enhanced_clip = clip.fl(enhance_frame)
            
            enhanced_clip.write_videofile(output_path, 
                                        codec='libx264',
                                        bitrate=self.video_params['bitrate'],
                                        audio_codec='aac')
            
            clip.close()
            enhanced_clip.close()
            return True
            
        except Exception as e:
            return False


    # Traitement principal
    def process_video(self, input_path: str, output_path: str) -> bool:
        if self.process_video_ffmpeg(input_path, output_path):
            return True
        elif self.process_video_moviepy(input_path, output_path):
            return True
        else:
            return self.process_video_opencv(input_path, output_path)


    # Traitement par lot
    def process_batch(self, file_paths: list, output_dir: str) -> dict:
        results = {'success': [], 'failed': []}
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_refined.mp4")
            
            if self.process_video(file_path, output_path):
                results['success'].append(output_path)
            else:
                results['failed'].append(file_path)
        
        return results
