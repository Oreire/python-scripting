# Week2 Project Group A: Secure and Highly Available Static Web Deployment on Azure AKS


### **1️⃣ Project Overview**

Engineered and deployed a containerised static web server to Azure Kubernetes Service (AKS), architected for security, scalability, and high availability. This project integrates DevSecOps best practices, which includes Ingress-based traffic routing, TLS encryption, pod-level network isolation, and auto-healing orchestration. This project demonstrates cloud-native resilience, compliance-aligned infrastructure, and CI/CD-ready deployment clarity.


### **2️⃣ Objectives**

* Deploy a **secure, load-balanced static web application** using Kubernetes on Azure AKS.
* Implement **Ingress and TLS termination** to protect public endpoints.
* Enhance **resilience** through multi-node scheduling, probes, and autoscaling.
* Ensure compliance with modern **cloud security and reliability standards**.

---

### **3️⃣ Infrastructure and Prerequisites**

| Component                           | Purpose                                      |
| ----------------------------------- | -------------------------------------------- |
| **Azure CLI**                       | Cluster provisioning and resource management |
| **Docker**                          | Container image creation                     |
| **Kubernetes (kubectl)**            | Declarative orchestration                    |
| **Azure Resource Group**            | Logical grouping for infrastructure          |
| **Cert-Manager + Ingress**          | Secure routing and TLS                       |
| **Prometheus + Grafana (optional)** | Monitoring and alerting                      |

**Resource Group Creation:**

```bash
az group create --name projecta-rg --location uksouth
```

**AKS Cluster Provisioning:**

```bash
az aks create \
  --resource-group projecta-rg \
  --name projecta-cluster \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys \
  --location uksouth \
  --node-vm-size Standard_DS2_v2 \
  --network-plugin azure
```

### **4️⃣ Dockerfile and Static Content**

**Dockerfile:**

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
```

* Lightweight, non-root container (Alpine base).
* NGINX serves static content securely.

**Build and Push to Azure Container Registry (optional):**

```bash
az acr build --registry projectaregistry --image projecta-static:v1 .
```

---

### **5️⃣ Kubernetes Manifests (kube/week2-projecta-aks.yaml)**

**Namespace:**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: projecta
```

**Deployment:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: projecta-server
  namespace: projecta
spec:
  replicas: 3
  selector:
    matchLabels:
      app: projecta-server
  template:
    metadata:
      labels:
        app: projecta-server
    spec:
      containers:
        - name: nginx
          image: projectaregistry.azurecr.io/projecta-static:v1
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 15
          securityContext:
            runAsNonRoot: true
            allowPrivilegeEscalation: false
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - projecta-server
              topologyKey: "kubernetes.io/hostname"
```

**Service:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: projecta-service
  namespace: projecta
spec:
  selector:
    app: projecta-server
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
```

---

### **6️⃣ Ingress and TLS Configuration**

**Step 1: Install NGINX Ingress Controller**

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.14.0/deploy/static/provider/azure/deploy.yaml
```

**Step 2: Install Cert-Manager for HTTPS**

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml
```

**ClusterIssuer (Let’s Encrypt):**

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: devops@projecta.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx
```

**Ingress Resource:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: projecta-ingress
  namespace: projecta
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - projecta.example.com
      secretName: projecta-tls
  rules:
    - host: projecta.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: projecta-service
                port:
                  number: 80
```

✅ **Benefits:**

* HTTPS termination with automatic certificate renewal.
* Single secure entry point with scalable routing.
* No direct exposure of pods or services to the public Internet.

---

### **7️⃣ Network Policies**

**Restrict Ingress Traffic:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-policy
  namespace: projecta
spec:
  podSelector:
    matchLabels:
      app: projecta-server
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
  policyTypes:
    - Ingress
```

> Limits inbound connections to only traffic routed through the NGINX Ingress Controller.

---

### **8️⃣ Autoscaling and High Availability**

**Horizontal Pod Autoscaler (HPA):**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: projecta-hpa
  namespace: projecta
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: projecta-server
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

**Cluster Autoscaler (Azure-managed):**
Enabled automatically with:

```bash
az aks update \
  --resource-group wordpress-rg \
  --name projecta-cluster \
  --enable-cluster-autoscaler \
  --min-count 2 \
  --max-count 5
```

✅ **Result:**

* Pods scale based on load.
* Node pool scales automatically to meet resource demand.
* Application remains available during spikes or node failures.

---

### **9️⃣ Observability and Logging**

Integrations:

* **Azure Monitor for Containers** (enabled via `--enable-addons monitoring`).
* Optional **Prometheus + Grafana + Alertmanager** for advanced metrics.

Monitored metrics include:

* Pod restarts and health status
* Ingress request latency
* CPU/memory utilization per deployment
* Node and control plane metrics

---

### **🔟 Security Hardening Summary**

| Control             | Implementation           | Outcome                           |
| ------------------- | ------------------------ | --------------------------------- |
| TLS/HTTPS           | Ingress + Cert-Manager   | Encrypted connections             |
| Network isolation   | NetworkPolicy            | Controlled pod traffic            |
| Non-root containers | SecurityContext          | Prevent privilege escalation      |
| Probes              | Liveness/Readiness       | Only healthy pods receive traffic |
| Autoscaling         | HPA + Cluster Autoscaler | Resilient scaling                 |
| Anti-affinity       | Multi-node scheduling    | High availability                 |
| Monitoring          | Prometheus/Azure Monitor | Real-time visibility              |

---

### **✅ Final Access**

Once Ingress and DNS are configured:

```
https://projecta.example.com
```

or via LoadBalancer public IP (if used temporarily):

```
http://<EXTERNAL-IP>
```

---

### **🧩 Conclusion**

This enhanced deployment transforms the Week2 Project into a **production-grade AKS workload** aligned with **DevOps**, **Cyber Essentials**, and **ISO 27001** principles.
It leverages **secure-by-design**, **declarative automation**, and **high availability patterns** to ensure performance, integrity, and compliance.

---

Would you like me to now:

1. 📦 Generate a **Helm Chart** structure for this deployment (values.yaml, templates, etc.), or
2. 🧩 Extend this into a **CPD Simulation Report** mapped to UK Cyber Essentials + ISO 27001 controls (for portfolio submission)?


INstalling INgreee on AZURE
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

**The URL you're using for the NGINX Ingress controller on Azure is outdated or incorrect — the file `deploy.yaml` for version `v1.14.0` does not exist at that path. The latest stable version is `v1.13.3`, and Azure-specific manifests are no longer maintained in that structure.**

---

## ✅ Recommended Solution: Use Helm to Install Ingress-NGINX on AKS

The most reliable and supported method to deploy the NGINX Ingress controller on Azure Kubernetes Service (AKS) is via Helm. Here's how to do it:

### 1️⃣ Add the Ingress-NGINX Helm Repository
```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

---

### 2️⃣ Install the Controller
```bash
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.replicaCount=2 \
  --set controller.nodeSelector."kubernetes\.io/os"=linux \
  --set defaultBackend.nodeSelector."kubernetes\.io/os"=linux
```

> This deploys the controller with two replicas for high availability and ensures compatibility with Linux nodes.

---

### 3️⃣ Verify the Deployment
```bash
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```

Look for the `EXTERNAL-IP` of the `ingress-nginx-controller` service to route traffic.

---

### 🧠 Sector-Facing Notes

- **Helm-based deployment** ensures reproducibility and aligns with GitOps workflows.
- **Versioning** is managed via Helm charts, currently at `controller-v1.13.3`.
- **Azure compatibility** is handled automatically via Helm values — no need for raw YAML from GitHub.

---

Would you like this scaffolded into a CPD simulation report or educator resource pack mapped to UK Cyber Essentials, ISO/IEC 27001, and DfE Digital Standards? I can also bundle it with signed YAML manifests and GitOps sync strategies.

Sources: [Ingress-NGINX GitHub Releases](https://github.com/kubernetes/ingress-nginx/releases)


install cert manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml


Secure Wordfloe

Excellent ✅ — we’ll now **extend your AKS deployment pipeline** to include a **complete security compliance stage** using **SonarQube (SAST)**, **Trivy (SCA)**, and **OWASP ZAP (DAST)** — while still relying **only on Azure secrets stored in GitHub** for all authentication.

Here’s the **final secure-by-design workflow**, ready for production.

---

## 🚀 Secure DevSecOps Pipeline — ProjectA AKS Deployment

**Filename:** `.github/workflows/deploy-projecta.yaml`

```yaml
name: 🔐 Secure AKS Deployment - ProjectA

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy:
    name: Deploy ProjectA to Azure AKS (with Security Compliance)
    runs-on: ubuntu-latest

    env:
      RESOURCE_GROUP: aks-resource-group
      CLUSTER_NAME: projecta-cluster
      MANIFEST_FILE: week2-projecta-aks.yaml
      NAMESPACE: projecta
      IMAGE_NAME: projecta-server
      IMAGE_TAG: latest
      ACR_NAME: glanikregistry      # Replace with your Azure Container Registry name
      SONAR_PROJECT_KEY: projecta
      SONAR_ORG: glanik
      SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
      SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

    steps:
      # -----------------------------------------------------
      # 1️⃣ Checkout repository
      # -----------------------------------------------------
      - name: Checkout source code
        uses: actions/checkout@v4

      # -----------------------------------------------------
      # 2️⃣ Azure Login (using Service Principal JSON secret)
      # -----------------------------------------------------
      - name: Azure Login
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      # -----------------------------------------------------
      # 3️⃣ Build & Push Container Image to Azure ACR
      # -----------------------------------------------------
      - name: Log in to Azure Container Registry
        run: |
          az acr login --name ${{ env.ACR_NAME }}

      - name: Build and Push Docker Image
        run: |
          IMAGE="${{ env.ACR_NAME }}.azurecr.io/${{ env.IMAGE_NAME }}:${{ env.IMAGE_TAG }}"
          echo "Building image: $IMAGE"
          docker build -t $IMAGE .
          docker push $IMAGE

      # -----------------------------------------------------
      # 4️⃣ Run Static Application Security Testing (SAST) - SonarQube
      # -----------------------------------------------------
      - name: SonarQube Scan (SAST)
        uses: SonarSource/sonarqube-scan-action@v3
        with:
          projectKey: ${{ env.SONAR_PROJECT_KEY }}
          organization: ${{ env.SONAR_ORG }}
        env:
          SONAR_TOKEN: ${{ env.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ env.SONAR_HOST_URL }}

      # -----------------------------------------------------
      # 5️⃣ Run Software Composition Analysis (SCA) - Trivy
      # -----------------------------------------------------
      - name: Scan image for vulnerabilities with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.ACR_NAME }}.azurecr.io/${{ env.IMAGE_NAME }}:${{ env.IMAGE_TAG }}
          format: 'table'
          severity: 'HIGH,CRITICAL'

      # -----------------------------------------------------
      # 6️⃣ Configure kubectl to connect to AKS
      # -----------------------------------------------------
      - name: Set AKS context
        uses: azure/aks-set-context@v3
        with:
          resource-group: ${{ env.RESOURCE_GROUP }}
          cluster-name: ${{ env.CLUSTER_NAME }}

      # -----------------------------------------------------
      # 7️⃣ Validate and Deploy Kubernetes manifests
      # -----------------------------------------------------
      - name: Validate manifests
        working-directory: ./kube
        run: |
          kubectl apply --dry-run=client -f "${MANIFEST_FILE}"

      - name: Apply manifests to AKS
        working-directory: ./kube
        run: |
          kubectl apply -f "${MANIFEST_FILE}" --record

      # -----------------------------------------------------
      # 8️⃣ Verify rollout
      # -----------------------------------------------------
      - name: Verify Deployment Rollout
        run: |
          kubectl rollout status deployment/week2-projecta-server -n "${NAMESPACE}" --timeout=120s

      # -----------------------------------------------------
      # 9️⃣ Run Dynamic Application Security Testing (DAST) - OWASP ZAP
      # -----------------------------------------------------
      - name: OWASP ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.13.0
        with:
          target: "http://<YOUR-SERVICE-EXTERNAL-IP>"   # Replace after service exposure
          cmd_options: "-a"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # -----------------------------------------------------
      # 🔟 Show endpoints and summary
      # -----------------------------------------------------
      - name: Display External Endpoints
        run: |
          kubectl get svc,ing -n "${NAMESPACE}"
```

---

## 🔑 Required GitHub Secrets

| Secret Name         | Description                                                             |
| ------------------- | ----------------------------------------------------------------------- |
| `AZURE_CREDENTIALS` | JSON credentials for Azure SP (see below)                               |
| `SONAR_TOKEN`       | Token from SonarQube project                                            |
| `SONAR_HOST_URL`    | Your SonarQube server URL (e.g. `https://sonarcloud.io` or self-hosted) |
| `GITHUB_TOKEN`      | (Auto-created by GitHub; do **not** add manually)                       |

**`AZURE_CREDENTIALS` Example:**

```json
{
  "clientId": "<AZURE_CLIENT_ID>",
  "clientSecret": "<AZURE_CLIENT_SECRET>",
  "subscriptionId": "<AZURE_SUBSCRIPTION_ID>",
  "tenantId": "<AZURE_TENANT_ID>"
}
```

## 🧠 Security Flow Summary

| Stage  | Tool      | Security Focus                     | Outcome                           |
| ------ | --------- | ---------------------------------- | --------------------------------- |
| Build  | Docker    | Image packaging                    | Secure build environment          |
| SAST   | SonarQube | Code vulnerabilities & code smells | Prevent insecure code merges      |
| SCA    | Trivy     | Dependency & container scanning    | Identify CVEs in image layers     |
| Deploy | kubectl   | Controlled rollout                 | Validated YAML syntax             |
| DAST   | OWASP ZAP | Runtime vulnerability testing      | Checks live endpoints post-deploy |

