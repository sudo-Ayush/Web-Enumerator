import asyncio

async def print_with_sleep(x):
    for i in range(1,5):
        print("test async {test_num}".format(test_num=x))
        await asyncio.sleep(2)

async def run():
    task = []
    for i in range(1,5):
        task.append(print_with_sleep(i))
    await asyncio.gather(*task)

if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run())