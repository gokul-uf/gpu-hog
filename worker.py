from __future__ import print_function
from multiprocessing import Process
from queue import Empty
import time


class Worker(Process):

    def __init__(self, gpu_id, queue, lock, timeout=5):
        super(Worker, self).__init__()
        self.gpu_id = gpu_id
        self.queue = queue
        self.lock = lock
        self.timeout = timeout

    def run(self):
        with self.lock:
            print(f"Worker {self.gpu_id} starting")

        while True:
            try:
                job_id, job = self.queue.get(timeout=self.timeout)
            except Empty:
                with self.lock:
                    print(f"(GPU {self.gpu_id}): exiting")
                    break
            with self.lock:
                print(f"(GPU {self.gpu_id}): running {job}")

            # TODO run the job here
            time.sleep(2)  # sleep for now

            with self.lock:
                print(f"job {job_id} completed")
