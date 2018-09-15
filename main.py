#!/usr/bin/env python3
from __future__ import print_function

from worker import Worker
from parser import parser
from job_yielder import get_jobs

from multiprocessing import Queue, Lock
import datetime
import os

if __name__ == "__main__":
    opt = parser.parse_args()

    gpus = [int(gpu_id) for gpu_id in opt.gpus.split(",")]
    queue = Queue()
    console_lock = Lock()  # for printing to STDOUT

    # spawn num_gpu worker threads that will handle job assignment
    # and monitoring to each gpu. 1 producer, N consumers
    workers = []

    # create the output dir
    if not os.path.exists(opt.output_dir):
        os.mkdir(opt.output_dir)

    # Start the workers
    for gpu in gpus:
        w = Worker(gpu, queue, console_lock, opt.prefix, opt.output_dir)
        # we don't want the main to exit before all workers are done
        w.daemon = False
        w.start()
        workers.append(w)

    start_time = datetime.datetime.now()
    with console_lock:
        print(f"(MAIN): Starting at {start_time}")

    job_counter = 0

    for job in get_jobs(opt):
        job_counter += 1
        queue.put((job_counter, job))

    # join here to be extra sure
    for w in workers:
        w.join()

    end_time = datetime.datetime.now()
    with console_lock:
        print(f"(MAIN): {job_counter} jobs completed at {end_time}")
        print(f"(MAIN): Lapsed Time: {end_time - start_time}")
