from pathlib import Path
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image


class Classifier(nn.Module):

    def __init__(self):
        super(Classifier, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, 3)
        self.conv2 = nn.Conv2d(16, 32, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(p=0.25)

        self.fc1 = nn.Linear(32 * 5 * 5, 400)
        self.fc2 = nn.Linear(400, 10)

    def forward(self, x):
        x = self.dropout(self.pool(F.relu(self.conv1(x))))  # dim=(8x13x13)
        x = self.dropout(self.pool(F.relu(self.conv2(x))))  # dim=(16x5x5)

        x = x.view(x.size(0), -1)

        x = self.dropout(F.relu(self.fc1(x)))
        x = F.relu(self.fc2(x))
        x = F.log_softmax(x, dim=1)
        return x

    def load_model(self, model_path):
        if not Path(model_path).exists():
            raise FileNotFoundError("The provided path to the model does not exist")
        self.load_state_dict(torch.load(model_path))

    def predict(self, image):
        image_transforms = transforms.Compose([
            transforms.Resize((28, 28)),
            transforms.Grayscale(),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

        if not isinstance(image, Image.Image):
            image = Image.open(image)

        input_image = image_transforms(image)
        input_image = torch.unsqueeze(input_image, 0)

        self.eval()
        with torch.no_grad():
            output = self.forward(input_image)

        predicted_label = torch.argmax(output).item()

        return predicted_label
