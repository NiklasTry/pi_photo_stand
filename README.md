
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

## Usage

Access the TE NAS photo share in the `/home/niklas/TE_NAS_photo_share` directory. Interact with your photos stored on the NAS using this directory.

**Note:** Ensure that your NAS is accessible on the specified IP address, and adjust the mount path and credentials accordingly.
