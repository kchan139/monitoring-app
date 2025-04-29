# **System Utilization Dashboard**

A simple web application built with Flask to monitor system CPU and memory usage in real-time, containerized with Docker, and deployed using Kubernetes.

---

## **How to Run Locally**

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask app**:
   ```bash
   python app.py
   ```

3. **Access the app**: Open `http://localhost:8080` in your browser.

**Optional - Using Docker**:
```bash
# Build the image
docker build -t monitoring-app .

# Run the container
docker run -p 8080:8080 monitoring-app
```

## **Cloud Deployment**

1. **Build & Push to ECR**:
    ```bash
    # Step 1.1 - Create ECR repository (one-time setup)
    python script/ecr.py  # Outputs ECR image URI
    
    # Step 1.2 - Authenticate Docker with ECR
    aws ecr get-login-password --region <aws-region> | \
    docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<region>.amazonaws.com
    
    # Step 1.3 - Build and tag image
    docker build -t monitoring-app .
    docker tag monitoring-app:latest <image-uri>:latest
    
    # Step 1.4 - Push to ECR
    docker push <image-uri>:latest
    ```

2. **Kubernetes Deployment**:
   ```bash
   # Option 1: Using manifests
   kubectl apply -f deployment.yml  # Ensure IMAGE_URI is set

   # Option 2: Use script/eks.py (requires configured AWS/K8s access)
   python script/eks.py
   ```

3. **Access Application**:
   ```bash
   kubectl port-forward deployment/monitoring-app 8080:8080
   ```
   Open `http://localhost:8080` in your browser.

### **Required Setup**
1. AWS CLI configured (`aws configure`)
2. `docker` and `kubectl` installed and authenticated with your cluster
3. IAM permissions for ECR push/EKS deployment
4. Python dependencies installed
