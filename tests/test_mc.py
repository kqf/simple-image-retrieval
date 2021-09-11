from model.mc import blob2image, make_blob
import matplotlib.pyplot as plt


def test_blob():
    alpha = 0.6
    blob1 = make_blob(0.5 + alpha, 0.4, 0.5 - alpha, 0.5 + alpha)
    blob2 = make_blob(0.5, 0.5)
    image = blob2image(blob1 + blob2)
    plt.imshow(image.transpose(1, 2, 0), interpolation='nearest')
    plt.show()
