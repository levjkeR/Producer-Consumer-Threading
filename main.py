import threading
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


class Queue:
    def __init__(self, queue=None):
        self.queue = queue

    def push(self, element):
        self.queue.append(element)

    def pop(self):
        if not len(self.queue):
            return None
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)


queue = Queue(queue=list(range(200)))


def get_randomint():
    randomized = random.randint(1, 100)
    return randomized


class Producer(threading.Thread):
    def __init__(self, number):
        threading.Thread.__init__(self, name=f"Worker {number}")
        self.number = number

    def run(self):
        while True:
            print(queue.size())
            if queue.size() < 100:
                queue.push(get_randomint())
            else:
                time.sleep(1)


class Consumer(threading.Thread):
    def __init__(self, number):
        threading.Thread.__init__(self, name=f"Consumer {number}")
        self.number = number

    def run(self):
        while True:
            if queue.size() != 0:
                queue.pop()
            else:
                print(queue.size(), 'sleep', queue.__dict__)
                time.sleep(5)


if __name__ == '__main__':
    producers = [Producer(1), Producer(2), Producer(3)]
    consumers = [Consumer(1), Consumer(2)]

    for producer in producers:
        producer.start()
    for consumer in consumers:
        consumer.start()
