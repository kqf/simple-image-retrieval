import cv2


def write(img, imgpath):
    imgpath.parent.mkdir(parents=True, exist_ok=True)

    # Convert to channels last
    image_channels_last = img.transpose(1, 2, 0)

    # Convert to BGR
    bgr_channel_last = cv2.cvtColor(image_channels_last, cv2.COLOR_RGB2BGR)

    # Write it to be compatible with other formats
    cv2.imwrite(str(imgpath), bgr_channel_last)


def read(imgpath):
    # By default OpenCV uses BGR color space for color images,
    # so we need to convert the image to RGB color space.
    image_channels_last = cv2.imread(str(imgpath), cv2.COLOR_BGR2RGB)
    image = image_channels_last.transpose(2, 0, 1)
    return image
