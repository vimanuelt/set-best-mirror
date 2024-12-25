#!/usr/bin/env python3

import subprocess
import time
import sys
import shutil
import os
import stat

def run_ping(host, count=5):
    """
    Runs a ping command to measure latency to a host.
    
    :param host: The hostname to ping
    :param count: Number of ping attempts
    :return: Average latency in milliseconds or None if ping fails
    """
    try:
        result = subprocess.run(['ping', '-c', str(count), host], 
                                capture_output=True, text=True, timeout=10, check=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if 'avg' in line:
                avg = line.split('/')[4]
                return float(avg)
        print(f"Unexpected ping output for {host}")
        return None
    except subprocess.TimeoutExpired:
        print(f"Ping to {host} timed out.")
    except subprocess.CalledProcessError as e:
        print(f"Ping to {host} failed with error: {e.returncode}")
        print(f"Ping error details: {e.stderr}")
    except ValueError as e:
        print(f"Could not parse ping result for {host}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during ping to {host}: {e}")
    return None

def measure_download_speed(host):
    """
    Measures download speed from a host by downloading the 'data.pkg' file.

    :param host: The hostname to test
    :return: Download speed in MB/s or None if download fails
    """
    url = f"https://{host}/stable/FreeBSD:14:amd64/latest/data.pkg"
    start_time = time.time()
    try:
        result = subprocess.run(['wget', '-O', '/dev/null', '-S', url], 
                                capture_output=True, text=True, timeout=30, check=True)
        
        end_time = time.time()
        if result.returncode == 0:  # Indicates wget completed without error
            size = 7.6  # 7.6 MB as specified
            duration = end_time - start_time
            if duration > 0:
                return size / duration  # MB/s
            else:
                print(f"Download from {host} took no time, which is unexpected.")
                return None
        else:
            print(f"wget failed with return code {result.returncode} for {host}")
            print(f"wget stdout: {result.stdout}")
            print(f"wget stderr: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print(f"Download from {host} timed out.")
    except subprocess.CalledProcessError as e:
        print(f"Download from {host} failed with error: {e.returncode}")
        print(f"wget stdout: {e.stdout}")
        print(f"wget stderr: {e.stderr}")
    except ValueError as e:
        print(f"Could not parse wget output for {host}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during download from {host}: {e}")
    return None

def rank_mirrors(mirrors):
    """
    Ranks mirrors based on ping and download speed.

    :param mirrors: List of hostnames to rank
    :return: List of tuples (mirror, ping, speed) ordered by performance
    """
    results = []
    for mirror in mirrors:
        print(f"Testing mirror: {mirror}")
        ping = run_ping(mirror)
        speed = measure_download_speed(mirror)
        if ping is not None and speed is not None:
            results.append((mirror, ping, speed))
        else:
            print(f"Could not measure performance for {mirror}")
    
    # Sort by ping (lower is better) and then by speed (higher is better)
    return sorted(results, key=lambda x: (x[1], -x[2]))

def set_best_mirror(best_mirror):
    """
    Sets the best mirror by copying the appropriate configuration file.

    :param best_mirror: The hostname of the best mirror
    :return: Boolean indicating success or failure
    """
    conf_dir = '/usr/local/etc/pkg/repos'
    # Define a mapping for mirrors to config files
    mirror_config_map = {
        'pkg.ghostbsd.org': 'GhostBSD.conf.default',  # Assuming default is for .org
        'pkg.ca.ghostbsd.org': 'GhostBSD.conf.ca',
        'pkg.fr.ghostbsd.org': 'GhostBSD.conf.fr'
    }
    
    conf_file = f"{conf_dir}/{mirror_config_map.get(best_mirror)}"
    dest_file = f"{conf_dir}/GhostBSD.conf"

    try:
        # Check if the source configuration file exists
        if not os.path.exists(conf_file):
            print(f"Configuration file for {best_mirror} not found: {conf_file}")
            return False

        # Copy the best mirror's config file to GhostBSD.conf
        try:
            subprocess.run(['cp', conf_file, dest_file], check=True)
            print(f"Successfully set {best_mirror} as the best mirror by updating {dest_file}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to copy configuration file: {e}")
            print(f"Error details: {e.stderr}")
            return False

    except Exception as e:
        print(f"An unexpected error occurred while setting the best mirror: {e}")
        return False

    return True

def main():
    # Check for root user privileges at the beginning of the program
    if os.geteuid() != 0:
        print("You need to run this script with root privileges.")
        print("Please run with 'sudo' or 'doas':")
        print(f"    sudo python set-best-mirror.py")
        sys.exit(1)

    mirrors = [
        'pkg.ghostbsd.org', 
        'pkg.ca.ghostbsd.org', 
        'pkg.fr.ghostbsd.org'
    ]
    
    try:
        ranked_mirrors = rank_mirrors(mirrors)
        
        print("Ranked Mirrors:")
        for i, (mirror, ping, speed) in enumerate(ranked_mirrors, 1):
            print(f"{i}. {mirror}: Ping = {ping:.2f} ms, Speed = {speed:.3f} MB/s")
        
        if ranked_mirrors:
            best_mirror, _, _ = ranked_mirrors[0]
            if not set_best_mirror(best_mirror):
                print("Failed to set the best mirror.")
        else:
            print("No mirrors could be ranked due to errors.")
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
