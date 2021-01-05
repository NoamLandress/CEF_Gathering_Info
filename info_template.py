import time
import subprocess


class SystemInfo:
    def __init__(self, command, command_output, error="No error received"):
        self.command = command
        self.command_output = command_output
        self.error = error

    def __repr__(self):
        delimiter = "\n-----------------------------------\n"
        return str(
            delimiter + "command: " + self.command + '\n' + "output: " + self.command_output + '\n' + "error: " + self.error + delimiter)


command_dict = {
    "netstat": "sudo netstat -lnpvt",
    "df": "sudo df -h",
    "free": "sudo free -m",
    "iptables": "sudo iptables -vnL --line",
    "selinux": "sudo getenforce",
    "os_version": "cat /etc/issue",
    "python_version": "python -V",
    "RAM_stats": "cat /proc/meminfo",
    "WD_list": "ls -l ."
}


def append_content_to_file(command_object, file_path='/tmp/cef_get_info'):
    output = repr(command_object).replace('%', '%%')
    command_tokens = ["sudo", "bash", "-c", "printf '" + "\n" + output + "' >> " + file_path]
    try:
        write_new_content = subprocess.Popen(command_tokens, stdout=subprocess.PIPE)
        time.sleep(0.5)
        o, e = write_new_content.communicate()
    except Exception:
        print(str(command_object.command) + "was not documented successfully")
    if e is not None:
        print(str(command_object.command) + "was not documented successfully")


def run_command(command):
    command_to_run = subprocess.Popen(command_dict[command].split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        o, e = command_to_run.communicate()
    except Exception:
        print(command_dict[command] + "failed to run")
        if e is None:
            e = Exception
        command_object = SystemInfo(command, "None", e)
        append_content_to_file(command_object)
    o = o.decode(encoding='UTF-8')
    command_object = SystemInfo(command, o)
    append_content_to_file(command_object)


def main():
    for command in command_dict:
        run_command(command)


if __name__ == '__main__':
    main()
