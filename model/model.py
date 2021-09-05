import torchvision


def model():
    backbone = torchvision.models.resnet50()
    print(backbone)
    return backbone
