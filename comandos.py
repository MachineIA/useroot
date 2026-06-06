import subprocess

def run(args):
    return subprocess.run(args, text=True, capture_output=True)

def ls(*args):
    return run(["ls", *args])
def which(*args):
    return run(["which", *args])
def pwd():
    return run(["pwd"])
def cat(*args):
    return run(["cat", *args])

def UR():
    return run([
        "/data/data/com.termux/files/home/tmux/tmux"
    ])
