import re
import paramiko

from core.settings import HOST_IP, PORT, USERNAME, PASSWD


def ssh_shutdown_host():
    try:
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(HOST_IP, port=PORT, username=USERNAME, password=PASSWD)
        vm_list = "vim-cmd vmsvc/getallvms"
        vm_poweroff = "poweroff"
        stdin, stdout, stderr = ssh.exec_command(vm_list)
        output = stdout.read().decode()
        lines = output.split("\n")

        for line in lines:
            match = re.search(r"^(\d+)", line)
            if match:
                vw_id = match.group(1)
                ssh.exec_command(f"vim-cmd vmsvc/power.off {vw_id}")

        ssh.exec_command(vm_poweroff)

        ssh.close()
    except Exception:
        pass
