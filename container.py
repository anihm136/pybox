import os
import resource
import secrets
import shutil
import sys

import unshare

hostname = secrets.token_hex(8)

command = sys.argv[1]
argv = sys.argv[1:]

ROOTFS_PATH = "rootfs"
ROOTFS_ARCHIVE_PATH = "rootfs.tar"
unshare.unshare(unshare.CLONE_NEWUTS | unshare.CLONE_NEWPID)

shutil.unpack_archive(ROOTFS_ARCHIVE_PATH, ROOTFS_PATH, "tar")
shutil.copy("run.py", f"{ROOTFS_PATH}/run.py")

pid = os.fork()

limits = {
    "nproc": (1, 1),  # Cannot create child processes
    "nofile": (5, 5),  # Can only open 5 file descriptors (i.e, 2 files at most)
    "as": (int(200 * 1e6), int(200 * 1e6)),  # Overall process size limited to 200MB
    "cpu": (5, 10),  # CPU time limited to 10s
}

if pid == 0:
    resource.prlimit(os.getpid(), resource.RLIMIT_NPROC, limits["nproc"])
    resource.prlimit(os.getpid(), resource.RLIMIT_NOFILE, limits["nofile"])
    resource.prlimit(os.getpid(), resource.RLIMIT_AS, limits["as"])
    resource.prlimit(os.getpid(), resource.RLIMIT_CPU, limits["cpu"])
    os.chroot(ROOTFS_PATH)
    os.chdir("/")
    os.system(f"hostname {hostname}")
    os.execvp(command, argv)
else:
    os.waitpid(pid, 0)
    shutil.rmtree(ROOTFS_PATH)
