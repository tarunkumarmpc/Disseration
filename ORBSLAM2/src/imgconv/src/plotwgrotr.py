import pandas as pd
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt

def plot_csv_data(file1_path, file2_path):
    # Read the CSV files
    data1 = pd.read_csv(file1_path)
    data2 = pd.read_csv(file2_path)

    # Extract the x and y values from each dataset
    x1 = data1['g_x'].to_numpy()
    y1 = data1['g_y'].to_numpy()
    
    x2 = data2['position_y'].to_numpy()
    y2 = data2['position_x'].to_numpy()
    
    for i in range(len(y2)):
      y2[i] = -y2[i]

    # Plot the data with different colors
    plt.plot( x1, y1, color='blue', label='groundtruth')
    plt.plot( x2, y2, color='yellow', label='orb')

    # Add labels and legend
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()

    # Show the plot
    plt.show()

# Example usage
file1_path = 'ground_t_10.csv'
file2_path = 'pose_data_10.csv'
plot_csv_data(file1_path, file2_path)
