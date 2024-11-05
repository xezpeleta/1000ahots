import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_timeline(csv_file, output_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Create a figure and axis
    fig, ax = plt.subplots()
    
    # Plot music probability
    for index, row in df.iterrows():
        ax.plot([row['start_time_s'], row['end_time_s']], [row['music_prob'], row['music_prob']], color='blue', label='Music' if index == 0 else "")
    
    # Plot speech probability
    for index, row in df.iterrows():
        ax.plot([row['start_time_s'], row['end_time_s']], [row['speech_prob'], row['speech_prob']], color='red', label='Speech' if index == 0 else "")
    
    # Add labels and title
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Probability')
    ax.set_title('Music and Speech Activity Timeline')
    
    # Add legend
    ax.legend()
    
    # Save the plot as a PNG file
    plt.savefig(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file> <output_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    output_file = sys.argv[2]
    plot_timeline(csv_file, output_file)