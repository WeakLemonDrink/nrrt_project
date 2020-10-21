# Activate the virtual environment and load env variables
source ./env/bin/activate
source ./scripts/dev_load_env_variables.sh

# Install all project dependencies to the virtual environment
pip install -r requirements.txt
