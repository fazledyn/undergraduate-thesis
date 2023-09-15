import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import metrics

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

SEED = 1234

csv_file = "../merged_csv.csv"
df = pd.read_csv(csv_file)

X = df[ ['comment_pos', 'comment_neg'] ]
y = df["polarity_class"]

scaler = MinMaxScaler()
X = scaler.fit_transform(X)

std_scaler = StandardScaler()
X = std_scaler.fit_transform(X)

print("Scaled X")
print(X)

N_CLASSES = 4

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEED)

# Define the model architecture
class NeuralNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# Convert the labels to one-hot encoding
def to_one_hot(labels, num_classes):
    return F.one_hot(labels, num_classes)

# Define the model and optimizer
model = NeuralNetwork(2, 64, N_CLASSES)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# print("Before conversion")
# # Convert the data to PyTorch tensors
x_train = torch.tensor(X_train).float()
y_train = torch.tensor(y_train.tolist()).long()
x_test = torch.tensor(X_test).float()
y_test = torch.tensor(y_test.tolist()).long()
# print("After conversion")

# Convert the labels to one-hot encoding
y_train_one_hot = to_one_hot(y_train, num_classes=N_CLASSES)

# Train the model
for epoch in range(200):
    optimizer.zero_grad()
    outputs = model(x_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

# Convert the test labels to one-hot encoding
y_test_one_hot = to_one_hot(y_test, num_classes=N_CLASSES)

# Evaluate the model
with torch.no_grad():
    outputs = model(x_test)
    _, predicted = torch.max(outputs.data, 1)
    accuracy = (predicted == y_test).sum().item() / len(y_test)

    conf_mat = metrics.confusion_matrix(y_test, predicted)
    conf_dis = metrics.ConfusionMatrixDisplay(conf_mat)
    conf_dis.plot()

    plt.title("Neural Network Classifier")
    plt.savefig("./nn_50_crossent.png")

    with open("./nn_50_crossent.txt", "w") as f:
        f.write(metrics.classification_report(y_test, predicted))

print("Test accuracy:", accuracy)
