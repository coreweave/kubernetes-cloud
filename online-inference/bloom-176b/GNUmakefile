export user=coreweave
export image_name=bloom-176b
commit := $(shell /usr/bin/bash -c "git log -1 --format=%h")
export version=$(commit)
export run_cmd=sleep infinity

docker: build push update_image

build:
	scripts/build

push:
	scripts/push 

run:
	scripts/run 

update_image:
	scripts/update_image