import cv2
import pickle


# Размер одного парковочного места
width, height = 18, 42

try:
    with open('data/coords/CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                break

    with open('data/coords/CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


# Создаем настраиваемое окно с рамкой
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

# Получаем разрешение экрана (например, 1920x1080)
screen_width = 1920
screen_height = 1080
cv2.resizeWindow("Image", screen_width, screen_height)

while True:
    img = cv2.imread('data/carparking.png')
    if img is None:
        print("Ошибка: изображение не найдено.")
        break

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)

    key = cv2.waitKey(1)
    if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
