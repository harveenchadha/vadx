


class BaseVad(object):
    def get_timestamps():
        pass

    def save_audio_chunks():
        pass

    def split(self, file_paths, **kwargs):
        print("Inside split method")
        pass

class WebRTCVAD(BaseVad):
    def __init__(self):
        print("Inside webrtc initialization")

    def __new__(self):
        #initialize vad object only once
        try:
            print("Inside try")
            from webrtc.pywebrtc import create_new_vad_object
            create_new_vad_object()
        except:
            print("WebRTCVAD is not installed")
        

    def split(self, file_paths, aggressiveness=1):
        print("Set aggressiveness to ", aggressiveness)


class SileroVAD(BaseVad):
    def __init__(self):
        print("Inside silero VAD initialization")

class VadFactory(object):
    def __new__(self, backend='webrtc'):
        if backend == 'webrtc':
            webrtc = WebRTCVAD()
            print("WebRTC is initialized")
            return webrtc
        if backend == 'silero':
            print("Silero is initialized")
            return SileroVAD()
    

def load_model():
    return vadx()