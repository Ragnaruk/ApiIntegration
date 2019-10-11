prepare:
	mkdir credentials data
	cp ./config/default_config.py ./config/config.py

install:
	pip install --no-cache-dir -r requirements.txt
