"""
Asyncio Library Examples
========================


"""

import asyncio
import time
import random
from typing import List


# Example 1: Basic async function
async def fetch_data(url: str, delay: float = 1.0) -> str:
    """Simulate fetching data from a URL with a delay."""
    print(f"Fetching data from {url}...")
    await asyncio.sleep(delay)  # Simulate network delay
    return f"Data from {url}"


# Example 2: Sequential vs Concurrent execution
async def sequential_example():
    """Run tasks one after another (slow)."""
    print("\n=== Sequential Execution ===")
    start_time = time.time()
    
    # Run tasks one by one
    result1 = await fetch_data("api1.com", 1.0)
    result2 = await fetch_data("api2.com", 1.0)
    result3 = await fetch_data("api3.com", 1.0)
    
    end_time = time.time()
    print(f"Sequential execution took: {end_time - start_time:.2f} seconds")
    print(f"Results: {result1}, {result2}, {result3}")


async def concurrent_example():
    """Run tasks concurrently (fast)."""
    print("\n=== Concurrent Execution ===")
    start_time = time.time()
    
    # Run tasks concurrently using asyncio.gather()
    results = await asyncio.gather(
        fetch_data("api1.com", 1.0),
        fetch_data("api2.com", 1.0),
        fetch_data("api3.com", 1.0)
    )
    
    end_time = time.time()
    print(f"Concurrent execution took: {end_time - start_time:.2f} seconds")
    print(f"Results: {results}")


# Example 3: Creating and managing tasks
async def task_management_example():
    """Demonstrate task creation and management."""
    print("\n=== Task Management ===")
    
    # Create tasks
    task1 = asyncio.create_task(fetch_data("task1.com", 2.0))
    task2 = asyncio.create_task(fetch_data("task2.com", 1.5))
    
    # Do other work while tasks run in background
    print("Tasks are running in background...")
    await asyncio.sleep(0.5)
    print("Still working on other things...")
    
    # Wait for tasks to complete
    result1 = await task1
    result2 = await task2
    
    print(f"Task results: {result1}, {result2}")


# Example 4: Timeout handling
async def timeout_example():
    """Demonstrate timeout handling."""
    print("\n=== Timeout Example ===")
    
    try:
        # This will timeout after 2 seconds
        result = await asyncio.wait_for(
            fetch_data("slow-api.com", 5.0), 
            timeout=2.0
        )
        print(f"Got result: {result}")
    except asyncio.TimeoutError:
        print("Request timed out after 2 seconds")


# Example 5: Async context manager
class AsyncResource:
    """Example async context manager."""
    
    async def __aenter__(self):
        print("Acquiring resource...")
        await asyncio.sleep(0.1)  # Simulate setup
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource...")
        await asyncio.sleep(0.1)  # Simulate cleanup


async def context_manager_example():
    """Demonstrate async context manager usage."""
    print("\n=== Async Context Manager ===")
    
    async with AsyncResource() as resource:
        print("Using the resource...")
        await asyncio.sleep(1.0)
        print("Resource usage complete")


# Example 6: Producer-Consumer pattern
async def producer(queue: asyncio.Queue, count: int):
    """Produce items and put them in the queue."""
    for i in range(count):
        item = f"item-{i}"
        await queue.put(item)
        print(f"Produced: {item}")
        await asyncio.sleep(0.5)  # Simulate work
    
    # Signal completion
    await queue.put(None)


async def consumer(queue: asyncio.Queue):
    """Consume items from the queue."""
    while True:
        item = await queue.get()
        if item is None:
            break
        
        print(f"Consumed: {item}")
        await asyncio.sleep(0.3)  # Simulate processing
        queue.task_done()


async def producer_consumer_example():
    """Demonstrate producer-consumer pattern."""
    print("\n=== Producer-Consumer Pattern ===")
    
    queue = asyncio.Queue(maxsize=3)
    
    # Start producer and consumer tasks
    producer_task = asyncio.create_task(producer(queue, 5))
    consumer_task = asyncio.create_task(consumer(queue))
    
    # Wait for producer to finish
    await producer_task
    await consumer_task


# Example 7: Error handling in async code
async def unreliable_service(delay: float, should_fail: bool = False):
    """Simulate an unreliable service that might fail."""
    await asyncio.sleep(delay)
    if should_fail:
        raise Exception("Service failed!")
    return f"Success after {delay}s"


async def error_handling_example():
    """Demonstrate error handling in async code."""
    print("\n=== Error Handling ===")
    
    tasks = [
        asyncio.create_task(unreliable_service(1.0, False)),
        asyncio.create_task(unreliable_service(0.5, True)),
        asyncio.create_task(unreliable_service(1.5, False)),
    ]
    
    # Wait for all tasks, return results and exceptions
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
        else:
            print(f"Task {i} succeeded: {result}")


# Example 8: Semaphore for limiting concurrency
async def worker_with_semaphore(semaphore: asyncio.Semaphore, worker_id: int):
    """Worker that uses semaphore to limit concurrent access."""
    async with semaphore:
        print(f"Worker {worker_id} starting...")
        await asyncio.sleep(random.uniform(1, 3))
        print(f"Worker {worker_id} finished")


async def semaphore_example():
    """Demonstrate semaphore for limiting concurrency."""
    print("\n=== Semaphore Example ===")
    
    # Limit to 2 concurrent workers
    semaphore = asyncio.Semaphore(2)
    
    # Create 5 workers
    tasks = [
        asyncio.create_task(worker_with_semaphore(semaphore, i))
        for i in range(5)
    ]
    
    await asyncio.gather(*tasks)


# Main function to run all examples
async def main():
    """Run all asyncio examples."""
    print("🚀 Asyncio Library Examples")
    print("=" * 50)
    
    # Run examples
    await sequential_example()
    await concurrent_example()
    await task_management_example()
    await timeout_example()
    await context_manager_example()
    await producer_consumer_example()
    await error_handling_example()
    await semaphore_example()
    
    print("\n✅ All examples completed!")


# Run the examples if this file is executed directly
if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
