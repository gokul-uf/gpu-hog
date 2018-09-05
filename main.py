#!/usr/bin/env python3
from parser import parser

# TODO add parser arguments

if __name__ == "__main__":
    opt = parser.parse_args()

    # get job file list from --job_file
    # get number of GPUs from --gpu_ids

    gpus = [int(gpu_id) for gpu_id in opt.gpus.split(",")]
    job_file = opt.job_file

    # spawn num_gpu worker threads that will handle job assignment
    # and monitoring to each gpu. 1 producer, N consumers
    print(gpus)
    print(job_file)
