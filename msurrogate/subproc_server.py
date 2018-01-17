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

        if module_name is None:
            raise RuntimeError("Must specify module_name")

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

        #start the error feed first so that we can see what is going on
        self.stderr_thread = threading.Thread(
            target = self._stderr_thread_loop,
            name = 'python subprocess stderr feed'
        )
        self.stderr_thread.daemon = True
        self.stderr_thread.start()

        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("Subprocess Did not complete its output")
            if line.strip() == 'COOKIE_START':
                break
            sys.stdout.write(self.stdout_prepend + line)

        cookie_lines = []
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("Subprocess Did not complete its output")
            if line.strip() == 'COOKIE_END':
                break
            cookie_lines.append(line)
        self.cookie_dict = json.loads(''.join(cookie_lines))

        self.stdout_thread = threading.Thread(
            target = self._stdout_thread_loop,
            name = 'python subprocess stdout feed'
        )
        self.stdout_thread.daemon = True
        self.stdout_thread.start()

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
            if not line:
                break
            sys.stdout.write(self.stdout_prepend + line)
            proc = self.proc

    def _stderr_thread_loop(self):
        proc = self.proc
        while proc is not None:
            line = proc.stderr.readline()
            if not line:
                break
            sys.stderr.write(self.stderr_prepend + line)
            proc = self.proc



