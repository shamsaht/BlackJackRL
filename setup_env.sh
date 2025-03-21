#!/bin/bash

# Create the Conda environment using the YAML file
echo "Creating Conda environment '21_env'..."
conda env create -f 21_env.yaml

# Activate the new environment
echo "Activating Conda environment '21_env'..."
conda activate 21_env

# Confirmation message
echo "Conda environment '21_env' is ready! Use 'conda activate 21_env' to work in the environment."

