# Week2 Project Group A: Secure and Highly Available Static Web Deployment on Azure AKS

# 🛡️ Secure-by-Design AKS Deployment  
**Cloud-Native | DevSecOps | CI/CD Ready | Compliance-Aligned**


## **1️⃣ Project Overview**

This project delivers a secure, containerised static web application deployed to Azure Kubernetes Service (AKS), architected for high availability, scalability, and compliance. It integrates DevSecOps best practices across all layers — including TLS encryption, Ingress-based routing, pod-level isolation, autoscaling, and observability — aligned with Cyber Essentials, NCSC Cloud Security Principles, and ISO 27001.


## **2️⃣ Objectives** 

- 🚀 Deploy a containerised static web app to AKS  
- 🔐 Implement secure ingress routing and TLS termination  
- 🧱 Enforce network isolation and autoscaling  
- 📊 Maintain observability via Azure Monitor and Prometheus stack  



## **3️⃣ Infrastructure and Prerequisites**

| Component                          | Purpose                               |
|-----------------------------------|----------------------------------------|
| Azure CLI                         | Provision and manage cloud resources   |
| Docker                            | Build and package container image      |
| Kubernetes (kubectl)              | Apply declarative manifests            |
| Azure Resource Group              | Logical container for infrastructure   |
| Azure Container Registry (ACR)    | Host private Docker images             |
| Cert-Manager + Ingress            | HTTPS certificates and routing         |
| Azure Monitor                     | Cluster monitoring and diagnostics     |



## **4️⃣ Provisioning and Deployment Workflows**

### 🔧 Resource Group
```bash
az group create --name wordpress-rg --location uksouth
```

### 🔧 AKS Cluster
```bash
az aks create \
  --resource-group wordpress-rg \
  --name projecta-cluster \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys \
  --location uksouth \
  --node-vm-size Standard_DS2_v2 \
  --network-plugin azure
```

### 🔧 Container Registry
```bash
az acr create \
  --resource-group wordpress-rg \
  --name projectaregistry \
  --sku Basic \
  --location uksouth
```

### 🔧 Image Build and Push
```bash
az acr build --registry projectaregistry --image oresky73/week5-server:latest .
```

## **5️⃣ Kubernetes Deployment and Service**

Manifests: `kube/week2-projecta-aks.yaml`  
Includes:
- Namespace: `projecta`
- Deployment + LoadBalancer Service
- NetworkPolicy
- Horizontal Pod Autoscaler
- Ingress (TLS pending)

```bash
kubectl apply -f week2-projecta-aks.yaml -n projecta
kubectl get all -n projecta
```


## **6️⃣ Ingress and TLS Configuration (In Progress)**

### 🔧 NGINX Ingress Controller
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.14.0/deploy/static/provider/azure/deploy.yaml
```

### 🔧 Cert-Manager
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml
```

### 🔧 ClusterIssuer
```bash
kubectl apply -f cluster-issuer.yaml
```

### 🔧 Ingress Resource
```bash
kubectl apply -f ingress.yaml -n projecta
kubectl get ingress -n projecta
```


## **7️⃣ Network Policies**
```bash
kubectl apply -f network-policy.yaml
```
✅ Restricts ingress to Ingress Controller and limits inter-pod traffic.

---

## **8️⃣ Autoscaling and High Availability**

### Horizontal Pod Autoscaler
```bash
kubectl get hpa -n projecta
```

✅ Benefits:
- CPU-based autoscaling
- Multi-node fault tolerance
- Self-healing orchestration


## **9️⃣ Observability and Logging**

- Azure Monitor enabled via AKS provisioning
- Metrics: pod health, CPU/memory, ingress latency, node events
- Prometheus + Grafana + Alertmanager **planned** for deep telemetry


## **🔟 Security and Compliance Summary**

| Domain              | Control Implemented              | Outcome                        |
|---------------------|----------------------------------|--------------------------------|
| Access Control      | RBAC, namespace isolation        | Restricted admin exposure      |
| Network Security    | NetworkPolicy                    | Reduced attack surface         |
| TLS Encryption      | Cert-Manager + Ingress (pending) | Encrypted traffic              |
| Container Security  | Non-root, minimal base images    | Least privilege, image integrity |
| Resilience          | Multi-node HA, autoscaling       | Self-healing workloads         |
| Monitoring          | Azure Monitor + Prometheus stack | Continuous visibility          |



## **✅ Final Access**

- LoadBalancer IP:  http://<EXTERNAL-IP>`

- DNS + TLS (planned):  `https://glanik.duckdns.org`

---

## **🧩 Helm-Based Ingress Controller (Recommended)**

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.replicaCount=2 \
  --set controller.nodeSelector."kubernetes\.io/os"=linux \
  --set defaultBackend.nodeSelector."kubernetes\.io/os"=linux
```


## **📌 Outstanding Tasks**

| Area                  | Task                                           | Purpose                                  |
|-----------------------|------------------------------------------------|------------------------------------------|
| Ingress & TLS         | Finalize NGINX + Cert-Manager integration      | HTTPS termination and domain routing     |
| Certificate Validation| Debug glanik-cert provisioning                 | Automated TLS issuance                   |
| DNS Resolution        | Bind glanik.duckdns.org to Ingress IP          | Public access via FQDN                   |
| Observability         | Deploy Prometheus, Grafana, Alertmanager       | Deep performance and security analytics  |
| Security Scanning     | Integrate SonarQube, Trivy, OWASP ZAP          | Continuous vulnerability testing         |



## **🏁 Conclusion**

This project establishes a production-grade, secure AKS deployment with declarative infrastructure, CI/CD compatibility, and compliance-aligned architecture. Once TLS, observability, and scanning integrations are complete, the solution will meet enterprise-grade standards — serving as a model for secure cloud-native DevOps on Azure.

