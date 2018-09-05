import argparse

parser = argparse.ArgumentParser(description="hog them GPUs")
parser.add_argument("--job_file", help="File to read jobs from", type=str)
parser.add_argument(
    "--gpus", help="comma separated IDs of the GPUs to use", type=str)
parser.add_argument(
    "--prefix",
    help="prefix to attach to each per-job folder name",
    type=str,
    default="job_")
parser.add_argument(
    "--output_dir",
    help="directory to store outputs from runs",
    default="hog_run")
