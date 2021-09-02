from model.mc import blob2image, make_blob
import matplotlib.pyplot as plt


def test_blob():
    blob1 = make_blob()
    blob2 = make_blob(0.8, 0.8, 0.08, 0.1)
    image = blob2image(blob1 + blob2)
    plt.imshow(image)
    plt.show()
