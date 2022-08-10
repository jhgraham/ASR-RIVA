
import io
import librosa
from time import time
import numpy as np
import grpc
import requests
import logging

# NLP proto
import riva_api.riva_nlp_pb2 as rnlp
import riva_api.riva_nlp_pb2_grpc as rnlp_srv

# ASR proto
import riva_api.riva_asr_pb2 as rasr
import riva_api.riva_asr_pb2_grpc as rasr_srv

import riva_api.riva_audio_pb2 as ra


class RivaASRClient:

    def __init__(self):

        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('riva-client-logger')
        self.logger.info('Initialising Riva Client')

        #channel = grpc.insecure_channel("riva-speech:50051")
        channel = grpc.insecure_channel("localhost:50051")

        self.riva_asr = rasr_srv.RivaSpeechRecognitionStub(channel)

    def toText(self, file_path):
        audio, sr = librosa.core.load(file_path, sr=None)
        with io.open(file_path, 'rb') as fh:
            content = fh.read()

        req = rasr.RecognizeRequest()
        req.audio = content                                   # raw bytes
        req.config.encoding = ra.AudioEncoding.LINEAR_PCM     # Supports LINEAR_PCM, FLAC, MULAW and ALAW audio encodings
        req.config.sample_rate_hertz = sr                     # Audio will be resampled if necessary
        req.config.language_code = "en-US"                    # Ignored, will route to correct model in future release
        req.config.max_alternatives = 1                       # How many top-N hypotheses to return
        req.config.enable_automatic_punctuation = True        # Add punctuation when end of VAD detected
        req.config.audio_channel_count = 1                    # Mono channel

        self.logger.info('Calling Recognise')

        response = self.riva_asr.Recognize(req)
        asr_best_transcript = response.results[0].alternatives[0].transcript

        return asr_best_transcript
