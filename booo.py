import matplotlib.pyplot as plt
import numpy as np
import time

# Bubble Sort Algorithm with Visualization
def bubble_sort_visualize(arr):
    n = len(arr)
    swapped = True

    # Create a figure and axis for the plot
    fig, ax = plt.subplots()
    bars = ax.bar(range(len(arr)), arr, align='center')
    
    # Setting the y-axis limit
    ax.set_ylim(0, max(arr) + 1)
    
    # Display the initial state
    plt.pause(0.1)

    # Bubble Sort Algorithm
    while swapped:
        swapped = False
        for i in range(1, n):
            if arr[i - 1] > arr[i]:
                arr[i - 1], arr[i] = arr[i], arr[i - 1]  # Swap elements
                swapped = True
                
                # Update the bars with the current state of the array
                for bar, val in zip(bars, arr):
                    bar.set_height(val)
                
                # Redraw the plot
                plt.pause(0.1)
        
        # Reduce the range of comparison by one after each pass
        n -= 1

    # Show the final sorted array
    plt.show()

# Generate a random array
np.random.seed(0)
arr = np.random.randint(1, 50, 10)

# Run the bubble sort visualization
bubble_sort_visualize(arr)
