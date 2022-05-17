import collections
import contextlib
import sys
import wave
import os
import webrtcvad
from ..base import BaseVad

# try:
#     import webrtcvad
# except:
#     os.system('pip install webrtcvad')
#     import webrtcvad

def read_wave(path):
    """Reads a .wav file.

    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate



def write_wave(path, audio, sample_rate):
    """Writes a .wav file.

    Takes path, PCM audio data, and sample rate.
    """
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)


class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def vad_collector(sample_rate, frame_duration_ms,
                  padding_duration_ms, vad, frames, start_time, end_time):
    """
    Arguments:
    sample_rate - The audio sample rate, in Hz.
    frame_duration_ms - The frame duration in milliseconds.
    padding_duration_ms - The amount to pad the window, in milliseconds.
    vad - An instance of webrtcvad.Vad.
    frames - a source of audio frames (sequence or generator).

    Returns: A generator that yields PCM audio data.
    """
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    # We use a deque for our sliding window/ring buffer.
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
    # NOTTRIGGERED state.
    triggered = False

    voiced_frames = []
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)

        #sys.stdout.write('1' if is_speech else '0')
        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            # If we're NOTTRIGGERED and more than 90% of the frames in
            # the ring buffer are voiced frames, then enter the
            # TRIGGERED state.
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                start_time.append(ring_buffer[0][0].timestamp)
                #sys.stdout.write('+(%s)' % (ring_buffer[0][0].timestamp,))
                # We want to yield all the audio we see from now until
                # we are NOTTRIGGERED, but we have to start with the
                # audio that's already in the ring buffer.
                for f, s in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            # We're in the TRIGGERED state, so collect the audio data
            # and add it to the ring buffer.
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            # If more than 90% of the frames in the ring buffer are
            # unvoiced, then enter NOTTRIGGERED and yield whatever
            # audio we've collected.
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                #sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                end_time.append(frame.timestamp + frame.duration)
                triggered = False
                yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                voiced_frames = []
    if triggered:
        #sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
        end_time.append(frame.timestamp + frame.duration)
    #sys.stdout.write('\n')
    # If we have any leftover voiced audio when we run out of input,
    # yield it.
    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames])


def create_new_vad_object():
    # vad = webrtcvad.Vad()
    print("I am here")







class WebRTCClass(BaseVad):
    '''def __init__(self):
        print("Inside webrtc initialization")
        pass'''
    def __init__(self):
        #initialize vad object only once
        try:
            print("Inside try")
            # from webrtc.pywebrtc import create_new_vad_object
            # create_new_vad_object()
            self.vad_obj = webrtcvad.Vad()
            
        except:
            print("WebRTCVAD is not installed")

    def change_aggressiveness(self, aggressiveness):
        self.vad_obj.set_mode(aggressiveness)


    def get_timestamps_single(self, audio_file, frame_duration, padding_duration):
        audio, sample_rate = read_wave(audio_file)
        frames = list(frame_generator(frame_duration, audio, sample_rate))
        start_time = []
        end_time = []
        segments = vad_collector(sample_rate, frame_duration, padding_duration, self.vad_obj, frames, start_time, end_time)
        #print(segments)
        chunks = 0
        for i, segment in enumerate(segments):
            chunks = chunks + 1
        if chunks != len(start_time):
            print("Error: Segments not broken properly")
        
        return list(zip(start_time, end_time))


    def get_timestamps(self, audio_files, aggressiveness=3, frame_duration=30, padding_duration=300):
        self.change_aggressiveness(aggressiveness)
        if type(audio_files) == str:
            audio_files = [audio_files]

        dict_mapping = {}
        for file in audio_files:
            timestamps = self.get_timestamps_single(file, frame_duration, padding_duration)
            dict_mapping[file] = timestamps

        if type(audio_files) == str:
            return dict_mapping[audio_file]

        return dict_mapping


# def main(args):
#     #sample_rate 8000,16000,32000,48000
#     #frame_duration : 10,20,30
#     #aggressiveness : 0,1,2,3
#     #padding_duration : 300





#     if len(args) != 2:
#         sys.stderr.write(
#             'Usage: example.py <aggressiveness> <path to wav file>\n')
#         sys.exit(1)
#     audio, sample_rate = read_wave(args[1])
#     vad = webrtcvad.Vad(int(args[0]))
#     frames = frame_generator(30, audio, sample_rate)
#     frames = list(frames)
#     segments = vad_collector(sample_rate, 30, 300, vad, frames)
#     for i, segment in enumerate(segments):
#         path = 'chunk-%002d.wav' % (i,)
#         print(' Writing %s' % (path,))
#         write_wave(path, segment, sample_rate)






# if __name__ == '__main__':
#     main(sys.argv[1:])
