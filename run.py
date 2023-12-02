#!/bin/env python

import argparse
import os
import time
import subprocess
import subprocess as sb

from proxyChecker import check
from proxyScraper import scrape, scrapers


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-w",
        "--work-dir",
        help="Work directory",
        required=True
    )
    parser.add_argument(
        "-p",
        "--proxy",
        help="Supported proxy type: " + ", ".join(sorted(set([s.method for s in scrapers]))),
        required=True,
        nargs='+',
        action="extend"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        help="Dismiss the proxy after -t seconds",
        default=20,
    )
    parser.add_argument(
        "-s",
        "--site",
        help="Check with specific website like google.com",
        default="https://google.com/",
    )
    parser.add_argument(
        "-r",
        "--random_agent",
        help="Use a random user agent per proxy",
        action="store_true",
    )

    args = parser.parse_args()

    for p in args.proxy:
        directory = os.path.join(args.work_dir, f'{p}_{int(time.time())}.txt')
        subprocess.run(["python", "proxyScraper.py", "-p", p, "-o", directory], check=True)

        cmd_list = ["python", "proxyChecker.py", "-t", str(args.timeout), "-s", args.site, '-l', directory]
        if args.random_agent:
            cmd_list.append("-r")
        subprocess.run(cmd_list, check=True)
