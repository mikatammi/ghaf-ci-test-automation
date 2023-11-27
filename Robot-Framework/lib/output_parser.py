# SPDX-FileCopyrightText: 2022-2023 Technology Innovation Institute (TII)
# SPDX-License-Identifier: Apache-2.0

import re
from datetime import datetime


def get_systemctl_status(output):
    output = re.sub(r'\033\[.*?m', '', output)   # remove colors from serial console output
    match = re.search(r'State: (\w+)', output)

    if match:
        return match.group(1)
    else:
        raise Exception("Couldn't parse systemctl status")


def get_service_status(output):
    output = re.sub(r'\033\[.*?m', '', output)   # remove colors from serial console output
    match = re.search(r'Active: (\w+) \((\w+)', output)

    if match:
        return match.group(1), match.group(2)
    else:
        raise Exception("Couldn't parse systemctl status")


def find_pid(output, proc_name):
    output = output.split('\n')
    pids = [line.split()[1] for line in output if proc_name in line]
    return pids


def verify_shutdown_status(output):
    output = re.sub(r'\033\[.*?m', '', output)   # remove colors from serial console output
    match = re.search(r'ExecStop=.*\(code=(\w+), status=(.*)\)', output)
    if match:
        return match.group(1), match.group(2)
    else:
        raise Exception("Couldn't parse shutdown status")


def parse_ghaf_version(output):
    major, minor = output.split(".")
    return major, minor


def parse_nixos_version(output):
    versions = output.split(' ')
    name = versions[1][1:-1] if len(versions) > 1 else None
    major, minor, date, commit = versions[0].split(".")
    return major, minor, date, commit, name


def verify_date_format(date_string):
    try:
        datetime.strptime(date_string, '%Y%m%d')
    except ValueError:
        raise Exception("Wrong date format in version date field")


def parse_cpu_results(output):
    def extract_value(pattern, output):
        match = re.search(pattern, output)
        if match:
            return match.group(1)
        else:
            raise Exception(f"Couldn't parse result of the test with pattern: {pattern}")

    output = re.sub(r'\033\[.*?m', '', output)  # remove colors from serial console output

    cpu_events_per_second = extract_value(r'events per second:\s*([.\d]+)', output)
    min_latency = extract_value(r'min:\s+([.\d]+)', output)
    max_latency = extract_value(r'max:\s+([.\d]+)', output)
    avg_latency = extract_value(r'avg:\s+([.\d]+)', output)
    cpu_events_per_thread = extract_value(r'events \(avg\/stddev\):\s+([.\d]+)', output)
    cpu_events_per_thread_stddev = extract_value(r'events \(avg\/stddev\):\s+[.\d]+\/([.\d]+)', output)

    cpu_data = {
        'cpu_events_per_second': cpu_events_per_second,
        'min_latency': min_latency,
        'max_latency': max_latency,
        'avg_latency': avg_latency,
        'cpu_events_per_thread': cpu_events_per_thread,
        'cpu_events_per_thread_stddev': cpu_events_per_thread_stddev
    }

    return cpu_data


def parse_memory_results(output):
    def extract_value(pattern, output):
        match = re.search(pattern, output)
        if match:
            return match.group(1)
        else:
            raise Exception(f"Couldn't parse result of the test with pattern: {pattern}")

    output = re.sub(r'\033\[.*?m', '', output)  # remove colors from serial console output

    operations_per_second = extract_value(r'Total operations:\s*\d+ \(([.\d]+) per second', output)
    data_transfer_speed = extract_value(r'\(([.\d]+) MiB\/sec\)', output)
    min_latency = extract_value(r'min:\s+([.\d]+)', output)
    max_latency = extract_value(r'max:\s+([.\d]+)', output)
    avg_latency = extract_value(r'avg:\s+([.\d]+)', output)
    avg_events_per_thread = extract_value(r'events \(avg\/stddev\):\s+([.\d]+)', output)
    events_per_thread_stddev = extract_value(r'events \(avg\/stddev\):\s+[.\d]+\/([.\d]+)', output)

    mem_data = {
        'operations_per_second': operations_per_second,
        'data_transfer_speed': data_transfer_speed,
        'min_latency': min_latency,
        'max_latency': max_latency,
        'avg_latency': avg_latency,
        'avg_events_per_thread': avg_events_per_thread,
        'events_per_thread_stddev': events_per_thread_stddev
    }

    return mem_data


def parse_iperf_output(output):
    tx_pattern = r'\s(\d+(\.\d+)?) MBytes\/sec.*sender'
    rx_pattern = r'\s(\d+(\.\d+)?) MBytes\/sec.*receiver'

    match = re.search(tx_pattern, output)
    if match:
        tx = match.group(1)
    else:
        raise Exception(f"Couldn't parse TX, pattern: {tx_pattern}")

    match = re.search(rx_pattern, output)
    if match:
        rx = match.group(1)
    else:
        raise Exception(f"Couldn't parse RX, pattern: {rx_pattern}")

    return {
        "tx": tx,
        "rx": rx
    }


def get_wifi_ip_from_ifconfig(output, if_name):
    pattern = if_name + r'.*?\n.*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    match = re.search(pattern, output)
    if match:
        return match.group(1)
    else:
        print(f"Couldn't find ip with pattern {pattern}")
        return None


def get_qspi_versions(output):
    fw_pattern = r"Current firmware version is: (\d*.\d*.\d*)"
    sw_pattern = r"Current software version is: (\d*.\d*.\d*)"

    match = re.search(fw_pattern, output)
    if match:
        fw_version = match.group(1)
    else:
        raise Exception(f"Couldn't parse current firmware version, pattern: {tx_pattern}")

    match = re.search(sw_pattern, output)
    if match:
        sw_version = match.group(1)
    else:
        raise Exception(f"Couldn't parse current software version, pattern: {rx_pattern}")

    return fw_version, sw_version
