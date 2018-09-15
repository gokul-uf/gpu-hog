# gpu-hog
Run many jobs on multiple GPUs, so I can enjoy my weekends while GPUs work :P

Currently, we do a Producer-Consumer pattern where the producer reads a text file of commands. One command per line and feeds into a queue. There are atleast n consumer processes, one per GPU which read from the queue and run the command on the corresponding GPU. For each job, the `STDOUT` and `STDERR` outputs are stored in a folder with the `job_id`.

Currently, we support only static number of GPUs


## Installation
Currently, hog is not hosted on PyPI (hopefully will be done soon).
Alternative would be to clone this repo, add it to it your `PATH` variable and call from there.

## Usage
We currently support running hog as a CLI command

A basic use case would be

`hog --job_file foo.txt --gpus 1,2,3`

See the section on _Format of Job File_ for more information on how to write the job file.

## Flags
* `job_file` file to read jobs from
* `job_yielder` file with `yielder` method that generates jobs programmatically
* `gpus` comma-separated IDs of GPUs to use. Can run more than one concurrent per GPU
* `output_dir` Directory to store outputs from runs. Defaults to `hog_run`
* `prefix` prefix to attach to each per-job folder name. Defaults to `job_` so you will have folders named `job_0`, `job_1`... under `output_dir`

##  User-Defined Job Yielders
 We have the `--job_yielder` flag that allows users to define their method to generate jobs instead of using a `job_file`. To use this, define a method named `yielder` in another file, say `test.py` and call hog as below

	hog --job_yielder test.py (other flags)

`hog` will now run the `yielder` method from `test.py` to generate the jobs to put into queue.

## Running Concurrent Jobs on the same GPU
We do not have restrictions on how many concurrent jobs can run on the same GPU. It is important to note that in some cases it might be better to run only one job at any given point on a GPU. In other cases, for example, running multiple tensorflow instances, it might be possible to run several concurrent sessions on the same GPU. It is up to the user to decide which one is better suited for their use-case.

To run multiple concurrent programs on the same GPU, use multiple instances of the ID while setting the `--gpus` flag. For example, `--gpus 0,0,1,2,2,2` will run two concurrent jobs on GPU `0`, one on GPU `1`, three on GPU `2`

## Format of Output Folder
Inside `output_dir`, there is one folder per job according to flags passed. Say we have `job_1`, inside we have the following files

* `INFO` has basic information about the job such as job name, command, GPU the command was run on
* `job_0.ERR` captured `STDERR` output of the job
* `job_0.OUT` captured `STDOUT` output of the job
* `SUCCESS` / `FAILURE` empty file showing whether the job succeeded or not

## Format of Job File
1. A job is a bash command or `&&` separated sequence of commands to be executed
2. Specify one job per line
3. Lines starting with `#` and empty lines are ignored

## TODOs
1. Incorporate using `hog` as a decorator to make it more
2. Allow users to override default task to be done for each job
3. Use `multiprocessing.logging` instead of `print` statements
4. Allow changing GPUs available at runtime through a `gpu_file` argument
5. Have a test suite
