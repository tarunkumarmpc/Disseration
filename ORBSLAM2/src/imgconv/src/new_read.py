import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

poses = pd.read_csv('04.txt', delimiter=' ', header=None)
print('Size of pose dataframe:', poses.shape)
poses.head()
first_pose = np.array(poses.iloc[0]).reshape((3,4)).round(2)
second_pose = np.array(poses.iloc[1]).reshape((3,4)).round(2)
print("First pose:\n", first_pose)
print("Second pose:\n",second_pose)
ground_truth = np.zeros((len(poses), 3, 4))

for i in range(len(poses)):
    ground_truth[i] = np.array(poses.iloc[i]).reshape((3, 4))


plt.plot(ground_truth[:,:,3][:,0], ground_truth[:,:,3][:,1])
plt.show()

