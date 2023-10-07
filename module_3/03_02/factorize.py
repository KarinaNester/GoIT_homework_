import multiprocessing
from time import time

def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(numbers, num_processes):
    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.map(factorize, numbers)
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":
    numbers_to_factorize = [128, 255, 99999, 10651060]

    # Synchronous version
    start_time_sync = time()
    factors_sync = [factorize(num) for num in numbers_to_factorize]
    end_time_sync = time()
    print("Synchronous version:")
    for num, factors in zip(numbers_to_factorize, factors_sync):
        print(f"Factors of {num}: {factors}")
    print(f"Time taken (synchronous): {end_time_sync - start_time_sync} seconds")

    # Parallel version
    num_processes = multiprocessing.cpu_count()
    start_time_parallel = time()
    factors_parallel = factorize_parallel(numbers_to_factorize, num_processes)
    end_time_parallel = time()
    print("\nParallel version:")
    for num, factors in zip(numbers_to_factorize, factors_parallel):
        print(f"Factors of {num}: {factors}")
    print(f"Time taken (parallel): {end_time_parallel - start_time_parallel} seconds")
