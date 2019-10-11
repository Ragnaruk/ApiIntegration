install:
    pip install --no-cache-dir -r requirements.txt
    mkdir credentials data logs
    cp ./config/default_config.py ./config/config.py