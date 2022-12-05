from process_video import process_video

video_path = r"C:\Users\79042\Downloads\видео\test.mp4"
annotation_path = r"C:\Users\79042\Downloads\diffgram_annotation.json"

process_video(video_path, annotation_path, 197, debag=False)
