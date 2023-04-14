# Docker build and push
build-push-docdb-migrator:
	cd docdb_migrator && docker build -t hassnat/toolkit:docdb-migrator-v1.0.2 . && cd ..
	docker push hassnat/toolkit:docdb-migrator-v1.0.2
build-push-docdb-connector:
	cd docdb_connector && docker build -t hassnat/toolkit:docdb-connector-v1.0.10 . && cd ..
	docker push hassnat/toolkit:docdb-connector-v1.0.10
run-commandor-cli:
	PYTHONPATH=commandor/src:$PYTHONPATH /home/hassnat/development/hassnatahmad/onpier-commandor/venv/bin/python commandor/src/cli/main.py
test-docdb-connectors:
	kubectx arn:aws:eks:eu-central-1:397078291328:cluster/devonpier
	kubectl port-forward pods/docdb-connector 8081:8081 &
	sleep 5;
	echo " Check if the docdb-connector is running in devonpier "
	curl -X 'POST' 'http://localhost:8081/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8081); echo "Killed port-forward"
	echo " Test the docdb-connector on stageonpier "
	kubectx arn:aws:eks:eu-central-1:233202861733:cluster/stageonpier
	kubectl port-forward pods/docdb-connector 8082:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8082/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8082); echo "Killed port-forward"
	echo " Test the docdb-connector on prodonpier "
	kubectx arn:aws:eks:eu-central-1:985578871783:cluster/prodonpier
	kubectl port-forward pods/docdb-connector 8083:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8083/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8083); echo "Killed port-forward"
	echo " Test the docdb-connector on devlvm "
	kubectx arn:aws:eks:eu-central-1:220965329085:cluster/devlvm
	kubectl port-forward pods/docdb-connector 8084:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8084/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8084); echo "Killed port-forward"
	echo " Test the docdb-connector on prodlvm "
	kubectx arn:aws:eks:eu-central-1:440694184070:cluster/prodlvm
	kubectl port-forward pods/docdb-connector 8085:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8085/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8085); echo "Killed port-forward"
	echo " Test the docdb-connector on devhdi "
	kubectx arn:aws:eks:eu-central-1:392007629827:cluster/devhdi
	kubectl port-forward pods/docdb-connector 8086:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8086/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8086); echo "Killed port-forward"
	echo " Test the docdb-connector on pprodhdi "
	kubectx arn:aws:eks:eu-central-1:240036087373:cluster/prodhdi
	kubectl port-forward pods/docdb-connector 8087:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8087/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8087); echo "Killed port-forward"
	echo " Test the docdb-connector on devhuk "
	kubectx arn:aws:eks:eu-central-1:297403996471:cluster/devhuk
	kubectl port-forward pods/docdb-connector 8088:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8088/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8088); echo "Killed port-forward"
	echo " Test the docdb-connector on prodhuk "
	kubectx arn:aws:eks:eu-central-1:626765625074:cluster/prodhuk
	kubectl port-forward pods/docdb-connector 8089:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8089/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8089); echo "Killed port-forward"
	echo " Test the docdb-connector on devowd "
	kubectx arn:aws:eks:eu-central-1:904684975200:cluster/devowd
	kubectl port-forward pods/docdb-connector 8090:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8090/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8090); echo "Killed port-forward"
	echo " Test the docdb-connector on prodowd "
	kubectx arn:aws:eks:eu-central-1:567850281018:cluster/prodowd
	kubectl port-forward pods/docdb-connector 8091:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8091/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8091); echo "Killed port-forward"
	echo " Test the docdb-connector on devwgv "
	kubectx arn:aws:eks:eu-central-1:098434142048:cluster/devwgv
	kubectl port-forward pods/docdb-connector 8092:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8092/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8092); echo "Killed port-forward"
	echo " Test the docdb-connector on prodwgv "
	kubectx arn:aws:eks:eu-central-1:172395385229:cluster/prodwgv
	kubectl port-forward pods/docdb-connector 8093:8081 &
	sleep 5;
	curl -X 'POST' 'http://localhost:8093/db' -H 'accept: application/json' -H 'Authorization: Basic b25waWVyOm9ucGllcg==' -H 'Content-Type: application/json' -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
	kill -9 $(lsof -t -i:8093); echo "Killed port-forward"

kill-all-ports-from-8081-8094:
	echo " Kill all port-forward from 8081 to 8094 "
	for (( i = 8081; i < 8095; i++ )); do
	    kill -9 $(lsof -t -i:$i)
	done