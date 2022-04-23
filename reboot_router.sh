#!/bin/bash

# path
$REBOOT_ROUTER_REPO_LOCATION="/path/to/reboot_router.py script"

# git pull and run the script
cd $REBOOT_ROUTER_REPO_LOCATION && git pull && python3 "reboot_router.py" 
