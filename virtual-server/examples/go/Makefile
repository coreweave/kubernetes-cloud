# Go parameters
GOCMD=go
GOMOD=$(GOCMD) mod
GOBUILD=$(GOCMD) build
GOCLEAN=$(GOCMD) clean
BINARY_NAME=vs

all: install run

install:
	$(GOMOD) download

run:
	export GO111MODULES=on
	$(GOBUILD) -o $(BINARY_NAME) -v ./...
	./$(BINARY_NAME)

clean:
	$(GOCLEAN)
	rm -rf $(BINARY_NAME)
