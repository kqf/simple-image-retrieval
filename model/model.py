import torch
import torchvision


def classifier():
    backbone = torchvision.models.resnet50()
    backbone.fc = torch.nn.Linear(backbone.fc.in_features, 2)
    return backbone
