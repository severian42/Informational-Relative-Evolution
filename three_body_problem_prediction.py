import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Constants
G = 1  # Gravitational constant (normalized)
m1, m2, m3 = 1, 1, 1  # Equal masses
dt = 0.001  # Higher accuracy time step
steps = 10000  # More steps for extended tracking
num_seeds = 10  # Run experiment across multiple random seeds for robustness

# Function to compute gravitational force
def gravitational_force(ri, rj, mj):
    diff = rj - ri
    dist = np.linalg.norm(diff) + 1e-9  # Avoid division by zero
    return G * mj * diff / dist**3

# Function to compute chaos measure
def compute_chaos_measure(r1, r2, r3, v1, v2, v3):
    r12, r13, r23 = r2 - r1, r3 - r1, r3 - r2
    chaos = np.sum([
        np.abs(np.cross(v1, r12)) / (np.linalg.norm(r12)**2 + 1e-9),
        np.abs(np.cross(v1, r13)) / (np.linalg.norm(r13)**2 + 1e-9),
        np.abs(np.cross(v2, r23)) / (np.linalg.norm(r23)**2 + 1e-9),
        np.abs(np.cross(v3, -r13)) / (np.linalg.norm(r13)**2 + 1e-9),
        np.abs(np.cross(v3, -r23)) / (np.linalg.norm(r23)**2 + 1e-9),
    ])
    return 0.2 * chaos  # Scaling factor for interpretability

# Function to compute IRE coherence field
def compute_ire_field(r1, r2, r3, x, sigma=0.5, C_t=0):
    dist_sum = np.sum([
        np.linalg.norm(x - r1)**2,
        np.linalg.norm(x - r2)**2,
        np.linalg.norm(x - r3)**2
    ])
    return np.exp(-dist_sum / (2 * sigma**2)) * np.exp(-C_t / 2)

# Storage for multiple runs
all_metrics = []

# Loop through multiple seeded experiments
for seed in range(num_seeds):
    np.random.seed(seed)  # Set seed for reproducibility
    
    # Generate challenging initial conditions
    r1 = np.random.uniform(-1, 1, 3)
    r2 = np.random.uniform(-1, 1, 3)
    r3 = np.random.uniform(-1, 1, 3)
    
    v1 = np.random.uniform(-0.1, 0.1, 3)
    v2 = np.random.uniform(-0.1, 0.1, 3)
    v3 = np.random.uniform(-0.1, 0.1, 3)

    # Data storage for this run
    positions1, positions2, positions3 = [r1.copy()], [r2.copy()], [r3.copy()]
    coherence_values, psi_values = [], []

    # Controlled simulation loop
    for _ in range(steps):
        # Compute gravitational forces
        F12 = gravitational_force(r1, r2, m2)
        F13 = gravitational_force(r1, r3, m3)
        F21 = gravitational_force(r2, r1, m1)
        F23 = gravitational_force(r2, r3, m3)
        F31 = gravitational_force(r3, r1, m1)
        F32 = gravitational_force(r3, r2, m2)

        # Update velocities
        v1 += (F12 + F13) * dt
        v2 += (F21 + F23) * dt
        v3 += (F31 + F32) * dt

        # Update positions
        r1 += v1 * dt
        r2 += v2 * dt
        r3 += v3 * dt

        # Store data
        positions1.append(r1.copy())
        positions2.append(r2.copy())
        positions3.append(r3.copy())

        # Compute coherence and IRE field
        C_t = compute_chaos_measure(r1, r2, r3, v1, v2, v3)
        coherence_values.append(C_t)
        psi_cm = compute_ire_field(r1, r2, r3, (r1 + r2 + r3) / 3, sigma=0.5, C_t=C_t)
        psi_values.append(psi_cm)

    # Convert data to arrays
    positions1 = np.array(positions1)
    positions2 = np.array(positions2)
    positions3 = np.array(positions3)
    coherence_values = np.array(coherence_values)
    psi_values = np.array(psi_values)

    # Compute evaluation metrics for this run
    mse_prediction = mean_squared_error(positions1[2:], positions1[1:-1] + (positions1[1:-1] - positions1[:-2]))
    coherence_stability = np.std(coherence_values) / np.mean(coherence_values) * 100  # % fluctuation
    prediction_accuracy = 100 - (mse_prediction * 10000)  # Scale accuracy from 0-100%

    # Store results
    all_metrics.append({
        "Seed": seed,
        "Mean Squared Error": mse_prediction,
        "Chaos Measure Stability (%)": coherence_stability,
        "Final IRE Field Value": psi_values[-1],
        "Overall Coherence Score": np.mean(coherence_values),
        "IRE Prediction Accuracy (%)": max(0, min(100, prediction_accuracy)),  # Ensure within bounds
    })

# Convert metrics to dataframe for visualization
metrics_df = pd.DataFrame(all_metrics)
print(metrics_df)

# Visualization: Top-down (XY-plane) view of the most chaotic run
worst_run_index = np.argmax(metrics_df["Chaos Measure Stability (%)"])
worst_seed = metrics_df.iloc[worst_run_index]["Seed"]

np.random.seed(int(worst_seed))  # Re-run the most chaotic case

# Generate challenging initial conditions
r1 = np.random.uniform(-1, 1, 3)
r2 = np.random.uniform(-1, 1, 3)
r3 = np.random.uniform(-1, 1, 3)
v1 = np.random.uniform(-0.1, 0.1, 3)
v2 = np.random.uniform(-0.1, 0.1, 3)
v3 = np.random.uniform(-0.1, 0.1, 3)

# Store positions for visualization
positions1, positions2, positions3 = [r1.copy()], [r2.copy()], [r3.copy()]

for _ in range(steps):
    # Compute forces and update system
    F12, F13, F21, F23, F31, F32 = gravitational_force(r1, r2, m2), gravitational_force(r1, r3, m3), gravitational_force(r2, r1, m1), gravitational_force(r2, r3, m3), gravitational_force(r3, r1, m1), gravitational_force(r3, r2, m2)
    v1, v2, v3 = v1 + (F12 + F13) * dt, v2 + (F21 + F23) * dt, v3 + (F31 + F32) * dt
    r1, r2, r3 = r1 + v1 * dt, r2 + v2 * dt, r3 + v3 * dt

    # Store positions
    positions1.append(r1.copy())
    positions2.append(r2.copy())
    positions3.append(r3.copy())

# Top-down visualization
plt.plot(np.array(positions1)[:, 0], np.array(positions1)[:, 1], 'r', label="Body 1")
plt.plot(np.array(positions2)[:, 0], np.array(positions2)[:, 1], 'g', label="Body 2")
plt.plot(np.array(positions3)[:, 0], np.array(positions3)[:, 1], 'b', label="Body 3")
plt.legend()
plt.show()

