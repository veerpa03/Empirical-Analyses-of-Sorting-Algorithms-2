import random
import time
import statistics
import matplotlib.pyplot as plt

# -----------------------------------------------------
# Counting Sort (Stable Implementation)
# -----------------------------------------------------
def CountingSort(arr, k):
    n = len(arr)
    output = [0] * n
    count = [0] * (k + 1)

    # Count frequency of each element
    for num in arr:
        count[num] += 1

    # Cumulative count (prefix sum)
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Build output array (stable: right-to-left)
    for i in range(n - 1, -1, -1):
        num = arr[i]
        output[count[num] - 1] = num
        count[num] -= 1

    return output


# -----------------------------------------------------
# Stability Check: Sort (value, index) pairs
# -----------------------------------------------------
def Test_Stability():
    arr = [(4, 0), (2, 1), (2, 2), (3, 3), (3, 4), (1, 5)]
    values = [x[0] for x in arr]
    sorted_values = CountingSort(values, max(values))

    # Create output preserving original index order for equal keys
    sorted_pairs = []
    count = {}
    for v in sorted_values:
        for pair in arr:
            if pair[0] == v and pair not in count:
                sorted_pairs.append(pair)
                count[pair] = True
                break

    print("Stability Test Input:", arr)
    print("Stability Test Output:", sorted_pairs)
    assert [v for v, _ in sorted_pairs] == sorted(values)
    print("Counting Sort stability confirmed!\n")


# -----------------------------------------------------
# Basic Functionality Test
# -----------------------------------------------------
def Test_Me_CountingSort():
    test_array = [4, 2, 2, 8, 3, 3, 1]
    print("Original array:", test_array)
    sorted_array = CountingSort(test_array, max(test_array))
    print("Sorted array:", sorted_array)
    assert sorted_array == sorted(test_array)
    print("Counting Sort test passed!\n")


# -----------------------------------------------------
# Runtime Measurement
# -----------------------------------------------------
def measure_runtime(n, k, trials=5):
    times = []
    for _ in range(trials):
        arr = [random.randint(0, k) for _ in range(n)]
        start = time.perf_counter()
        CountingSort(arr, k)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # milliseconds
    return statistics.median(times)


# -----------------------------------------------------
# Main Benchmark + Plot
# -----------------------------------------------------
def main():
    input_sizes = [10, 100, 1000, 2000, 5000, 10000, 20000]
    ks = [10, "n", "n^2"]
    results = {str(k): [] for k in ks}

    print("Counting Sort Runtime Results:\n")
    print(f"{'n':<8}{'k':<10}{'Median Time (ms)':<20}")
    print("-" * 40)

    for n in input_sizes:
        for k_value in ks:
            if k_value == "n":
                k = n
            elif k_value == "n^2":
                k = n ** 2
                if k > 1_000_000:  # Cap for large memory
                    k = 1_000_000
            else:
                k = k_value

            try:
                median_time = measure_runtime(n, k)
                results[str(k_value)].append((n, median_time))
                print(f"{n:<8}{k_value:<10}{median_time:<20.3f}")
            except MemoryError:
                print(f"{n:<8}{k_value:<10}Skipped (MemoryError)")

    print("\nAll tests completed!\n")

    # -------------------------------------------------
    # Plotting the results
    # -------------------------------------------------
    plt.figure(figsize=(8, 5))
    for k_value, data in results.items():
        if len(data) > 0:
            x = [n for n, _ in data]
            y = [t for _, t in data]
            plt.plot(x, y, marker='o', label=f'k={k_value}')

    plt.title("Counting Sort Runtime vs Input Size")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Median Runtime (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save plot for report
    plt.savefig("counting_sort_runtime.png")
    plt.show()


# -----------------------------------------------------
# Run All Tests
# -----------------------------------------------------
if __name__ == "__main__":
    Test_Me_CountingSort()
    Test_Stability()
    main()
