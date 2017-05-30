import platform
import subprocess
from binaryninja import PluginCommand, log_alert

def spawn_xterm(command=None):
    subprocess.Popen(['xterm', '-e', command])

def spawn_gnome(command=None):
    subprocess.Popen(['gnome-terminal', '-e', command])

def spawn_konsole(command=None):
    subprocess.Popen(['konsole', '-e', command])

def spawn_terminal_dot_app(_command=None):
    import os
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile(delete=False) as temp:
        temp.write(_command)
        temp.flush()
        temp.close()
        os.chmod(temp.name, 0o777)
        subprocess.Popen(['open', '-b', 'com.apple.terminal', temp.name])

def spawn_terminal(command=None):
    if platform.system() == 'Darwin':
        spawn_terminal_dot_app(command)
    elif platform.system() == 'Linux':
        try:
            import apt
        except ImportError:
            print("apt is not installed, defaulting to gnome")
            spawn_gnome(command)
            return
        cache = apt.Cache()
        if cache['xterm'].is_installed:
            spawn_xterm(command)
        elif cache['gnome-terminal'].is_installed:
            spawn_gnome(command)
        elif cache['konsole'].is_installed:
            spawn_konsole(command)
    else:
        log_alert('No supported terminals found!')
