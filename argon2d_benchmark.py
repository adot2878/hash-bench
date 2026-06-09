import csv
import time
from argon2.low_level import Type, hash_secret_raw


def benchmark_argon2d(duration_sec=30, time_cost=1, memory_cost=32 * 1024, threads=4, hash_len=32):
    password = b"benchmark-password"
    salt = b"benchmark-salt-123456"

    records = []
    start = time.perf_counter()
    iteration = 0

    while True:
        iter_start = time.perf_counter()
        hash_secret_raw(password, salt, time_cost, memory_cost, threads, hash_len, Type.D)
        iter_end = time.perf_counter()

        elapsed = iter_end - iter_start
        records.append(elapsed)
        iteration += 1

        if iter_end - start >= duration_sec:
            break

    total_time = time.perf_counter() - start
    average = sum(records) / len(records)
    minimum = min(records)
    maximum = max(records)

    return {
        "algorithm": "Argon2d",
        "time_cost": time_cost,
        "memory_cost_kib": memory_cost,
        "threads": threads,
        "hash_len": hash_len,
        "duration_sec": round(total_time, 6),
        "iterations": iteration,
        "avg_sec": round(average, 6),
        "min_sec": round(minimum, 6),
        "max_sec": round(maximum, 6),
    }


def write_results(path, summary, records):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["field", "value"])
        for key, value in summary.items():
            writer.writerow([key, value])
        writer.writerow([])
        writer.writerow(["iteration", "elapsed_sec"])
        for idx, elapsed in enumerate(records, start=1):
            writer.writerow([idx, round(elapsed, 6)])


def main():
    duration_sec = 30
    summary = benchmark_argon2d(duration_sec=duration_sec)
    print("Benchmark complete:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    results_path = "argon2d_benchmark_results.csv"
    write_results(results_path, summary, summary_records)
    print(f"Results saved to {results_path}")


if __name__ == "__main__":
    summary_records = []
    password = b"benchmark-password"
    salt = b"benchmark-salt-123456"
    duration_sec = 30
    time_cost = 1
    memory_cost = 32 * 1024
    threads = 4
    hash_len = 32

    start = time.perf_counter()
    while True:
        iter_start = time.perf_counter()
        hash_secret_raw(password, salt, time_cost, memory_cost, threads, hash_len, Type.D)
        iter_end = time.perf_counter()

        elapsed = iter_end - iter_start
        summary_records.append(elapsed)
        if iter_end - start >= duration_sec:
            break

    total_time = time.perf_counter() - start
    summary = {
        "algorithm": "Argon2d",
        "time_cost": time_cost,
        "memory_cost_kib": memory_cost,
        "threads": threads,
        "hash_len": hash_len,
        "duration_sec": round(total_time, 6),
        "iterations": len(summary_records),
        "avg_sec": round(sum(summary_records) / len(summary_records), 6),
        "min_sec": round(min(summary_records), 6),
        "max_sec": round(max(summary_records), 6),
    }

    results_path = "argon2d_benchmark_results.csv"
    write_results(results_path, summary, summary_records)
    print("Benchmark complete:")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print(f"Results saved to {results_path}")
