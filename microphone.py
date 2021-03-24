import config
import pyaudio


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
    print('mic srteam stopped')
    
def stream_active():
    return stream is not None