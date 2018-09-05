#!/usr/bin/env python
from __future__ import print_function

from parser import parser

# TODO add parser arguments

if __name__ == "__main__":
    opt = parser.parse_args()

    gpus = [int(gpu_id) for gpu_id in opt.gpus.split(",")]
    job_file = opt.job_file

    # spawn num_gpu worker threads that will handle job assignment
    # and monitoring to each gpu. 1 producer, N consumers
    
    with open(job_file) as f:
        for job_id, job in enumerate(f):
            print(f"{job_id}, {job.strip()}")

    # print(gpus)
    # print(job_file)
