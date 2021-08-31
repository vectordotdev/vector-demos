ifndef ACCOUNT_ID
$(error ACCOUNT_ID is not set)
endif
.PHONY: up
up: eks-up iam-up sa-up alb-up vector-up

.PHONY: down
down: helm-down sa-down iam-down eks-down

.PHONY: eks-up
eks-up:
	eksctl create cluster --with-oidc --name vector-demo

.PHONY: iam-up
iam-up:
	aws iam create-policy \
		--policy-name AWSLoadBalancerControllerIAMPolicy \
		--policy-document file://aws/iam_policy.json | jq -r .Policy.Arn

.PHONY: sa-up
sa-up:
	eksctl create iamserviceaccount \
		--cluster=vector-demo \
		--namespace=kube-system \
		--name=aws-load-balancer-controller \
		--attach-policy-arn=arn:aws:iam::$(ACCOUNT_ID):policy/AWSLoadBalancerControllerIAMPolicy \
		--override-existing-serviceaccounts \
		--approve
.PHONY: alb-up
alb-up:
	helm repo add eks https://aws.github.io/eks-charts && \
		helm repo update
	kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller/crds?ref=master"
	helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
		--set clusterName=vector-demo \
		--set serviceAccount.create=false \
		--set serviceAccount.name=aws-load-balancer-controller \
		--namespace kube-system
.PHONY: vector-up
vector-up:
	helm repo add vector https://helm.vector.dev && \
		helm repo update
	helm upgrade --install vector vector/vector-aggregator \
		--values vector/values.yaml \
		--namespace vector \
		--create-namespace

.PHONY: helm-down
helm-down:
	helm uninstall aws-load-balancer-controller \
		--namespace kube-system
	helm uninstall vector \
		--namespace vector

.PHONY: sa-down
sa-down:
	eksctl delete iamserviceaccount \
		--cluster=vector-demo \
		--namespace=kube-system \
		--name=aws-load-balancer-controller

.PHONY: iam-down
iam-down:
	sleep 15
	aws iam delete-policy --policy-arn arn:aws:iam::$(ACCOUNT_ID):policy/AWSLoadBalancerControllerIAMPolicy

.PHONY: eks-down
eks-down:
	eksctl delete cluster --name=vector-demo
