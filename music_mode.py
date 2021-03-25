from __future__ import print_function
from __future__ import division

import sys
import math
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from time import time
from base_classes import *

import pyaudio
import config
import dsp


SPECTRUM_PIXELS = 64

# variants (visualization)
# 0 = spectrum
# 1 = energy
# 2 = scroll

# shapes
# 0 = circular in - out
# 1 = circular out - in
# 2 = vertical in - out
# 3 = vertical out - in
# 4 = vertical left - right
# 5 = vertical right - left
# 6 = horizontal in - out
# 7 = horizontal out- in
# 8 = horizontal bottom - up
# 9 = horizontal top - down
# 10 = continental

_gamma = np.load(config.GAMMA_TABLE_PATH)
"""Gamma lookup table used for nonlinear brightness correction"""


shape = 5
pos = 0.0 # 0.0 - 255.0 
pos_time_stamp = time()

mel_output = np.tile(0, SPECTRUM_PIXELS)

class MusicMode(Mode):
    key = "MUSIC"
    
    
    def __init__(self, variant, shape):
        self.variant = variant
        self.shape = shape
        self.spectrum_len = SPECTRUM_PIXELS if shape is not 10 else 6
        
        if not stream_active():
            start_microphone_stream()
            
            
            
        # filters for visualization
        self.r_filt = dsp.ExpFilter(np.tile(0.01, self.spectrum_len),
                               alpha_decay=0.2, alpha_rise=0.99)
        self.g_filt = dsp.ExpFilter(np.tile(0.01, self.spectrum_len),
                               alpha_decay=0.05, alpha_rise=0.3)
        self.b_filt = dsp.ExpFilter(np.tile(0.01, self.spectrum_len),
                               alpha_decay=0.1, alpha_rise=0.5)
        self.common_mode = dsp.ExpFilter(np.tile(0.01, self.spectrum_len),
                               alpha_decay=0.99, alpha_rise=0.01)
        self.p_filt = dsp.ExpFilter(np.tile(1, (3, self.spectrum_len)),
                               alpha_decay=0.08, alpha_rise=0.5) # default: decay = 0.1, rise = 0.99
        self.p = np.tile(1.0, (3, self.spectrum_len))
        self.gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                             alpha_decay=0.008, alpha_rise=0.5) # default: decay = 0.001, rise = 0.99
        

        self._prev_spectrum = np.tile(0.01, self.spectrum_len)
        
    def copy(self):
        return MusicMode(self.variant, self.shape)
        
    def args(self):
        return str(self.variant) + "," + str(self.shape)
        
    def loop(self, _leds):
        
        global mel_output
        
        output = 0.0
        
        if self.variant == 0:
            output = self.visualize_spectrum(mel_output)
        elif self.variant == 1:
            output = self.visualize_energy(mel_output)
        elif self.variant == 2:
            output = self.visualize_scroll(mel_output)
        
        # Truncate values and cast to integer
        col = np.clip(output, 0, 255).astype(int)
        # Optional gamma correction
        c = _gamma[col] if config.SOFTWARE_GAMMA_CORRECTION else np.copy(col)
        # Encode 24-bit LED values in 32 bit integers
        r = np.left_shift(c[0][:].astype(int), 8)
        g = np.left_shift(c[1][:].astype(int), 16)
        b = c[2][:].astype(int)
        rgb = np.bitwise_or(np.bitwise_or(r, g), b)
        
        
        color_idx = np.tile(0.0, len(_leds))
        
        if self.shape == 0: # circular in - out
            color_idx = np.array(map(lambda led: (led.dist - 10) * 2.2, _leds))
            
        elif self.shape == 1: # circular out - in
            color_idx = np.array(map(lambda led: abs(led.dist - 200), _leds))
            
        elif self.shape == 2: # vertical in - out
            color_idx = np.array(map(lambda led: abs(led.long - 20) * 2, _leds))
            
        elif self.shape == 3: # vertical out - in
            color_idx = np.array(map(lambda led: -abs(led.long - 20) + 200, _leds))
            
        elif self.shape == 4: # vertical left - right
            color_idx = np.array(map(lambda led: led.long + 120.0, _leds))
            
        elif self.shape == 5: # vertical right - left
            color_idx = np.array(map(lambda led: 255 - (led.long + 120.0) * 0.8, _leds))
            
        elif self.shape == 6: # horizontal in - out
            color_idx = np.array(map(lambda led: abs(led.lat - 20) * 4, _leds))
                
        elif self.shape == 7: # horizontal out - in
            color_idx = np.array(map(lambda led: 255 - abs(led.lat - 20) * 4, _leds))
                
        elif self.shape == 8: # horizontal bottom - up
            color_idx = np.array(map(lambda led: (led.lat + 45.0) * 1.5, _leds))
                    
        elif self.shape == 9: # horizontal top - down
            color_idx = np.array(map(lambda led: 255 - (led.lat + 65.0) * 1.5, _leds))
            
        elif self.shape == 10: # continental
            color_idx = np.array(map(lambda led: 0.0 + led.continent.index, _leds))
                    
        
        if self.shape is not 10:
            color_idx *= self.spectrum_len / 256
            
        color_idx = np.clip(color_idx.astype(int), 0, len(rgb) - 1)
        
        for i in range(len(_leds)):
            strip._led_data[_leds[i].pos] = rgb[color_idx[i]]
        
        

    def visualize_scroll(self, y):
        """Effect that originates in the center and scrolls outwards"""
        y = y**3.0 # default **2.0
        self.gain.update(y)
        y /= self.gain.value
        y *= 255.0
        r = int(np.max(y[:len(y) // 3]))
        g = int(np.max(y[len(y) // 3: 2 * len(y) // 3]))
        b = int(np.max(y[2 * len(y) // 3:]))
        # Scrolling effect window
        self.p[:, 2:] = self.p[:, :-2] # default 1: and :-1
        self.p *= 0.98
        self.p = gaussian_filter1d(self.p, sigma=2.0) # default 0.2
        # Create new color originating at the center
        self.p[0, 0] = r
        self.p[1, 0] = g
        self.p[2, 0] = b
        # Update the LED strip
        return self.p


    def visualize_energy(self, y):
        """Effect that expands from the center with increasing sound energy"""
        y = np.copy(y)
        self.gain.update(y)
        
        y /= self.gain.value
        
        # Scale by the width of the LED strip
        y *= float((self.spectrum_len) - 1)
        # Map color channels according to energy in the different freq bands
        scale = 1.0 # default 0.9
        r = int(np.mean(y[:len(y) // 3]**scale))
        g = int(np.mean(y[len(y) // 3: 2 * len(y) // 3]**scale))
        b = int(np.mean(y[2 * len(y) // 3:]**scale))
        # Assign color to different frequency regions
        self.p[0, :r] = 255.0
        self.p[0, r:] = 0.0
        self.p[1, :g] = 255.0
        self.p[1, g:] = 0.0
        self.p[2, :b] = 255.0
        self.p[2, b:] = 0.0
        self.p_filt.update(self.p)
        self.p = np.round(self.p_filt.value)
        # Apply substantial blur to smooth the edges
        self.p[0, :] = gaussian_filter1d(self.p[0, :], sigma=4.0)
        self.p[1, :] = gaussian_filter1d(self.p[1, :], sigma=4.0)
        self.p[2, :] = gaussian_filter1d(self.p[2, :], sigma=4.0)
        # Set the new pixel value
        return self.p



    def visualize_spectrum(self, y):
        """Effect that maps the Mel filterbank frequencies onto the LED strip"""
        y = np.copy(interpolate(y, self.spectrum_len))
        self.common_mode.update(y)
        diff = y - self._prev_spectrum
        self._prev_spectrum = np.copy(y)
        # Color channel mappings
        
        #pos = 50
        
        #c0 = wheel(pos)
        #c1 = wheel((pos+85)%255)
        #c2 = wheel((pos+170)%255)
        
        r = self.r_filt.update(y - self.common_mode.value)
        g = np.abs(diff)
        b = self.b_filt.update(np.copy(y))
        
        #r = r_filt.update((c0.r / 255) * (y - common_mode.value) + (c1.r / 255) * np.abs(diff) + (c2.r / 255) * np.copy(y))
        #g = (c0.g / 255) * (y - common_mode.value) + (c1.g / 255) * np.abs(diff) + (c2.g / 255) * (np.copy(y))
        #b = b_filt.update((c0.b / 255) * (y - common_mode.value) + (c1.b / 255) * np.abs(diff) + (c2.b / 255) * (np.copy(y)))
        
        output = np.array([r, g, b]) * 255
        
        return output#self.spectrum_len)

                    

_time_prev = time() * 1000.0
"""The previous time that the frames_per_second() function was called"""

_fps = dsp.ExpFilter(val=config.FPS, alpha_decay=0.2, alpha_rise=0.2)
"""The low-pass filter used to estimate frames-per-second"""


def frames_per_second():
    """Return the estimated frames per second

    Returns the current estimate for frames-per-second (FPS).
    FPS is estimated by measured the amount of time that has elapsed since
    this function was previously called. The FPS estimate is low-pass filtered
    to reduce noise.

    This function is intended to be called one time for every iteration of
    the program's main loop.

    Returns
    -------
    fps : float
        Estimated frames-per-second. This value is low-pass filtered
        to reduce noise.
    """
    global _time_prev, _fps
    time_now = time() * 1000.0
    dt = time_now - _time_prev
    _time_prev = time_now
    if dt == 0.0:
        return _fps.value
    return _fps.update(1000.0 / dt)


def memoize(function):
    """Provides a decorator for memoizing functions"""
    from functools import wraps
    memo = {}

    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper


@memoize
def _normalized_linspace(size):
    return np.linspace(0, 1, size)


def interpolate(y, new_length):
    """Intelligently resizes the array by linearly interpolating the values

    Parameters
    ----------
    y : np.array
        Array that should be resized

    new_length : int
        The length of the new interpolated array

    Returns
    -------
    z : np.array
        New array with length of new_length that contains the interpolated
        values of y.
    """
    if len(y) == new_length:
        return y
    x_old = _normalized_linspace(len(y))
    x_new = _normalized_linspace(new_length)
    z = np.interp(x_new, x_old, y)
    return z








fft_plot_filter = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                         alpha_decay=0.5, alpha_rise=0.99)
mel_gain = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                         alpha_decay=0.01, alpha_rise=0.99)
mel_smoothing = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                         alpha_decay=0.5, alpha_rise=0.99)
volume = dsp.ExpFilter(config.MIN_VOLUME_THRESHOLD,
                       alpha_decay=0.02, alpha_rise=0.02)
fft_window = np.hamming(int(config.MIC_RATE / config.FPS) * config.N_ROLLING_HISTORY)
prev_fps_update = time()


overflows = 0
prev_ovf_time = time()

def microphone_update():
    
    # start mic stream if it's not running
    if stream is None or pa is None:
        start_microphone_stream()
    
    global y_roll, prev_rms, prev_exp, prev_fps_update, stream, frames_per_buffer, overflows, prev_overflow_time, mel_output
    
    try:
        y = np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
        y = y.astype(np.float32)
        stream.read(stream.get_read_available(), exception_on_overflow=False)
        #callback(y)
    except IOError:
        overflows += 1
        if time() > prev_ovf_time + 1:
            prev_ovf_time = time()
            print('Audio buffer has overflowed {} times'.format(overflows))
    
    
    # Normalize samples between 0 and 1
    y = y / 2.0**15
    # Construct a rolling window of audio samples
    y_roll[:-1] = y_roll[1:]
    y_roll[-1, :] = np.copy(y)
    y_data = np.concatenate(y_roll, axis=0).astype(np.float32)
    
    vol = np.max(np.abs(y_data))
    if vol < config.MIN_VOLUME_THRESHOLD:
        #print('No audio input. Volume below threshold. Volume:', vol)
        mel_output = np.tile(0.0, config.N_FFT_BINS)
        
    else:
        # Transform audio input into the frequency domain
        N = len(y_data)
        N_zeros = 2**int(np.ceil(np.log2(N))) - N
        # Pad with zeros until the next power of two
        y_data *= fft_window
        y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
        YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
        # Construct a Mel filterbank from the FFT data
        mel = np.atleast_2d(YS).T * dsp.mel_y.T
        # Scale data to values more suitable for visualization
        # mel = np.sum(mel, axis=0)
        mel = np.sum(mel, axis=0)
        mel = mel**2.0
        # Gain normalization
        mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
        mel /= mel_gain.value
        mel = mel_smoothing.update(mel)
        
        mel_output = mel

    
    if config.DISPLAY_FPS:
        fps = frames_per_second()
        if time() - 0.5 > prev_fps_update:
            prev_fps_update = time()
            print('FPS {:.0f} / {:.0f}'.format(fps, config.FPS))
            
def wheel(pos):
    if pos < 85:
        return C.fromRGB(255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return C.fromRGB(0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return C.fromRGB(pos * 3, 0, 255 - pos * 3)


# Number of audio samples to read every time frame
samples_per_frame = int(config.MIC_RATE / config.FPS)

# Array containing the rolling audio sample window
y_roll = np.random.rand(config.N_ROLLING_HISTORY, samples_per_frame) / 1e16



## MICROPHONE

"""global variables for microphone stream"""
pa = None
stream = None
frames_per_buffer = int(config.MIC_RATE / config.FPS)
        
def start_microphone_stream():
    global pa, frames_per_buffer, stream
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=config.MIC_RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer)
    
def stop_microphone_stream():
    global pa, stream
    if stream is not None:
        stream.stop_stream()
        stream.close()
        stream = None
    if pa is not None:
        pa.terminate()
        pa = None
    print('mic stream stopped')
    
def stream_active():
    return stream is not None

