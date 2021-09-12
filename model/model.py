import skorch
import torch
import torchvision

from model.loss import RetrievalLoss


class Classifier(torch.nn.Module):
    def __init__(self, n_outputs=2):
        super().__init__()
        backbone = torchvision.models.resnet50()
        backbone.fc = torch.nn.Linear(backbone.fc.in_features, n_outputs)
        self.backbone = backbone

    def forward(self, x):
        return self.backbone(x.float())


def build_model(lr=1e-3, max_epochs=2):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = skorch.NeuralNetClassifier(
        module=Classifier,
        module__n_outputs=100,
        criterion=RetrievalLoss,
        optimizer=torch.optim.Adam,
        optimizer__lr=lr,
        train_split=None,
        max_epochs=max_epochs,
        batch_size=8,
        iterator_train__shuffle=True,
        iterator_valid__shuffle=False,
        device=device,
    )
    return model
