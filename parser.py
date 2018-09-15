import argparse

parser = argparse.ArgumentParser(
    description='''Hog them GPUs!
        Run many jobs on mulitple jobs programmatically.
        No root access required!''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

input_group = parser.add_mutually_exclusive_group(required=True)
input_group.add_argument("--job_file", help="File to read jobs from", type=str)
input_group.add_argument(
    "--job_yielder", help="Yielder method to get jobs from", type=str)

parser.add_argument(
    "--gpus",
    help="comma separated IDs of the GPUs to use",
    type=str,
    required=True)
parser.add_argument(
    "--prefix",
    help="prefix to attach to each per-job folder name",
    type=str,
    default="job_")
parser.add_argument(
    "--output_dir",
    help="directory to store outputs from runs",
    default="hog_run")
