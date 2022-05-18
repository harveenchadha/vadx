class BaseVad(object):
    def get_timestamps(self, audio_files):
        if type(audio_files) == str:
            audio_files = [audio_files]
        return audio_files
    

    # def get_timestamps_dir(self, audio_dir, **kwargs):
    #     for audio_file in audio_dir:
    #         print(self.get_timestamps(audio_file, kwargs))


    def save_audio_chunks(self):
        pass

    def get_audio_chunks(self, audio_files, chunks):
        pass

    def split(self, file_paths, **kwargs):
        print("Inside split method")
        pass

    def save_broken_files(blank_offset_duration):
        pass

    def get_broken_files(self, blank_offset_duration):
        pass

    def get_silence_removed_single_file(self, blank_offset_duration):
        pass