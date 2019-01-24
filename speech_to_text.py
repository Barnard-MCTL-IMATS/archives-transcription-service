def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    
    client = speech.SpeechClient()
    audio  = speech.types.RecognitionAudio(uri = gcs_uri)
    config = speech.types.RecognitionConfig(
        encoding = enums.RecognitionConfig.AudioEncoding.FLAC,
        language_code = 'en-US')
    
    operation = client.long_running_recognize(config, audio)
    print('Waiting for operation to complete...')
    response = operation.result()
    return response

def set_google_app_credentials(root):
    from os import environ
    from os.path import join
    credentials_json = ""
    credentials = join(root, credentials_json)
    try:
        environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
        print("Set!")
    except:
        print("NOT Set!")
        
def get_dirs_and_wav_files():
    from os import getcwd, listdir
    from os.path import join, splitext
    root = getcwd()
    wav_dir = join(root, 'wav-files')
    wav_files = [join(wav_dir, wav) for wav in listdir(wav_dir) if splitext(wav)[1] == '.wav']
    flac_dir = join(root, 'flac-files')
    transcriptions_dir = join(root, 'transcriptions')
    return root, wav_dir, wav_files, flac_dir, transcriptions_dir

def get_sample_rate(wav):
    from pydub.utils import mediainfo
    info = mediainfo(wav)
    sample_rate = int(info['sample_rate'])
    return sample_rate

def reset_sample_and_channel(wav, sample_rate):
    from pydub import AudioSegment
    audio = AudioSegment.from_file(wav, format = "wav", frame_rate = sample_rate)
    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)
    return audio

def convert_to_flac(wav, flac_dir):
    from os.path import basename, splitext, join
    basename = basename(wav)
    filename = splitext(basename)[0]
    flac_path = join(flac_dir, filename + '.flac')
    x = 1
    # flesh this out to handle it better
    try:
        audio.export(flac_path, format = 'flac')
        return 0
    except:
        return 1
    
root, wav_dir, wav_files, flac_dir, transcriptions_dir = get_dirs_and_wav_files()

set_google_app_credentials(root)

for wav in wav_files:
    sample_rate = get_sample_rate(wav)
    audio = reset_sample_and_channel(wav, sample_rate)
    convert_result = convert_to_flac(wav, flac_dir)
    
import os
import pandas as pd

bucket =.............
samples = ........... # 

for sample in samples:
    '''Build Paths'''
    sample_basename = os.path.splitext(sample)[0]
    sample_filename = os.path.basename(sample_basename)
    
    csv_dir = os.path.join(transcriptions_dir, sample_filename)
    csv_file = os.path.join(csv_dir, sample_filename + '.csv')
    
    '''Transcribe'''
    gcs_uri = os.path.join(bucket, sample)
    results = transcribe_gcs(gcs_uri).results
    all_transcriptions = [result.alternatives[0].transcript for result in results]
    all_confidence = [result.alternatives[0].confidence for result in results]
    result_dict = {'transcription': all_transcriptions, 'confidence': all_confidence}
    
    '''Write to dir'''
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)
    
    df = pd.DataFrame(result_dict)
    df.to_csv(csv_file, encoding='utf-8', index=False)    

