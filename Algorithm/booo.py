import matplotlib.pyplot as plt
import numpy as np
import time

def bubble_sort_visualize(arr):
    n = len(arr)
    swapped = True

    fig, ax = plt.subplots()
    bars = ax.bar(range(len(arr)), arr, align='center')
    
    ax.set_ylim(0, max(arr) + 1)
    
    plt.pause(0.1)

    while swapped:
        swapped = False
        for i in range(1, n):
            if arr[i - 1] > arr[i]:
                arr[i - 1], arr[i] = arr[i], arr[i - 1]  
                swapped = True
                
                for bar, val in zip(bars, arr):
                    bar.set_height(val)
                
                plt.pause(0.1)
        
        n -= 1

    plt.show()

np.random.seed(0)
arr = np.random.randint(1, 1000, 100)

bubble_sort_visualize(arr)
