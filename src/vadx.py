
class BaseVad(object):
    def get_timestamps():
        pass

    def save_audio_chunks():
        pass

    def split(self):
        print("Inside split method")
        pass

class WebRTCVAD(BaseVad):
    def __init__(self):
        print("Inside webrtc initialization")

    def split(self, aggressiveness):
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