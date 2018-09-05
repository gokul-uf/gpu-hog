from __future__ import print_function
from multithreading import Process
import time


class Worker(Process):

    def __init__(self, gpu_id, queue, lock):
        super(Worker, self).__init__()
        self.gpu_id = gpu_id
        self.queue = queue
        self.lock = lock

    def run(self):
        with self.lock:
            print(f"Worker {self.gpu_id} starting")

        while True:
            job_id, job = self.queue.get()
            with self.lock:
                print(f"(GPU {self.gpu_id}): running {job}")

            # TODO run the job here
            time.sleep(10)  # sleep for now

            with self.lock:
                print(f"job {job_id} completed")
