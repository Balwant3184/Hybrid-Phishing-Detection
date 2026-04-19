import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import random

# Load dataset
data = pd.read_csv("data/phishing_dataset.csv")

X = data.drop("label", axis=1)

# Remove non-numeric columns
X = X.select_dtypes(include=[np.number])
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

n_particles = 10
n_features = X.shape[1]
n_iterations = 10

# Initialize particles (binary positions)
particles = np.random.randint(2, size=(n_particles, n_features))
velocities = np.random.rand(n_particles, n_features)

pbest = particles.copy()
pbest_scores = np.zeros(n_particles)

gbest = None
gbest_score = 0

def fitness(position):
    selected = [i for i in range(len(position)) if position[i] == 1]
    if len(selected) == 0:
        return 0
    model = RandomForestClassifier()
    model.fit(X_train.iloc[:, selected], y_train)
    preds = model.predict(X_test.iloc[:, selected])
    return accuracy_score(y_test, preds)

# Evaluate initial particles
for i in range(n_particles):
    score = fitness(particles[i])
    pbest_scores[i] = score

best_index = np.argmax(pbest_scores)
gbest = pbest[best_index]
gbest_score = pbest_scores[best_index]

# BPSO iterations
for iteration in range(n_iterations):
    print(f"Iteration {iteration+1}/{n_iterations} running...")
    for i in range(n_particles):
        r1 = random.random()
        r2 = random.random()

        velocities[i] = (
            velocities[i]
            + r1 * (pbest[i] - particles[i])
            + r2 * (gbest - particles[i])
        )

        sigmoid = 1 / (1 + np.exp(-velocities[i]))
        particles[i] = np.where(
            np.random.rand(n_features) < sigmoid, 1, 0
        )

        score = fitness(particles[i])

        if score > pbest_scores[i]:
            pbest[i] = particles[i].copy()
            pbest_scores[i] = score

    best_index = np.argmax(pbest_scores)
    if pbest_scores[best_index] > gbest_score:
        gbest = pbest[best_index]
        gbest_score = pbest_scores[best_index]

print("Best Accuracy after BPSO:", gbest_score)
selected_features = [X.columns[i] for i in range(n_features) if gbest[i] == 1]
print("Selected Features:", selected_features)