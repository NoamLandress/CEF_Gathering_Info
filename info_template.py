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
            delimiter + "command: " + self.command + '\n' + "output: " + self.command_output + delimiter)


command_dict = {
    "netstat": "sudo netstat -lnpvt",
    "df": "sudo df -h",
    "free": "sudo free -m",
    "iptables": "sudo iptables -vnL --line",
    "selinux": "sudo getenforce",
    "os_version": "sudo cat /etc/issue",
    "python_version": "sudo python -V",
    "ram_stats": "sudo cat /proc/meminfo",
    "cron_jobs": "sudo crontab -l",
    "ws_list": "sudo ls -l .",
    "internet_connection": "sudo curl -D - http://google.com",
    "sudoers_list": "sudo cat /etc/sudoers",
    "rotation_configuration": "sudo cat /etc/logrotate.conf",
#    "top_processes": "sudo top"
#    "omsagent_process": "grep omsagent \<\(ps -aux\)"
    "rsyslog_conf": "sudo cat /etc/rsyslog.conf",
    "rsyslog_dir": "sudo ls -l /etc/rsyslog.d/",
    "rsyslog_regex": "sudo cat /etc/rsyslog.d/security-config-omsagent.conf",
    "syslog_conf": "sudo cat /etc/syslog-ng/syslog-ng.conf",
    "syslog_dir": "sudo ls -l /etc/syslog-ng/conf.d/",
    "syslog_regex": "sudo cat /etc/syslog-ng/conf.d/security-config-omsagent.conf",
    "agent_log_snip": "sudo tail -15 /var/opt/microsoft/omsagent/log/omsagent.log",
    "agent_config_dir": "sudo ls -l /etc/opt/microsoft/omsagent/conf/omsagent.d/",
    "agent_cef_config": "sudo cat /etc/opt/microsoft/omsagent/conf/omsagent.d/security_events.conf"
#    "tcpdump": "sudo timeout 2 tcpdump -A -ni any port 25226 -vv"
}


def append_content_to_file(command_object, file_path='/tmp/cef_get_info'):
    output = repr(command_object).replace('%', '%%')
    command_tokens = ["sudo", "bash", "-c", "printf '" + "\n" + output + "' >> " + file_path]
    try:
        write_new_content = subprocess.Popen(command_tokens, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#        time.sleep(0.5)
        o = write_new_content.communicate()
    except Exception:
        print(str(command_object.command) + "was not documented successfully")



def run_command(command):
    command_to_run = subprocess.Popen(command_dict[command].split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        o, e = command_to_run.communicate()
    except Exception:
        print(command_dict[command] + "failed to run")
    o = o.decode(encoding='UTF-8')
    command_object = SystemInfo(command, o)
    append_content_to_file(command_object)


def main():
    for command in command_dict:
        run_command(command)


if __name__ == '__main__':
    main()
