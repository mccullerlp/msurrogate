"""
An msurrogate model server. Start this code to connect from other applications
"""
from __future__ import division, print_function, unicode_literals
from .meta_daemon import MetaDaemon
import sys
import json
import uuid
import subprocess
import threading


class ServerSubprocess(object):

    def __init__(
        self,
        python_call    = None,
        module_name    = None,
        env            = None,
        stdout_prepend = '  PYOUT:',
        stderr_prepend = '  PYERR:',
        args           = [],
    ):

        self.stdout_prepend = stdout_prepend
        self.stderr_prepend = stderr_prepend

        if python_call is None:
            python_call = sys.executable

        self.proc = subprocess.Popen(
            [python_call, '-m', module_name, '-S', '-', '-c', '-'] + args,
            stdout = subprocess.PIPE,
            stdin  = subprocess.PIPE,
            stderr = subprocess.PIPE,
            env    = env,
            bufsize=1,
        )

        #write the secret
        self.mysecret = str(uuid.uuid4())
        self.proc.stdin.write(self.mysecret + "\n")

        lines = []
        while True:
            line = self.proc.stdout.readline()
            lines.append(line)
            if line.strip() == 'COOKIE_END':
                break
        for idx, line in enumerate(lines):
            if line.strip() == 'COOKIE_START':
                idx_start = idx
                break
        cookie_lines = lines[idx_start + 1 : -1]
        self.cookie_dict = json.loads(''.join(cookie_lines))

        #now print everything else:
        for line in lines[:idx_start]:
            sys.stdout.write(self.stdout_prepend + line)

        self.stdout_thread = threading.Thread(
            target = self._stdout_thread_loop,
            name = 'python subprocess stdout feed'
        )
        self.stdout_thread.daemon = True
        self.stdout_thread.start()

        self.stderr_thread = threading.Thread(
            target = self._stderr_thread_loop,
            name = 'python subprocess stderr feed'
        )
        self.stderr_thread.daemon = True
        self.stderr_thread.start()
        return

    def stop(self):
        self.proc.kill()
        #stops the threads
        self.proc = None
        return

    def _stdout_thread_loop(self):
        proc = self.proc
        while proc is not None:
            line = proc.stdout.readline()
            sys.stdout.write(self.stdout_prepend + line)
            proc = self.proc

    def _stderr_thread_loop(self):
        proc = self.proc
        while proc is not None:
            line = proc.stderr.readline()
            sys.stderr.write(self.stderr_prepend + line)
            proc = self.proc



