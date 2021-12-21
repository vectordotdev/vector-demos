start-local:
	@echo "ℹ️  \033[36mRunning Vector locally to demonstrate how configs are loaded from a directory.\033[0m\n"
	@vector -C ./vector

start-k8s:
	@echo "ℹ️  \033[36mRunning Vector in target k8s cluster to demonstrate merged configmaps.\033[0m"
	@echo "⚠️  \033[33mNote that this will run in whatever your current kubectl target cluster is!\033[0m\n"
	@helm install -n vector test .

stop-k8s:
	@echo "⚠️  \033[33mRemoving the test k8s Vector instance.\033[0m\n"
	@helm uninstall -n vector test

logs-k8s:
	@kubectl logs -n vector test-vector-aggregator-0