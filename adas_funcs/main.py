from lines import *
from convert import *
from crop_roi import crop_area
from interpolation import interpolate
import cv2
import numpy as np
import time

def nothing(*arg):
        pass

# creating settings window
cv2.namedWindow( "settings" )

#creating trackbars to set up params
#inRange params
cv2.createTrackbar('h1', 'settings', 2, 255, nothing) #101
cv2.createTrackbar('s1', 'settings', 95, 255, nothing) #118
cv2.createTrackbar('v1', 'settings', 1, 255, nothing) #111
cv2.createTrackbar('h2', 'settings', 53, 255, nothing) #143
cv2.createTrackbar('s2', 'settings', 190, 255, nothing) #152
cv2.createTrackbar('v2', 'settings', 69, 255, nothing) #186
#canny params
cv2.createTrackbar('first', 'settings', 35, 255, nothing) #40
cv2.createTrackbar('second', 'settings', 16, 255, nothing) #65
#erosion and dilation kernel params
cv2.createTrackbar('kernel_size_dil', 'settings', 2, 21, nothing)
cv2.createTrackbar('kernel_size_erode', 'settings', 2, 21, nothing)

crange = [0,0,0, 0,0,0]
kernel_shape = cv2.MORPH_ELLIPSE

#loading video
cap = cv2.VideoCapture(r'C:\Users\79042\Downloads\видео\cloudy_1.mp4')
#loading image
img_croped = cv2.imread(r'C:\Users\79042\Desktop\Screenshot_3.png')

annotation_path = r'C:\Users\79042\Downloads\diffgram_annotation.json'
file_id = 197

packet_map = interpolate(annotation_path, file_id)
points_map = convert_points(packet_map)
frame_number = 0


#HoughLinesP settings
rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 25  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 80  # minimum number of pixels making up a line
max_line_gap = 15  # maximum gap in pixels between connectable line segments

cv2.resizeWindow("settings", 480, 100)

while True:
    #uncoment to work with video
    _, img = cap.read()

    if frame_number in points_map.keys():
        img_croped = crop_area(img, points_map[frame_number])


    frame_number += 1
    #flip image to work with coordinates
    img_flip = cv2.flip(img_croped, 0)
    #convert to hls color space
    hls = cv2.cvtColor(img_flip, cv2.COLOR_BGR2HLS)

    #creting a copy of image to draw lines
    img_copy = img_flip.copy()

    #setting the inRange params up
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    #creating min and max color thresholds
    h_min = np.array((h1, s1, v1), np.uint8) # 19 134 125
    h_max = np.array((h2, s2, v2), np.uint8) # 163 170 192

    #getting filtered image
    thresh = cv2.inRange(hls, h_min, h_max)

    #getting first and second thresholds for canny
    first = cv2.getTrackbarPos('first', 'settings')
    second = cv2.getTrackbarPos('second', 'settings')

    #getting blured original image
    img_blur = cv2.GaussianBlur(hls, (5, 5), 0)

    #finding edges using canny
    canny = cv2.Canny(img_blur, first, second) #175, 40

    img_bitwise = cv2.bitwise_and(canny, thresh)

    #getting kernel sizes
    kernel_size_dil = cv2.getTrackbarPos('kernel_size_dil', 'settings')
    kernel_size_erode = cv2.getTrackbarPos('kernel_size_erode', 'settings')

    #creating kernel for dilate and erode funcs
    kernel = cv2.getStructuringElement(kernel_shape, (2 * kernel_size_dil + 1, 2 * kernel_size_dil + 1), (kernel_size_dil, kernel_size_dil))
    kernel_erode = cv2.getStructuringElement(kernel_shape, (2 * kernel_size_erode + 1, 2 * kernel_size_erode + 1), (kernel_size_erode, kernel_size_erode))

    dilatation_dst = cv2.dilate(img_bitwise, kernel)
    erode_dst = cv2.erode(dilatation_dst, kernel_erode)

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(erode_dst, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

    height, width, _ = img_flip.shape
    marking = select_lines(lines, 3200, height)
    polygons = get_polygons(marking, height)


    #drawing polygons
    cv2.polylines(img_copy, polygons, True, (255, 0, 255), 2)

    #resizing and printing images
    #cv2.imshow('img', cv2.resize(img_copy, (1600, 900)))
    cv2.imshow('img', cv2.flip(img_copy, 0))
    #cv2.imshow('img', cv2.resize(img, (1600, 900)))
    #cv2.imshow('bitwise', cv2.resize(img_bitwise, (1600, 900)))
    #cv2.imshow('thresh', cv2.resize(thresh, (1600, 900)))
    #cv2.imshow('erode', cv2.resize(erode_dst, (1600, 900)))
    #cv2.imshow('croped', img_croped)
    cv2.imshow('Canny', cv2.flip(canny, 0))
    #cv2.imshow('bitwise', cv2.flip(img_bitwise, 0))
    cv2.imshow('thresh', cv2.flip(thresh, 0))
    #cv2.imshow('dilation', cv2.flip(dilatation_dst, 0))
    #cv2.imshow('erode', cv2.flip(erode_dst, 0))
    time.sleep(1)

    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()
