import cv2
import pickle
import cvzone


cap = cv2.VideoCapture('data/carpark.mp4')

with open('data/coords/CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 18, 42


def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y+height, x:x+width]
        count = cv2.countNonZero(imgCrop)

        color = (0, 255, 0) if count < 15 else (0, 0, 255)
        thickness = 2
        if count < 15:
            spaceCounter += 1

        cv2.rectangle(img, pos, (x + width, y + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 10), scale=1, thickness=1, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (50, 50), scale=2, thickness=3, offset=10, colorR=(0, 200, 0))


# Создаем настраиваемое окно с рамкой
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

# Получаем разрешение экрана (например, 1920x1080)
screenWidth = 1920
screenHeight = 1080
cv2.resizeWindow("Image", screenWidth, screenHeight)


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    if not success:
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThresh, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    cv2.imshow("Image", img)
    cv2.waitKey(10)
    if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
