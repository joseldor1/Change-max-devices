import paramiko
import json

def read_remote_file(ip, username, password, remote_path, file_name):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the remote machine
        ssh.connect(ip, username=username, password=password)
        
        # Open SFTP session
        sftp = ssh.open_sftp()
        sftp.chdir(remote_path)

        # Read the remote file
        with sftp.open(file_name, 'r') as remote_file:
            file_content = remote_file.read()
            json_content = json.loads(file_content)
            print(json.dumps(json_content, indent=4, sort_keys=True))
        
        # Close the SFTP session and SSH connection
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    ip = "10.224.2.8"
    username = "omniaccess"
    password = "squeezematq2"
    remote_path = "/var/www/html/config/"
    file_name = "_crew_vrc.json"
    read_remote_file(ip, username, password, remote_path, file_name)
