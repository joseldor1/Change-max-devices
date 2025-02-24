import paramiko
import json
import argparse

def load_config(config_path):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def modify_remote_file(ip, username, password, remote_path, file_name, new_devices_limit, user_type):
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
            levels_content = json_content["levels"][str(user_type)]

        # Modify the devices_limit key
        if "devices_limit" in levels_content:
            levels_content["devices_limit"] = new_devices_limit
            print(f"Updated devices_limit to {new_devices_limit}")
        else:
            print("Key 'devices_limit' not found in the JSON content.")
        
        print(json.dumps(json_content, indent=4))
        # Write the modified content back to the remote file
        #with sftp.open(file_name, 'w') as remote_file:
        #    remote_file.write(json.dumps(json_content, indent=4))
        
        # Close the SFTP session and SSH connection
        sftp.close()
        ssh.close()
        
        print("File modified successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modify the devices_limit in a remote JSON file.")
    parser.add_argument("ip", help="IP address of the remote machine")
    parser.add_argument("new_devices_limit", type=int, help="New value for devices_limit")
    parser.add_argument("users", help="Is crew or guests")

    args = parser.parse_args()
    
    config = load_config("config.json")
    username = config["username"]
    password = config["password"]
    
    remote_path = "/var/www/html/config/"
    file_name = f"_{args.users}_vrc.json"
    print(file_name)

    # Modify the remote file
    modify_remote_file(args.ip, username, password, remote_path, file_name, args.new_devices_limit, args.users)
