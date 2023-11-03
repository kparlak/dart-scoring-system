import cv2
import numpy as np

display_blur = False
display_thresh = False
display_edges = False
display_contours = False

display_src = False
display_dest = False

display_corr = False

image_src = cv2.imread('img_src.jpg')
image_dest = cv2.imread('img_dest.jpg')

image = image_src.copy()

def get_dartboard_ellipse(image, threshold):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Blur image
    kernel = np.ones((5, 5), np.float32) / 25
    blur = cv2.filter2D(image_hsv, -1, kernel)
    #blur = cv2.GaussianBlur(image_hsv, (3,3),0)
    #blur = cv2.bilateralFilter(image, 9, 75, 75)
    # Display blur
    if display_blur:
        resize = cv2.resize(blur, (0,0), fx=0.5, fy=0.5)
        cv2.imshow("BLUR", resize)

    h, s, image_cal = cv2.split(blur)
    # Find thresholds
    ret, thresh = cv2.threshold(image_cal, threshold, 255, cv2.THRESH_BINARY_INV)
    # Remove noise
    kernel = np.ones((3, 3), np.uint8)
    thresh_no_noise = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # Display thresholds
    if display_thresh:
        resize = cv2.resize(thresh_no_noise, (0,0), fx=0.5, fy=0.5)
        cv2.imshow("THRESH", resize)

    # Find edges
    edged = cv2.Canny(thresh_no_noise, 0, 255)
    # Display edges
    if display_edges:
        resize = cv2.resize(edged, (0,0), fx=0.5, fy=0.5)
        cv2.imshow("EDGES", resize)

    # Find contours
    contours, hierarchy = cv2.findContours(edged, 1, 2)
    contour = max(contours, key=cv2.contourArea)
    image_contour = image.copy()
    # Display contours
    if display_contours:
        cv2.drawContours(image_contour, contour, -1, (0, 255, 0), 3)
        resize = cv2.resize(image_contour, (0,0), fx=0.5, fy=0.5)
        cv2.imshow('CONTOURS', resize)

    ellipse = cv2.fitEllipse(contour)

    return ellipse

def get_dartboard_circle(image, threshold):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Blur image
    kernel = np.ones((5, 5), np.float32) / 25
    blur = cv2.filter2D(image_hsv, -1, kernel)
    #blur = cv2.GaussianBlur(image_hsv, (3,3),0)
    #blur = cv2.bilateralFilter(image, 9, 75, 75)
    # Display blur
    if display_blur:
        resize = cv2.resize(blur, (0,0), fx=0.5, fy=0.5)
        cv2.imshow("BLUR", resize)

    h, s, image_cal = cv2.split(blur)
    # Find thresholds
    ret, thresh = cv2.threshold(image_cal, threshold, 255, cv2.THRESH_BINARY_INV)
    # Remove noise
    kernel = np.ones((3, 3), np.uint8)
    thresh_no_noise = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # Display thresholds
    if display_thresh:
        resize = cv2.resize(thresh_no_noise, (0,0), fx=0.5, fy=0.5)
        cv2.imshow("THRESH", resize)

    # Find edges
    edged = cv2.Canny(thresh_no_noise, 0, 255)
    # Display edges
    if display_edges:
        resize = cv2.resize(edged, (0,0), fx=0.5, fy=0.5)
        cv2.imshow("EDGES", resize)

    # Find contours
    contours, hierarchy = cv2.findContours(edged, 1, 2)
    contour = max(contours, key=cv2.contourArea)
    image_contour = image.copy()
    # Display contours
    if display_contours:
        cv2.drawContours(image_contour, contour, -1, (0, 255, 0), 3)
        resize = cv2.resize(image_contour, (0,0), fx=0.5, fy=0.5)
        cv2.imshow('CONTOURS', resize)

    (x, y), r = cv2.minEnclosingCircle(contour)

    return x, y, r

# Source coordinate frame
ellipse = get_dartboard_ellipse(image=image_src, threshold=70)
factor = 55
x, y = ellipse[0]
a, b = ellipse[1]
angle = ellipse[2]
top_src = x, y - a / 2
center_src = x, y - factor
bottom_src = x, y + a / 2
left_src = x - b / 2, y - factor
right_src = x + b / 2, y - factor

cv2.ellipse(image_src, ellipse, color=(0, 255, 0), thickness=2)
cv2.circle(image_src, (round(top_src[0]), round(top_src[1])), radius=10, color=(255, 0, 0), thickness=-1)
cv2.circle(image_src, (round(center_src[0]), round(center_src[1])), radius=10, color=(255, 0, 0), thickness=-1)
cv2.circle(image_src, (round(bottom_src[0]), round(bottom_src[1])), radius=10, color=(255, 0, 0), thickness=-1)
cv2.circle(image_src, (round(left_src[0]), round(left_src[1])), radius=10, color=(255, 0, 0), thickness=-1)
cv2.circle(image_src, (round(right_src[0]), round(right_src[1])), radius=10, color=(255, 0, 0), thickness=-1)
if display_src:
    resize = cv2.resize(image_src, (0,0), fx=0.5, fy=0.5)
    cv2.imshow("SOURCE", resize)

# Destination coordinate frame
x, y, r = get_dartboard_circle(image=image_dest, threshold=85)
top_dest = x, y - r
center_dest = x, y
bottom_dest = x, y + r
left_dest = x - r, y
right_dest = x + r, y

cv2.circle(image_dest, (round(x), round(y)), radius=int(r), color=(0, 255, 0), thickness=2)
cv2.circle(image_dest, (round(top_dest[0]), round(top_dest[1])), radius=10, color=(255, 0, 0), thickness=-1)
cv2.circle(image_dest, (round(center_dest[0]), round(center_dest[1])), radius=10, color=(255, 0, 0), thickness=-1)
cv2.circle(image_dest, (round(bottom_dest[0]), round(bottom_dest[1])), radius=10, color=(255, 0, 0), thickness=-1)
cv2.circle(image_dest, (round(left_dest[0]), round(left_dest[1])), radius=10, color=(255, 0, 0), thickness=-1)
cv2.circle(image_dest, (round(right_dest[0]), round(right_dest[1])), radius=10, color=(255, 0, 0), thickness=-1)
if display_dest:
    resize = cv2.resize(image_dest, (0,0), fx=0.5, fy=0.5)
    cv2.imshow("DEST", resize)

# Construct transformation vector
src_points = np.array([top_src, center_src, bottom_src, left_src, right_src])
dest_points = np.array([top_dest, center_dest, bottom_dest, left_dest, right_dest])

H, _ = cv2.findHomography(src_points, dest_points)
#print(H)

if display_corr:
    image_corr = cv2.warpPerspective(image, H, (image.shape[1], image.shape[0]))
    resize = cv2.resize(image_corr, (0,0), fx=0.5, fy=0.5)
    cv2.imshow("CORR", resize)

#test_in = np.array([800, 400, 1])
#test_out = np.dot(H, temp)
#test_out = test_out/test_out[2]

# Save matrix to text file
file = open('H.txt', 'w')
content = str(H)
file.write(content)
file.close()

file = open('H.txt', 'r')
content = file.read()
file.close()
print(content)

cv2.waitKey()
cv2.destroyAllWindows()

# EOF
