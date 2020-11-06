import torch
from torch import nn
import torchvision.models as models

class AlexNet(nn.Module):
    def __init__(self,num_classes=2):
        super(AlexNet,self).__init__()
        self.model_name = "AlexNet"
        model = models.alexnet(pretrained=True)
        for param in model.parameters():
            param.requires_grad = False
        model.classifier[-1] = nn.Linear(model.classifier[-1].in_features,num_classes)
        self.model = model

    def forward(self,x):
        return self.model(x)

if __name__=="__main__":
    net = AlexNet()
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    net.to(device)
    from torchsummary import summary
    print(summary(net,(3,224,224)))