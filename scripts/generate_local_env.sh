#!/bin/bash

# Define the directory and file paths
dir_name="frontend"
file_path="$dir_name/.env.local"

# Create or overwrite the .env.local file
echo "Creating or updating the file: $file_path"
echo "VUE_APP_API_URL=http://127.0.0.1:5000" > $file_path
echo "VUE_APP_SERVER=http" >> $file_path

echo ".env.local file created/updated successfully in $dir_name"
