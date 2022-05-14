
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname("../src"))


from src.vadx import VadFactory


if __name__ == "__main__":
    #model = VadFactory(backend='silero')#.get_vad()

    model_2 = VadFactory(backend='webrtc')
    #model.split()
    model_2.get_timestamps('1.wav')