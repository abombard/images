all: build run

run:
	docker-compose up

# build: server.build vue.build

build: server-py.build vue.build

server-py.build:
	docker build --tag images-server-py --file ./docker/Dockerfile.server-py ./server-py

server.build:
	docker build --tag images-server --file ./docker/Dockerfile.server ./server

vue.build:
	docker build --tag images-web --file ./docker/Dockerfile.vue ./vue
