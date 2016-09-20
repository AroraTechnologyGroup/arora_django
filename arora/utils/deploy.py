import os
from arora.settings import BASE_DIR
import cgitb
import subprocess
from subprocess import PIPE
from django.core.mail import send_mail
from django.core import mail
cgitb.enable()


def pull(path):
    kwargs = dict()
    kwargs['cwd'] = path
    kwargs['stderr'] = PIPE
    kwargs['stdout'] = PIPE
    kwargs['universal_newlines'] = True
    git_cmd = "git pull"
    proc = subprocess.Popen(git_cmd, **kwargs)
    (std_out, std_err) = proc.communicate()

    python_path = os.path.join(BASE_DIR, r"venv\scripts\python.exe")
    manage_script = os.path.join(BASE_DIR, "manage.py")
    proc = subprocess.Popen([python_path, manage_script, "collectstatic --no-input"])
    (out, err) = proc.communicate()

    connection = mail.get_connection()
    connection.open()
    send_mail(
        "Deploy ARORA to Staging",
        "std_out: {} \n std_err: {} \n collectstatic: {}, err{}".format(std_out, std_err, out, err),
        "rhughes@aroraengineers.com",
        ["richardh522@gmail.com"],
        fail_silently=False,
    )
    connection.close()
    if std_err:
        return std_err
    else:
        return std_out
