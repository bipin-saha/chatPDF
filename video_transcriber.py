import moviepy.editor as mp
import speech_recognition as sr
import os

def transcribe_audio_chunk(audio_chunk):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_chunk) as source:
        audio_data = recognizer.record(source)

    try:
        text_result = recognizer.recognize_google(audio_data, language='en-US')
        return text_result
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def transcribe_video(video_path):
    # Step 1: Extract audio from the video
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile("temp_audio.wav")

    # Step 2: Split the audio into smaller chunks (e.g., 10 seconds each)
    chunk_duration = 10  # in seconds
    total_duration = audio_clip.duration
    chunk_paths = []

    for start_time in range(0, int(total_duration), chunk_duration):
        end_time = min(start_time + chunk_duration, total_duration)
        chunk_path = f"temp_audio_chunk_{start_time}_{end_time}.wav"
        audio_chunk = audio_clip.subclip(start_time, end_time)
        audio_chunk.write_audiofile(chunk_path)
        chunk_paths.append(chunk_path)

    # Step 3: Transcribe each audio chunk
    transcribed_texts = []
    for chunk_path in chunk_paths:
        text_result = transcribe_audio_chunk(chunk_path)
        transcribed_texts.append(text_result)

    # Step 4: Concatenate the transcribed texts
    final_transcription = " ".join(transcribed_texts)
    print("Transcription:\n", final_transcription)

    # Clean up temporary files
    audio_clip.close()
    video_clip.close()
    os.remove("temp_audio.wav")
    for chunk_path in chunk_paths:
        os.remove(chunk_path)

# Example usage
video_path = "C:/Users/HP/Downloads/Video/1.mp4"
transcribe_video(video_path)
