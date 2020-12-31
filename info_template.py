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


def append_content_to_file(command_object, file_path='/tmp/cef_get_info'):
    output = repr(command_object)
    command_tokens = ["sudo", "bash", "-c", "printf '" + "\n" + output + "' >> " + file_path]
    try:
        write_new_content = subprocess.Popen(command_tokens, stdout=subprocess.PIPE)
        time.sleep(2)
        o, e = write_new_content.communicate()
    except Exception:
        print(str(command_object.command) + "was not run successfully")


def netstat_open_ports():
    command_to_run = subprocess.Popen(["sudo", "netstat", "-lnpvt"], stdout=subprocess.PIPE)
    print("Gathering open ports info")
    o, e = command_to_run.communicate()
    o = o.decode(encoding='UTF-8')
    netstat = SystemInfo('netstat -lnpvt', str(o), str(e))
    append_content_to_file(netstat)


def disk_space():
    command_to_run = subprocess.Popen(["sudo", "df", "-h"], stdout=subprocess.PIPE)
    print("Gathering free disk space info")
    o, e = command_to_run.communicate()
    o = o.decode(encoding='UTF-8')
    df = SystemInfo('df -h', str(o), str(e))
    append_content_to_file(df)


def memory_space():
    command_to_run = subprocess.Popen(["sudo", "free", "-m"], stdout=subprocess.PIPE)
    print("Gathering system memory info")
    o, e = command_to_run.communicate()
    o = o.decode(encoding='UTF-8')
    df = SystemInfo('free -m', str(o), str(e))
    append_content_to_file(df)


def main():
    netstat_open_ports()
    disk_space()
    memory_space()


if __name__ == '__main__':
    main()
