#!/usr/bin/env python3
"""
Performance test for projects API.
"""
import time
import requests
import statistics
from typing import List, Dict
import sys

# Configuration
BASE_URL = "http://localhost:8000"  # Adjust if needed
ENDPOINTS = [
    "/api/v1/projects",
    "/api/v1/projects?limit=10",
    "/api/v1/projects?technology=python",
    "/api/v1/projects?search=test",
]

def test_endpoint(endpoint: str, iterations: int = 5) -> Dict:
    """Test a single endpoint and return performance metrics."""
    url = f"{BASE_URL}{endpoint}"
    times = []
    successes = 0
    
    print(f"Testing {url}...")
    
    for i in range(iterations):
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            elapsed = (time.time() - start_time) * 1000  # Convert to ms
            
            if response.status_code == 200:
                times.append(elapsed)
                successes += 1
                print(f"  Iteration {i+1}: {elapsed:.2f} ms")
            else:
                print(f"  Iteration {i+1}: Failed with status {response.status_code}")
        except Exception as e:
            print(f"  Iteration {i+1}: Error - {e}")
    
    if times:
        return {
            "endpoint": endpoint,
            "success_rate": (successes / iterations) * 100,
            "avg_time_ms": statistics.mean(times),
            "min_time_ms": min(times),
            "max_time_ms": max(times),
            "median_time_ms": statistics.median(times),
            "std_dev_ms": statistics.stdev(times) if len(times) > 1 else 0,
            "sample_size": len(times),
        }
    else:
        return {
            "endpoint": endpoint,
            "success_rate": 0,
            "avg_time_ms": 0,
            "min_time_ms": 0,
            "max_time_ms": 0,
            "median_time_ms": 0,
            "std_dev_ms": 0,
            "sample_size": 0,
        }

def main():
    """Run performance tests on all endpoints."""
    print("=" * 60)
    print("Performance Test for Projects API")
    print("=" * 60)
    
    results = []
    
    for endpoint in ENDPOINTS:
        result = test_endpoint(endpoint)
        results.append(result)
        print()
    
    # Print summary
    print("=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    
    for result in results:
        print(f"\nEndpoint: {result['endpoint']}")
        print(f"  Success Rate: {result['success_rate']:.1f}%")
        print(f"  Average Time: {result['avg_time_ms']:.2f} ms")
        print(f"  Min Time: {result['min_time_ms']:.2f} ms")
        print(f"  Max Time: {result['max_time_ms']:.2f} ms")
        print(f"  Median Time: {result['median_time_ms']:.2f} ms")
        print(f"  Std Dev: {result['std_dev_ms']:.2f} ms")
        print(f"  Samples: {result['sample_size']}")
    
    # Check if any endpoint is too slow (> 500ms)
    slow_endpoints = [r for r in results if r['avg_time_ms'] > 500]
    if slow_endpoints:
        print(f"\n⚠️  WARNING: {len(slow_endpoints)} endpoint(s) are slow (> 500ms):")
        for r in slow_endpoints:
            print(f"  - {r['endpoint']}: {r['avg_time_ms']:.2f} ms")
        return 1
    else:
        print("\n✅ All endpoints are performing well (< 500ms)")
        return 0

if __name__ == "__main__":
    sys.exit(main())