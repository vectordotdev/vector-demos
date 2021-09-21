ifndef ACCOUNT_ID
$(error ACCOUNT_ID is not set)
endif
.PHONY: cluster-up
cluster-up:
	eksctl create cluster --with-oidc --name vector-demo
	aws iam create-policy \
		--policy-name AWSLoadBalancerControllerIAMPolicy \
		--policy-document file://iam_policy.json | jq -r .Policy.Arn
	eksctl create iamserviceaccount \
		--cluster=vector-demo \
		--namespace=kube-system \
		--name=aws-load-balancer-controller \
		--attach-policy-arn=arn:aws:iam::$(ACCOUNT_ID):policy/AWSLoadBalancerControllerIAMPolicy \
		--override-existing-serviceaccounts \
		--approve
	helm repo add eks https://aws.github.io/eks-charts && \
		helm repo update
	kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller/crds?ref=master"
	helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
		--set clusterName=vector-demo \
		--set serviceAccount.create=false \
		--set serviceAccount.name=aws-load-balancer-controller \
		--namespace kube-system
	kubectl apply -f "https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml"
	kubectl create namespace vector 
	kubectl create namespace datadog 

.PHONY: cluster-down
cluster-down:
	helm uninstall aws-load-balancer-controller \
		--namespace kube-system
	kubectl delete namespace vector 
	kubectl delete namespace datadog 
	eksctl delete iamserviceaccount \
		--cluster=vector-demo \
		--namespace=kube-system \
		--name=aws-load-balancer-controller
	sleep 15
	aws iam delete-policy --policy-arn arn:aws:iam::$(ACCOUNT_ID):policy/AWSLoadBalancerControllerIAMPolicy
	eksctl delete cluster --name=vector-demo
