# pybox
A proof-of-concept bare-bones container written in <50 lines of python code. Provides namespace isolation and resource limit control

# Usage
Install dependencies with pipenv
```sh
pipenv install
```
Run container.py as root (this is required for resource limits and process isolation)
```sh
sudo python container.py <command_to_run>
```
Command can also be interactive, for example `sh` can be executed to navigate and explore the container (which is just an isolated bare-bones linux file system)  
As a proof-of-concept for running code within the container, modify `run.py` to whatever python code you want to run. The script copies the file within the container and runs it with the specified resource limits. Currently only supports standard library and numpy.
```sh
sudo python container.py python run.py
```

# How it works
First we use `unshare` to isolate the UTS and PID namespaces (process and hosts). A skeleton Linux filesystem tarball is included, which is unpacked. Then, the main process is forked to allow for isolating within the skeleton filesystem using `chroot`. Finally, resource limits are set for the forked process using `prlimit`. The parent process waits for the child to exit and cleans up by removing the skeleton filesystem. Thus, each time the commands execute in a fresh filesystem with no artifacts of previous runs 

(This section is WIP, will be improved)

# Pitfalls
THIS IS HIGHLY UNTESTED. Error handling is practically non-existent, and there is potential for high-risk errors due to requirement of root access. That said, I've run it plenty of times over the last week and haven't faced any major issues on the host system  
Note that the `proc`, `sys` and `dev` filesystems are either non-existent or bare-bones, so code/commands relying on them will not work as expected. It is trivial to mount these, however unmounting as part of cleanup has proven difficult so far. PRs welcome 

# Credits and inspiration
This experiment was initiated by an interesting discussion over at PESOS. A lot of this is inspired (and copied) from [shubham1172/pocket](https://github.com/shubham1172/pocket), as well as his talk [](https://www.youtube.com/watch?v=VThBhfnTRiY). The idea for a barebones root filesystem came from [this talk](https://www.youtube.com/watch?v=gMpldbcMHuI), and is created using [buildroot/buildroot](https://github.com/buildroot/buildroot). Also some great ideas, inspiration and understanding from [here](https://medium.com/@jain.sm/writing-your-own-linux-container-259054465bd1), [here](https://ericchiang.github.io/post/containers-from-scratch/) and [here](https://fabianlee.org/2020/01/18/docker-placing-limits-on-container-memory-using-cgroups/)
