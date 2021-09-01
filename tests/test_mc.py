from model.mc import blob2image, make_blob
import matplotlib.pyplot as plt


def test_blob():
    blob = make_blob()
    image = blob2image(blob)
    plt.imshow(image)
    plt.show()
