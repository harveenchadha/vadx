
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname("../src"))


from src.vadx import VadFactory


if __name__ == "__main__":
    #model = VadFactory(backend='silero')#.get_vad()

    model_2 = VadFactory(backend='webrtc')
    #model.split()
    print(sys.argv)
    if len(sys.argv)>1:
        filename = sys.argv[1]
    else:
        filename = '1.wav'
    for agg in [0,1,2,3]:
        print(model_2.get_timestamps(filename, agg))

