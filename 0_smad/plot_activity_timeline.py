import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np

def plot_timeline(csv_file, output_file, filtered_csv=None):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Create time points for interpolation
    time_points = np.linspace(df['start_time_s'].min(), df['end_time_s'].max(), 1000)
    
    # Create arrays for music and speech probabilities
    music_interp = np.interp(time_points, df['start_time_s'], df['music_prob'])
    speech_interp = np.interp(time_points, df['start_time_s'], df['speech_prob'])
    
    # Apply smoothing using rolling average
    window_size = 31  # Adjust this value to control smoothing amount
    music_smooth = pd.Series(music_interp).rolling(window=window_size, center=True).mean()
    speech_smooth = pd.Series(speech_interp).rolling(window=window_size, center=True).mean()
    
    # Create a figure and axis
    fig, ax = plt.subplots()

    # If filtered CSV is provided, add highlight rectangles
    if filtered_csv:
        filtered_df = pd.read_csv(filtered_csv)
        for _, row in filtered_df.iterrows():
            ax.axvspan(row['start_time'], row['end_time'], 
                      alpha=0.2, color='lightgreen')
    
    # Plot smooth curves
    ax.plot(time_points, music_smooth, color='blue', label='Music')
    ax.plot(time_points, speech_smooth, color='red', label='Speech')
    
    # Add labels and title
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Probability')
    ax.set_title('Music and Speech Activity Timeline')
    
    # Add legend
    ax.legend()
    
    # Save the plot as a PNG file
    plt.savefig(output_file)

if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print("Usage: python script.py <csv_file> <output_file> [filtered_csv]")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    output_file = sys.argv[2]
    filtered_csv = sys.argv[3] if len(sys.argv) == 4 else None
    
    plot_timeline(csv_file, output_file, filtered_csv)