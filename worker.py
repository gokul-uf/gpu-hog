from __future__ import print_function
from multiprocessing import Process
from queue import Empty
from job import job


class Worker(Process):

    def __init__(self,
                 gpu_id,
                 queue,
                 lock,
                 prefix,
                 output_dir,
                 timeout=5,
                 job_method=job):
        super(Worker, self).__init__()
        self.gpu_id = gpu_id
        self.queue = queue
        self.lock = lock
        self.timeout = timeout

        self.prefix = prefix
        self.output_dir = output_dir

        assert callable(job_method), "job_method argument must be a callable"
        self.job_method = job_method

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

            job_name = self.prefix + str(job_id)
            self.job_method(job_name, job, self.output_dir, self.gpu_id)

            with self.lock:
                print(f"job {job_id} completed")
