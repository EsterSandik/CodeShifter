#!/bin/bash
symlink_created=false
function cleanup {
  if [ "$symlink_created" = true ]; then
    rm -rf ./node_modules
    echo "Cleaned up temporary node_modules path."
  fi
}

trap cleanup EXIT

if [ -n "$NODE_PATH" ]; then
  if [ ! -d ./node_modules ]; then
    echo "Creating node_modules symlink"

    ln -s $NODE_PATH .
    symlink_created=true
  else
    echo "../node_modules already exists. Skipping symlink creation."
  fi
else
  echo "NODE_PATH variable is not set. Exiting."
fi

eslint "$@" 'client/**/*.{js,ts,jsx,tsx}'
