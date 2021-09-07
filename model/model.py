import skorch
import torch
import torchvision


class Classifier(torch.nn.Module):
    def __init__(self):
        super().__init__()
        backbone = torchvision.models.resnet50()
        backbone.fc = torch.nn.Linear(backbone.fc.in_features, 2)
        self.backbone = backbone

    def forward(self, x):
        x = x[:, None].repeat(1, 3, 1, 1)
        return self.backbone(x)


def build_model(lr=1e-4):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = skorch.NeuralNetClassifier(
        module=Classifier,
        criterion=torch.nn.CrossEntropyLoss,
        optimizer=torch.optim.Adam,
        optimizer__lr=lr,
        train_split=None,
        max_epochs=2,
        batch_size=256,
        iterator_train__shuffle=True,
        iterator_valid__shuffle=False,
        device=device,
    )
    return model
