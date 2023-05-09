import torch.nn as nn
from os.path import join, exists, abspath
import warnings
from skimage.io import imread
from skimage.transform import resize
from skimage.color import gray2rgb
from skimage.color import rgba2rgb
from skimage.color import rgb2gray
import torch

from Constants import MODEL_LIB, PRETRAIND_MODEL, MODEL_PATH, MODEL_NAME, THRESHOLD
warnings.filterwarnings("ignore")

class LungsModel:
    def __init__(self, size = (224, 224), modelType = "efficientnet"):
        self.model = torch.hub.load(MODEL_LIB, PRETRAIND_MODEL, pretrained=True)
        if modelType == "efficientnet":
            self.model.classifier.fc = nn.Sequential(
                nn.Linear(1792, 4),
                nn.Softmax()
            )
        elif modelType == "resnet":
            self.model.fc = torch.nn.Sequential(
                nn.Linear(2048, 1),
                nn.Sigmoid()
            )
        else:
            raise Exception("You have to download your model and change MODEL_LIB in Constants.py")
        self.model = self.model.double()
        self.model = self.model.eval()
        state_dict = torch.load(abspath(join(MODEL_PATH, MODEL_NAME)), map_location=torch.device('cpu'))
        self.model.load_state_dict(state_dict)
        self.model = self.model.eval()
        self.model.train(False)
        self.size = size

    def forward(self, file_name):
        if not exists(file_name):
            return 0
        image_obj = imread(file_name)
        if len(image_obj.shape) == 3 and image_obj.shape[-1] == 4:
            image_obj = rgba2rgb(image_obj)
        if len(image_obj.shape) == 3:
            image_obj = rgb2gray(image_obj)
        image_obj = gray2rgb(image_obj)
        image_obj = resize(image_obj, self.size, mode='constant', anti_aliasing=True,)
        img = torch.transpose(torch.transpose(torch.from_numpy(image_obj), 0, 2), 1, 2).unsqueeze(0)
        return self.model.forward(img).squeeze().detach().numpy()


'''
{'avg_loss': 0.8864293921202914,
 'accuracy': 0.8495460440985733,
 'f1_micro': 0.8495460440985731,
 'f1_macro': 0.8450114281424903,
 'precision_micro': 0.8495460440985733,
 'precision_macro': 0.8177207293232036,
 'recall_micro': 0.8495460440985733,
 'recall_macro': 0.8922673762296404,
 'ill score': 15.73469387755102}


{'avg_loss': 0.9422026015603204,
 'accuracy': 0.7976653696498055,
 'f1_micro': 0.7976653696498055,
 'f1_macro': 0.7644902379573053,
 'precision_micro': 0.7976653696498055,
 'precision_macro': 0.7428211151537611,
 'recall_micro': 0.7976653696498055,
 'recall_macro': 0.8280196742460894,
 'ill score': 15.73469387755102}
'''