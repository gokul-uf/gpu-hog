import os
import subprocess

# method that actually executes the job, can be replaced in the
# __init__ method to Worker class


def job(job_name, job_instruction, output_dir, gpu_id):
    # create the output dir
    base_dir = os.path.join(output_dir, job_name)
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    # write some basic INFO
    with open(os.path.join(base_dir, "INFO"), "w") as f:
        f.write(f"job name: {job_name}\n")
        f.write(f"ran on gpu: {gpu_id}\n")
        f.write(f"command: {job_instruction}\n")

    instr = f"export CUDA_VISIBLE_DEVICES={gpu_id} && {job_instruction}"
    stdout_file = os.path.join(base_dir, f"{job_name}.OUT")
    stderr_file = os.path.join(base_dir, f"{job_name}.ERR")

    with open(stdout_file, "w") as stdout, open(stderr_file, "w") as stderr:
        ''' Yes, I know shell=True has security issues, but this runs in
            user space and source of instruction is the user themselves.'''
        proc = subprocess.run(instr, stdout=stdout, stderr=stderr, shell=True)

    if proc.returncode:
        filename = os.path.join(base_dir, "FAILURE")
    else:
        filename = os.path.join(base_dir, "SUCCESS")

    with open(filename, 'a'):
        os.utime(filename, None)
