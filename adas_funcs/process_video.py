import cv2
from lines import *
from convert import *
from crop_roi import crop_area
from interpolation import interpolate


def process_video(video_path,
                  roi_annotation_path,
                  file_id,
                  lower_bound=(2, 95, 1),
                  upper_bound=(53, 190, 69),
                  canny=(35, 16),
                  debag=True
):
    validate_roi(roi_annotation_path)
    validate_video(video_path)

    #loading video
    cap = cv2.VideoCapture(r"C:\Users\79042\Downloads\видео\cloudy_1.mp4")

    packet_map = interpolate(roi_annotation_path, file_id)
    points_map = convert_points(packet_map)
    frame_number = 0

    # HoughLinesP settings
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 25  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 80  # minimum number of pixels making up a line
    max_line_gap = 15  # maximum gap in pixels between connectable line segments

    # kernel sizes for erosion and dilation
    kernel_size_dil = 2
    kernel_size_erode = 2
    kernel_shape = cv2.MORPH_ELLIPSE

    # color filter params
    h1, l1, s1 = lower_bound
    h2, l2, s2 = upper_bound

    # canny thresholds
    upper, lower = canny

    if debag:
        cv2.resizeWindow("settings", 480, 100)
        # inRange params
        cv2.createTrackbar("h1", "settings", h1, 255, nothing) #2
        cv2.createTrackbar("l1", "settings", l1, 255, nothing) #95
        cv2.createTrackbar("s1", "settings", s1, 255, nothing) #111
        cv2.createTrackbar("h2", "settings", h2, 255, nothing) #143
        cv2.createTrackbar("l2", "settings", l2, 255, nothing) #152
        cv2.createTrackbar("s2", "settings", s2, 255, nothing) #186
        # canny params
        cv2.createTrackbar("upper", "settings", 35, 255, nothing) #40
        cv2.createTrackbar("lower", "settings", 16, 255, nothing) #65


    frames = []
    try:
        while True:
            # reading frames
            ret, img = cap.read()

            # check if the video is ended
            if not ret:
                break

            if frame_number in points_map.keys():
                img_croped = crop_area(img, points_map[frame_number])

            # flip image to work with coordinates
            img_flip = cv2.flip(img_croped, 0)
            # convert to hls color space
            hls = cv2.cvtColor(img_flip, cv2.COLOR_BGR2HLS)

            # creting a copy of image to draw lines
            img_copy = img_flip.copy()

            if debag:
                # setting the inRange params up
                h1 = cv2.getTrackbarPos("h1", "settings")
                l1 = cv2.getTrackbarPos("l1", "settings")
                s1 = cv2.getTrackbarPos("s1", "settings")
                h2 = cv2.getTrackbarPos("h2", "settings")
                l2 = cv2.getTrackbarPos("l2", "settings")
                s2 = cv2.getTrackbarPos("s2", "settings")

            # creating min and max color thresholds
            h_min = np.array((h1, l1, s1), np.uint8)
            h_max = np.array((h2, l2, s2), np.uint8)

            # getting filtered image
            thresh = cv2.inRange(hls, h_min, h_max)

            if debag:
                # getting first and second thresholds for canny
                upper = cv2.getTrackbarPos("upper", "settings")
                lower = cv2.getTrackbarPos("lower", "settings")

            # getting blured original image
            img_blur = cv2.GaussianBlur(hls, (5, 5), 0)

            # finding edges using canny
            canny = cv2.Canny(img_blur, upper, lower) #175, 40

            img_bitwise = cv2.bitwise_and(canny, thresh)

            # creating kernel for dilate and erode funcs
            kernel = cv2.getStructuringElement(
                kernel_shape,
                (2 * kernel_size_dil + 1, 2 * kernel_size_dil + 1),
                (kernel_size_dil, kernel_size_dil)
            )
            kernel_erode = cv2.getStructuringElement(
                kernel_shape,
                (2 * kernel_size_erode + 1, 2 * kernel_size_erode + 1),
                (kernel_size_erode, kernel_size_erode)
            )

            dilatation_dst = cv2.dilate(img_bitwise, kernel)
            erode_dst = cv2.erode(dilatation_dst, kernel_erode)

            # Run Hough on edge detected image
            # Output "lines" is an array containing endpoints of
            # detected line segments
            lines = cv2.HoughLinesP(erode_dst, rho, theta, threshold,
                                    np.array([]), min_line_length, max_line_gap)

            height, width, _ = img_flip.shape
            marking = select_lines(lines, 3200, height)
            polygons = get_polygons(marking, erode_dst)

            img = cv2.flip(img, 0)
            cv2.polylines(img, polygons, True, (255, 0, 255), 2)
            cv2.imshow("frame", cv2.resize(cv2.flip(img, 0), (720, 480)))

            frame_number += 1

            ch = cv2.waitKey(0)
            if ch == 27:
                break
            if ch == 13:
                cv2.imwrite(f"frame_{frame_number - 1}.png", img2)

    except Exception as e:
        print(e)

    cap.release()
    cv2.destroyAllWindows()
    return frames


def validate_video(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        cap.read()
        cap.release()
    except Exception as e:
        raise Exception("Exception while validating video file")


def validate_roi(annotation_path):
    try:
        open(annotation_path)
    except Exception as e:
        raise Exception("Exception while validating roi annotation file")
