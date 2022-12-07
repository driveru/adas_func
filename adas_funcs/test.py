from process_video import process_video


def start_test_cloudy_1():
    video_path = r"..\tests\cloudy_1_test.mp4"
    annotation_path = r"..\tests\cloudy_1_annotation.json"
    file_id = 197

    process_video(video_path, annotation_path, file_id, debag=False)


if __name__ == '__main__':
    start_test_cloudy_1()
