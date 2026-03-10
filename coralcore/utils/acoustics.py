# 🪸 CORAL-CORE Acoustics Utilities
# Acoustic processing utilities for reef soundscapes
# Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""
Acoustics Utilities
===================

Utilities for processing and analyzing acoustic reef signatures,
including spectral analysis, feature extraction, and soundscape metrics.

Reference: Gordon, T.A.C. et al. (2019). Nature Communications, 10, 5414.
"""

# تم إزالة numpy
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from scipy import signal, ndimage
import warnings

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    warnings.warn("librosa not installed. Some acoustic functions will be limited.")

# =============================================================================
# CONSTANTS
# =============================================================================

# Default audio parameters
DEFAULT_SR = 96000  # Hz (CORAL-CORE standard)
DEFAULT_N_FFT = 4096
DEFAULT_HOP_LENGTH = 1024

# Frequency bands (Hz)
FREQUENCY_BANDS = {
    'very_low': (20, 100),
    'low': (100, 400),
    'fish_chorus': (400, 800),
    'fish_extended': (800, 2000),
    'invertebrate': (800, 2000),
    'snapping_shrimp': (2000, 5000),
    'shrimp_extended': (5000, 20000),
    'ultrasonic': (20000, 48000)
}

# Acoustic indices
ACOUSTIC_INDICES = {
    'aci': 'Acoustic Complexity Index',
    'bi': 'Biodiversity Index',
    'ndsi': 'Normalized Difference Soundscape Index',
    'aei': 'Acoustic Entropy Index',
    'shannon': 'Shannon Entropy',
    'spectral_centroid': 'Spectral Centroid',
    'spectral_bandwidth': 'Spectral Bandwidth',
    'zero_crossing_rate': 'Zero Crossing Rate'
}


@dataclass
class AcousticFeatures:
    """Container for extracted acoustic features"""
    
    shannon_entropy: float
    spectral_centroid: float
    spectral_bandwidth: float
    zero_crossing_rate: float
    aci: float  # Acoustic Complexity Index
    bi: float  # Biodiversity Index
    ndsi: float  # Normalized Difference Soundscape Index
    band_powers: Dict[str, float]
    mfccs: np.ndarray
    spectrogram: np.ndarray
    frequencies: np.ndarray
    times: np.ndarray


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def load_audio(
    file_path: str,
    sr: int = DEFAULT_SR,
    mono: bool = True,
    duration: Optional[float] = None
) -> Tuple[np.ndarray, int]:
    """
    Load audio file.
    
    Parameters
    ----------
    file_path : str
        Path to audio file
    sr : int
        Target sampling rate
    mono : bool
        Convert to mono
    duration : float, optional
        Load only first N seconds
    
    Returns
    -------
    tuple
        (audio, sampling_rate)
    """
    if not LIBROSA_AVAILABLE:
        raise ImportError("librosa is required for audio loading")
    
    audio, sr = librosa.load(
        file_path,
        sr=sr,
        mono=mono,
        duration=duration,
        res_type='kaiser_fast'
    )
    
    return audio, sr


def compute_spectrogram(
    audio: np.ndarray,
    sr: int = DEFAULT_SR,
    n_fft: int = DEFAULT_N_FFT,
    hop_length: int = DEFAULT_HOP_LENGTH,
    window: str = 'hann'
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute spectrogram of audio signal.
    
    Parameters
    ----------
    audio : np.ndarray
        Audio time series
    sr : int
        Sampling rate
    n_fft : int
        FFT window size
    hop_length : int
        Hop length between frames
    window : str
        Window type
    
    Returns
    -------
    tuple
        (spectrogram, frequencies, times)
    """
    if not LIBROSA_AVAILABLE:
        raise ImportError("librosa is required for spectrogram computation")
    
    # Compute STFT
    D = librosa.stft(
        audio,
        n_fft=n_fft,
        hop_length=hop_length,
        window=window
    )
    
    # Convert to power spectrogram (dB)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    
    # Get frequencies and times
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    times = librosa.frames_to_time(np.arange(D.shape[1]), sr=sr, hop_length=hop_length)
    
    return S_db, frequencies, times


def extract_features(
    audio: np.ndarray,
    sr: int = DEFAULT_SR,
    bands: Optional[Dict[str, Tuple[float, float]]] = None
) -> AcousticFeatures:
    """
    Extract acoustic features from audio signal.
    
    Parameters
    ----------
    audio : np.ndarray
        Audio time series
    sr : int
        Sampling rate
    bands : dict, optional
        Frequency bands to analyze
    
    Returns
    -------
    AcousticFeatures
        Extracted features
    """
    if not LIBROSA_AVAILABLE:
        raise ImportError("librosa is required for feature extraction")
    
    if bands is None:
        bands = FREQUENCY_BANDS
    
    # Compute spectrogram
    S_db, freqs, times = compute_spectrogram(audio, sr)
    
    # Shannon entropy
    S_power = librosa.db_to_power(S_db)
    S_norm = S_power / (np.sum(S_power) + 1e-12)
    shannon_entropy = -np.sum(S_norm * np.log2(S_norm + 1e-12))
    
    # Spectral centroid
    spectral_centroid = librosa.feature.spectral_centroid(
        y=audio, sr=sr
    ).mean()
    
    # Spectral bandwidth
    spectral_bandwidth = librosa.feature.spectral_bandwidth(
        y=audio, sr=sr
    ).mean()
    
    # Zero crossing rate
    zero_crossing_rate = librosa.feature.zero_crossing_rate(audio).mean()
    
    # MFCCs
    mfccs = librosa.feature.mfcc(
        y=audio, sr=sr, n_mfcc=13
    ).mean(axis=1)
    
    # Band powers
    band_powers = {}
    for band_name, (low, high) in bands.items():
        # Find frequency indices
        idx_low = np.argmin(np.abs(freqs - low))
        idx_high = np.argmin(np.abs(freqs - high))
        
        # Average power in band
        if idx_high > idx_low:
            band_power = np.mean(S_power[idx_low:idx_high, :])
            band_powers[band_name] = 10 * np.log10(band_power + 1e-12)
        else:
            band_powers[band_name] = -np.inf
    
    # Acoustic Complexity Index (ACI)
    aci = compute_aci(S_power)
    
    # Biodiversity Index (simplified)
    bi = compute_bi(band_powers)
    
    # Normalized Difference Soundscape Index (NDSI)
    ndsi = compute_ndsi(band_powers)
    
    return AcousticFeatures(
        shannon_entropy=shannon_entropy,
        spectral_centroid=spectral_centroid,
        spectral_bandwidth=spectral_bandwidth,
        zero_crossing_rate=zero_crossing_rate,
        aci=aci,
        bi=bi,
        ndsi=ndsi,
        band_powers=band_powers,
        mfccs=mfccs,
        spectrogram=S_db,
        frequencies=freqs,
        times=times
    )


def compute_aci(S_power: np.ndarray) -> float:
    """
    Compute Acoustic Complexity Index.
    
    Parameters
    ----------
    S_power : np.ndarray
        Power spectrogram
    
    Returns
    -------
    float
        ACI value
    """
    # ACI = sum(abs(diff) / sum) across time
    aci_total = 0
    
    for freq_bin in range(S_power.shape[0]):
        diff_sum = np.sum(np.abs(np.diff(S_power[freq_bin, :])))
        total_sum = np.sum(S_power[freq_bin, :])
        if total_sum > 0:
            aci_total += diff_sum / total_sum
    
    return aci_total / S_power.shape[0]


def compute_bi(band_powers: Dict[str, float]) -> float:
    """
    Compute Biodiversity Index.
    
    Parameters
    ----------
    band_powers : dict
        Powers in each frequency band
    
    Returns
    -------
    float
        BI value (0-1)
    """
    # BI = 1 - (min_power / max_power) in biological bands
    bio_bands = ['fish_chorus', 'invertebrate', 'snapping_shrimp']
    
    powers = []
    for band in bio_bands:
        if band in band_powers and band_powers[band] > -np.inf:
            powers.append(band_powers[band])
    
    if len(powers) < 2:
        return 0.0
    
    powers = np.array(powers)
    bi = 1 - (powers.min() / (powers.max() + 1e-12))
    
    return np.clip(bi, 0, 1)


def compute_ndsi(band_powers: Dict[str, float]) -> float:
    """
    Compute Normalized Difference Soundscape Index.
    
    Parameters
    ----------
    band_powers : dict
        Powers in each frequency band
    
    Returns
    -------
    float
        NDSI value (-1 to 1)
    """
    # NDSI = (bio_power - anthro_power) / (bio_power + anthro_power)
    bio_power = band_powers.get('fish_chorus', -np.inf)
    if bio_power == -np.inf:
        bio_power = band_powers.get('snapping_shrimp', -100)
    
    anthro_power = band_powers.get('low', -100)
    
    if bio_power == -np.inf and anthro_power == -np.inf:
        return 0.0
    
    bio_linear = 10 ** (bio_power / 10)
    anthro_linear = 10 ** (anthro_power / 10)
    
    ndsi = (bio_linear - anthro_linear) / (bio_linear + anthro_linear + 1e-12)
    
    return np.clip(ndsi, -1, 1)


def detect_snapping_shrimp(
    audio: np.ndarray,
    sr: int = DEFAULT_SR,
    threshold: float = 3.0
) -> Dict:
    """
    Detect snapping shrimp snaps in audio.
    
    Parameters
    ----------
    audio : np.ndarray
        Audio time series
    sr : int
        Sampling rate
    threshold : float
        Detection threshold (multiples of RMS)
    
    Returns
    -------
    dict
        Snapping shrimp detection results
    """
    # Bandpass filter for snapping shrimp (2-20 kHz)
    sos = signal.butter(10, [2000, 20000], 'bandpass', fs=sr, output='sos')
    filtered = signal.sosfilt(sos, audio)
    
    # Compute envelope
    envelope = np.abs(signal.hilbert(filtered))
    
    # Smooth envelope
    envelope_smooth = ndimage.uniform_filter1d(envelope, size=int(sr * 0.001))
    
    # Find peaks
    threshold_value = np.mean(envelope_smooth) * threshold
    peaks, properties = signal.find_peaks(
        envelope_smooth,
        height=threshold_value,
        distance=int(sr * 0.01),  # 10 ms minimum between snaps
        prominence=threshold_value / 2
    )
    
    # Calculate snap rate
    duration = len(audio) / sr
    snap_rate = len(peaks) / duration
    
    # Calculate inter-snap intervals
    if len(peaks) > 1:
        isi = np.diff(peaks) / sr
        isi_mean = np.mean(isi)
        isi_std = np.std(isi)
    else:
        isi_mean = 0
        isi_std = 0
    
    return {
        'snap_count': len(peaks),
        'snap_rate': snap_rate,
        'snaps_per_minute': snap_rate * 60,
        'mean_amplitude': np.mean(properties['peak_heights']) if len(peaks) > 0 else 0,
        'isi_mean': isi_mean,
        'isi_std': isi_std,
        'activity_level': 'high' if snap_rate > 10 else 'medium' if snap_rate > 2 else 'low'
    }


def design_restoration_signal(
    duration: float = 60.0,
    sr: int = DEFAULT_SR,
    target_bands: List[str] = ['fish_chorus', 'snapping_shrimp'],
    emphasize_factor: float = 2.0
) -> np.ndarray:
    """
    Design acoustic restoration signal.
    
    Parameters
    ----------
    duration : float
        Signal duration in seconds
    sr : int
        Sampling rate
    target_bands : list
        Frequency bands to emphasize
    emphasize_factor : float
        Amplification factor for target bands
    
    Returns
    -------
    np.ndarray
        Restoration signal
    """
    t = np.linspace(0, duration, int(sr * duration))
    signal_sum = np.zeros_like(t)
    
    for band_name in target_bands:
        if band_name in FREQUENCY_BANDS:
            low, high = FREQUENCY_BANDS[band_name]
            
            # Generate frequency sweep
            freq_sweep = np.linspace(low, high, len(t))
            band_signal = np.sin(2 * np.pi * freq_sweep * t)
            
            # Apply envelope
            envelope = np.exp(-t / 10)  # Decay over time
            band_signal *= envelope
            
            # Add to sum
            signal_sum += band_signal * emphasize_factor
    
    # Add background ambient noise
    ambient = np.random.randn(len(t)) * 0.1
    signal_sum += ambient
    
    # Normalize
    signal_sum = signal_sum / np.max(np.abs(signal_sum)) * 0.95
    
    return signal_sum


def calculate_sound_pressure_level(
    audio: np.ndarray,
    calibration: float = 1.0
) -> float:
    """
    Calculate sound pressure level in dB re 1 μPa.
    
    Parameters
    ----------
    audio : np.ndarray
        Audio time series
    calibration : float
        Calibration factor (μPa per unit)
    
    Returns
    -------
    float
        SPL in dB re 1 μPa
    """
    # RMS pressure
    p_rms = np.sqrt(np.mean(audio**2)) * calibration
    
    # Convert to dB re 1 μPa
    spl = 20 * np.log10(p_rms / 1e-6 + 1e-12)
    
    return spl


# =============================================================================
# MODULE METADATA
# =============================================================================

__all__ = [
    'load_audio',
    'compute_spectrogram',
    'extract_features',
    'compute_aci',
    'compute_bi',
    'compute_ndsi',
    'detect_snapping_shrimp',
    'design_restoration_signal',
    'calculate_sound_pressure_level',
    'AcousticFeatures',
    'FREQUENCY_BANDS',
    'ACOUSTIC_INDICES'
]

__version__ = '1.0.0'
__doi__ = '10.5281/zenodo.18913829'
