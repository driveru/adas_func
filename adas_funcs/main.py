import cv2
import numpy as np

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
img = cv2.imread(r'C:\Users\79042\Desktop\Screenshot_3.png')

#HoughLinesP setting
rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 25  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 80  # minimum number of pixels making up a line
max_line_gap = 15  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on

cv2.resizeWindow("settings", 480, 100)

while True:
    #uncoment to work with video
    #_, img = cap.read()

    #convert to hls color space
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    #creting a copy of image to draw lines
    img_copy = img.copy()

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

    if lines is None:
        lines = []

    #drawing lines
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img_copy, (x1,y1),(x2,y2),(255,0,0),2)

    #contours
    '''
    contours, hierarchy = cv2.findContours(erode_dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    marking = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            cv2.polylines(img_copy, contour, True, (0,255,255), 1)
            marking.append(contour)
    '''

    #resizing and printing images
    cv2.imshow('img', cv2.resize(img_copy, (1600, 900)))
    cv2.imshow('Canny', cv2.resize(canny, (1600, 900)))
    cv2.imshow('bitwise', cv2.resize(img_bitwise, (1600, 900)))
    cv2.imshow('thresh', cv2.resize(thresh, (1600, 900)))
    cv2.imshow('erode', cv2.resize(erode_dst, (1600, 900)))


    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()
