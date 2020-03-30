
SHELL = /bin/bash

package:
	docker build --tag serverless-slope:latest .
	docker run --name serverless-slope --volume $(shell pwd)/:/local -itd serverless-slope:latest bash
	docker exec -it serverless-slope bash '/local/bin/package.sh'
	docker stop serverless-slope
	docker rm serverless-slope
