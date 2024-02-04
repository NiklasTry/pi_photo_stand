#!/bin/bash

# Mount the NAS photo share
mount -a

# Check if the mount was successful
if [ $? -eq 0 ]; then
    echo "Mount successful. Running Python script..."
    
    # Navigate to the directory where your Python script is located
    cd pi_photo_stand

    # Run your Python script
    python3 main.py  # Replace 'your_script.py' with the actual name of your Python script
    sleep 30
else
    echo "Mount failed. Exiting script."
    sleep 30
fi
