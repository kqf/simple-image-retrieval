import skorch
import torch
import torchvision


def classfifier():
    backbone = torchvision.models.resnet50()
    backbone.fc = torch.nn.Linear(backbone.fc.in_features, 2)
    return backbone


def build_model(lr=1e-4):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = skorch.NeuralNetClassifier(
        module=classfifier(),
        criterion=torch.nn.CrossEntropyLoss,
        optimizer=torch.optim.Adam,
        optimizer__lr=lr,
        max_epochs=2,
        batch_size=256,
        iterator_train__shuffle=True,
        iterator_valid__shuffle=False,
        device=device,
    )
    return model
