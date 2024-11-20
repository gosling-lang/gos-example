# /// script
# requires-python = ">=3.11,<3.12"
# dependencies = [
#     "clodius",
#     "h5py",
#     "pyvcf3",
#     "rich",
#     "snakemake",
# ]
#
# [tool.uv]
# exclude-newer = "2024-11-20T16:30:40.690699-05:00"
# ///
import os
import sysconfig
import sys


def find_snakemake_bin() -> str:
    """Find the Snakemake executable on Linux or macOS."""
    exe = "snakemake" + (sysconfig.get_config_var("EXE") or "")

    # Look in the scripts directory of the current environment
    path = os.path.join(sysconfig.get_path("scripts"), exe)
    if os.path.isfile(path):
        return path

    # Look in the user scripts directory
    user_scripts_path = sysconfig.get_path("scripts", scheme="posix_user")
    path = os.path.join(user_scripts_path, exe)
    if os.path.isfile(path):
        return path

    raise FileNotFoundError(f"Could not find Snakemake executable: {exe}")


snakemake = find_snakemake_bin()
os.execvp(snakemake, [snakemake, *sys.argv[1:]])
