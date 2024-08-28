import paramiko
import tenants
from logconf import get_logger

logger = get_logger()


def run_ssh_cmd(server, user, password, cmd):
    # Initialize SSH client and configure to auto-accept unknown keys
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect to the remote server
    try:
        # print "\nConnecting to server: {0}".format(server), don't uncomment unless for debugging purpose
        ssh_client.connect(server, username=user, password=password, timeout=30)
    except Exception as e:
        logger.error("Error Occurred: {}".format(e))
        return 'An error occurred'

    # Run command on remote server
    # print "\nExecuting SSH command: {0} on {1}".format(cmd, server), don't uncomment unless for debugging purpose
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(cmd)
    std_err = ssh_stderr.read()
    if std_err:
        logger.error("Error occurred during remote command execution: {}".format(std_err))
        return 'An error occurred'
    else:
        ssh_stdin.close()
        std_out = ssh_stdout.read()
        ssh_client.close()
        return std_out


def collect_all_tenant_enm_management_alarms():
    # array to collect all alarms from different tenants
    all_tenants_alarms_list = []

    for tenant in tenants.Tenants:
        # dict of 1 tenant alarms
        alarms_per_tenant = {}
        tenant_alarm = run_ssh_cmd(tenant["ip"], tenant["user"], tenant["password"],
                                   "python {}".format(tenants.local_script_path))
        if tenant_alarm != 'An error occurred':
            # convert string to array
            tenant_alarm_array = eval(tenant_alarm)
            alarms_per_tenant[tenant["name"]] = tenant_alarm_array
            all_tenants_alarms_list.append(alarms_per_tenant)
        else:
            continue

    return all_tenants_alarms_list
