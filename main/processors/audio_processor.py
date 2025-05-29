import librosa
import soundfile as sf
import numpy as np
from pydub import AudioSegment
from scipy import signal
import os


#------------------------------------------------------------------#
#                       Audio Processor                           #
#------------------------------------------------------------------#
class AudioProcessor:
    def __init__(self, config):
        self.config = config
        self.audio_params = config.get_audio_params()


    # Réduction du bruit
    def reduce_noise(self, audio_data, sr):
        stft = librosa.stft(audio_data)
        magnitude = np.abs(stft)
        phase = np.angle(stft)
        noise_profile = np.mean(magnitude[:, :int(sr * 0.5)], axis=1, keepdims=True)
        noise_factor = 0.3
        mask = magnitude > (noise_profile * noise_factor)
        cleaned_magnitude = magnitude * mask
        cleaned_stft = cleaned_magnitude * np.exp(1j * phase)
        return librosa.istft(cleaned_stft)


    # Normalisation audio
    def normalize_audio(self, audio_data):
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            return audio_data / max_val * 0.95
        return audio_data


    # Amélioration de la clarté
    def enhance_clarity(self, audio_data, sr):
        nyquist = sr // 2
        low_freq = 300 / nyquist
        high_freq = 3400 / nyquist
        b, a = signal.butter(4, [low_freq, high_freq], btype='band')
        enhanced = signal.filtfilt(b, a, audio_data)
        return audio_data + (enhanced * 0.3)


    # Égalisation audio
    def equalize_audio(self, audio_data, sr):
        stft = librosa.stft(audio_data)
        magnitude = np.abs(stft)
        freqs = librosa.fft_frequencies(sr=sr)
        
        eq_curve = np.ones_like(freqs)
        eq_curve[(freqs >= 100) & (freqs <= 300)] *= 1.1
        eq_curve[(freqs >= 1000) & (freqs <= 4000)] *= 1.2
        eq_curve[(freqs >= 6000) & (freqs <= 12000)] *= 1.15
        
        magnitude_eq = magnitude * eq_curve[:, np.newaxis]
        phase = np.angle(stft)
        stft_eq = magnitude_eq * np.exp(1j * phase)
        return librosa.istft(stft_eq)


    # Suppression des clics et pops
    def remove_clicks(self, audio_data, sr):
        hop_length = 512
        frame_length = 2048
        stft = librosa.stft(audio_data, hop_length=hop_length, n_fft=frame_length)
        magnitude = np.abs(stft)
        
        median_mag = signal.medfilt(magnitude, kernel_size=(1, 5))
        threshold = 2.0
        mask = magnitude < (median_mag * threshold)
        
        cleaned_stft = stft * mask
        return librosa.istft(cleaned_stft, hop_length=hop_length)


    # Amélioration de la dynamique
    def enhance_dynamics(self, audio_data):
        threshold = 0.1
        ratio = 4.0
        attack = 0.003
        release = 0.1
        
        envelope = np.abs(audio_data)
        compressed = np.copy(audio_data)
        
        for i in range(1, len(audio_data)):
            if envelope[i] > threshold:
                reduction = 1 - (envelope[i] - threshold) / ratio
                compressed[i] *= max(reduction, 0.1)
        
        return compressed


    # Traitement principal de l'audio
    def process_audio(self, input_path: str, output_path: str) -> bool:
        try:
            audio_data, sr = librosa.load(input_path, sr=None)
            
            processed = self.reduce_noise(audio_data, sr)
            processed = self.remove_clicks(processed, sr)
            processed = self.enhance_clarity(processed, sr)
            processed = self.equalize_audio(processed, sr)
            processed = self.enhance_dynamics(processed)
            processed = self.normalize_audio(processed)
            
            target_sr = self.audio_params['sample_rate']
            if sr != target_sr:
                processed = librosa.resample(processed, orig_sr=sr, target_sr=target_sr)
            
            sf.write(output_path, processed, target_sr, subtype='PCM_24')
            return True
            
        except Exception as e:
            return False


    # Conversion avec pydub pour formats spéciaux
    def convert_with_pydub(self, input_path: str, output_path: str) -> bool:
        try:
            audio = AudioSegment.from_file(input_path)
            
            audio = audio.normalize()
            audio = audio.compress_dynamic_range(threshold=-20.0, ratio=4.0, attack=5.0, release=50.0)
            audio = audio.high_pass_filter(80)
            audio = audio.low_pass_filter(15000)
            
            bitrate = self.audio_params['bitrate']
            audio.export(output_path, format="mp3", bitrate=bitrate)
            return True
            
        except Exception as e:
            return False


    # Traitement par lot
    def process_batch(self, file_paths: list, output_dir: str) -> dict:
        results = {'success': [], 'failed': []}
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_refined.wav")
            
            if self.process_audio(file_path, output_path):
                results['success'].append(output_path)
            else:
                results['failed'].append(file_path)
        
        return results