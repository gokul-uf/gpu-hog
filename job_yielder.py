import os
import sys

# method that generates jobs from either
# a file or another user-defined generator


def get_jobs(opt):
    if opt.job_file:  # we have a job_file
        with open(opt.job_file) as f:
            for line in f:
                line = line.strip()
                # ignore comments and empty lines
                if line.startswith("#") or len(line) == 0:
                    continue
                yield line
    else:  # we have job generator
        directory, module_name = os.path.split(opt.job_yielder)
        module_name = os.path.splitext(module_name)[0]

        sys.path.insert(0, directory)
        try:
            module = __import__(module_name)
            module.yielder  # testing if yielder method exists
        except ImportError:
            raise ImportError(
                f"Can't import {opt.job_yielder}, ensure it exists",
                " and has a method named 'yielder'")

        yield from module.yielder()
