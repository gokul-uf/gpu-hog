# gpu-hog
scripts to run many jobs on multiple GPUs, so I can enjoy my weekends while GPUs work :P

Currently, we do a Producer-Consumer pattern where the producer reads a text file of commands.
One command per line and feeds into a queue. 

There are n consumer processes, one per GPU which read from the queue and run the command
on the corresponding GPU.

For each job, the `STDOUT` and `STDERR` outputs are stored in a folder with the `job_id`.


Currently, we support only static number of GPUs



## Format of Job File
1. A job is a bash command or `&&` separated sequence of commands to be executed
2. Specify one job per line
3. Lines starting with `#` and empty lines are ignored


