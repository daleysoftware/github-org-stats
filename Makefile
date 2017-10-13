ORG=

all:
	./env/bin/python3 fetch.py $(ORG)

setup:
	virtualenv -p python3 env
	./env/bin/pip3 install -r requirements.txt

