import cv2


def write(img, imgpath):
    imgpath.parent.mkdir(parents=True, exist_ok=True)
    img_ = cv2.cvtColor(img.transpose(1, 2, 0), cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(imgpath), img_)
