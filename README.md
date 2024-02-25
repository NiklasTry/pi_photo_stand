
# TE NAS Photo Share

## Preparation
1. **Create a folder**
2. **Clone this reposotory into the folder**

## Installation

1. **Update system and install cifs-utils:**
    ```bash
    sudo apt update && sudo apt install cifs-utils -y
    ```

2. **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Create the following directory in your home folder for the NAS photo share:**
    ```bash
    mkdir TE_NAS_photo_share
    ```

4. **Edit the /etc/fstab file:**
    ```bash
    sudo nano /etc/fstab
    ```

5. **Add the following line at the end, replacing placeholders:**
    ```plaintext
    //192.168.178.27/Global-Share/pi_photo_stand /home/niklas/TE_NAS_photo_share cifs user,username=guest,vers=3.0 0 0
    ```

    Make sure to adjust the user and the server info accordingly.
    Save the file and exit the text editor.

6. **Reboot or manually mount the share:**
    ```bash
    sudo mount -a
    ```
## Bash Script

1. **Change bash script**
    Go into the git reposetory and execute in terminal:
   ```
   chmod +x autostart_pi_stand.sh
    ```
1. **Change the path in service file**
    
    Change the path in the service file to match the bash file.

3. **Copy service**
    Copy the autostar_pi_stand.service into:

    ```
    /etc/systemd/system/
    ```
    Go into the git directory
    ```
    sudo cp autostart_pi_stand.service /etc/systemd/system/
    ```
2. **Reload systemd:**
   After modifying the Bash script, reload the systemd manager to apply the changes:

   ```bash
   sudo systemctl daemon-reload
   ```

4. **Enable and start the service**
    ```
    sudo systemctl enable autostart_pi_stand
    ```

5. **Start the service**
    ```
    sudo systemctl start autostart_pi_stand
    ```
6. **Verify the status**
    ```
    sudo systemctl status autostart_pi_stand
    ```
7. **Stop the service**
    ```
    sudo systemctl stop autostart_pi_stand
    ```
8. **Disable the Service**
    ```
    sudo systemctl disable autostart_pi_stand
    ```    
## Usage

Access the TE NAS photo share in the `/home/niklas/TE_NAS_photo_share` directory. Interact with your photos stored on the NAS using this directory.

**Note:** Ensure that your NAS is accessible on the specified IP address, and adjust the mount path and credentials accordingly.
