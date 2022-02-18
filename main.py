import threading
import queue

import random
import time

"""
Разработать программу, имитирующую работу склада (конвейера).

- Дано 3 производителя и 2 потребителя, все разные потоки и работают все одновременно.

    + Есть очередь с 200 элементами. Производители добавляют случайное число от 1…100, а потребители берут эти числа.

    + Если в очереди элементов >= 100 производители спят, если нет элементов в очереди - потребители спят.

    + Если элементов стало <= 80 производители просыпаются.
    
Все это работает до тех пор пока пользователь не нажал на кнопку “q”, после чего производители останавливаются, 
а потребители берут все элементы, только потом программа завершается. 
"""


def produce(queue, event):
    while not event.is_set():
        if queue.qsize() <= 80:
            item = random.randint(1, 100)
            queue.put(item)
        else:
            while not event.is_set() and queue.qsize() > 80:
                time.sleep(1)


def consume(queue, event):
    while not event.is_set():
        if not queue.empty():
            item = queue.get()
            time.sleep(0)


if __name__ == '__main__':
    queue = queue.Queue()
    for i in range(100):
        queue.put(i)

    reduce_stop = threading.Event()
    produce_stop = threading.Event()
    workers = [
        threading.Thread(target=produce, args=(queue, reduce_stop,)),
        threading.Thread(target=produce, args=(queue, reduce_stop,)),
        threading.Thread(target=produce, args=(queue, reduce_stop,)),
        threading.Thread(target=consume, args=(queue, produce_stop,)),
        threading.Thread(target=consume, args=(queue, produce_stop,))
    ]
    for w in workers:
        w.start()

    while True:
        if input('Press q for stop produce: ') == 'q':
            reduce_stop.set()
            while not queue.empty():
                pass
            produce_stop.set()
            break

    for w in workers:
        w.join()
