export user=tweldoncw
export image_name=bloom-175b
commit := $(shell /usr/bin/bash -c "git log -1 --format=%h")
export version=$(commit)
export run_cmd=sleep infinity

build:
	scripts/build

push:
	scripts/push 

run:
	scripts/run 