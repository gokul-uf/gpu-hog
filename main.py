#!/usr/bin/env python3
from __future__ import print_function

from worker import Worker
from parser import parser

from multiprocessing import Queue, Lock
import datetime

if __name__ == "__main__":
    opt = parser.parse_args()

    gpus = [int(gpu_id) for gpu_id in opt.gpus.split(",")]
    job_file = opt.job_file
    queue = Queue()
    console_lock = Lock()  # for printing to STDOUT

    # spawn num_gpu worker threads that will handle job assignment
    # and monitoring to each gpu. 1 producer, N consumers
    workers = []

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
    with open(job_file) as f:
        for line in f:
            line = line.strip()
            # ignore comments and empty lines
            if line.startswith("#") or len(line) == 0:
                continue

            queue.put((job_counter, line))
            job_counter += 1

    # join here to be extra sure
    for w in workers:
        w.join()

    end_time = datetime.datetime.now()
    with console_lock:
        print(f"(MAIN): {job_counter+1} jobs completed at {end_time}")
        print(f"(MAIN): Lapsed Time: {end_time - start_time}")
