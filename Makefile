prepare:
	mkdir -p credentials data
	cp ./config/default_config.py ./config/config.py
	touch ./credentials/credentials.json
	touch ./credentials/zuliprc.txt

install:
	pip install --no-cache-dir -r requirements.txt
