import asyncio

async def say_hello():
    for i in range(3):
        await asyncio.sleep(2)
        print(f"Hello {i}")

async def say_world():
    for i in range(3):
        await asyncio.sleep(1)
        print(f"World {i}")

async def main():
    # Schedule both tasks to run concurrently
    task1 = asyncio.create_task(say_hello())
    task2 = asyncio.create_task(say_world())

    await task1
    await task2

# Run the main function
asyncio.run(main())