"""
Work Pool Examples and Infrastructure Control
Demonstrates different work pool types and configurations
"""
import os
from prefect import flow
from prefect.deployments import Deployment
from prefect.infrastructure import Process, DockerContainer, KubernetesJob
from prefect.filesystems import LocalFileSystem
from task import math_operations

# Example 1: Process Work Pool (Local execution)
def create_process_deployment():
    """Process work pool - runs on local machine or VM"""
    return Deployment.build_from_flow(
        flow=math_operations,
        name="process-math-ops",
        description="Runs using local process",
        work_pool_name="process-pool",  # Default process work pool
        work_queue_name="default",
        parameters={"x": 10, "y": 5},
        infra_overrides={
            "command": ["python", "-m", "prefect.engine"],
            "env": {
                "PYTHONPATH": "/app",
                "LOG_LEVEL": "INFO"
            },
            "working_dir": "/app"
        }
    )

# Example 2: Docker Work Pool
def create_docker_deployment():
    """Docker work pool - runs in Docker containers"""
    return Deployment.build_from_flow(
        flow=math_operations,
        name="docker-math-ops",
        description="Runs in Docker container",
        work_pool_name="docker-pool",
        work_queue_name="default",
        parameters={"x": 20, "y": 10},
        infra_overrides={
            "image": "prefect-math:latest",
            "command": ["python", "task.py"],
            "env": {
                "MATH_X": "20",
                "MATH_Y": "10"
            },
            "volumes": ["/app:/app"],
            "cpu_request": "100m",
            "memory_request": "128Mi",
            "cpu_limit": "500m",
            "memory_limit": "512Mi"
        }
    )

# Example 3: Kubernetes Work Pool
def create_kubernetes_deployment():
    """Kubernetes work pool - runs as Kubernetes jobs"""
    return Deployment.build_from_flow(
        flow=math_operations,
        name="k8s-math-ops", 
        description="Runs as Kubernetes job",
        work_pool_name="kubernetes-pool",
        work_queue_name="production",
        parameters={"x": 50, "y": 25},
        infra_overrides={
            "image": "prefect-math:latest",
            "namespace": "prefect",
            "service_account_name": "prefect-worker",
            "image_pull_policy": "Always",
            "labels": {
                "app": "prefect-math",
                "environment": "production"
            },
            "annotations": {
                "scheduler": "prefect"
            },
            "node_selector": {
                "workload-type": "compute"
            },
            "tolerations": [
                {
                    "key": "compute",
                    "operator": "Equal", 
                    "value": "true",
                    "effect": "NoSchedule"
                }
            ],
            "env": {
                "MATH_X": "50",
                "MATH_Y": "25",
                "ENVIRONMENT": "production"
            },
            "resources": {
                "requests": {
                    "memory": "256Mi",
                    "cpu": "200m"
                },
                "limits": {
                    "memory": "1Gi", 
                    "cpu": "1000m"
                }
            }
        }
    )

# Example 4: Cloud Run Work Pool (Google Cloud)
def create_cloud_run_deployment():
    """Cloud Run work pool - runs on Google Cloud Run"""
    return Deployment.build_from_flow(
        flow=math_operations,
        name="cloudrun-math-ops",
        description="Runs on Google Cloud Run",
        work_pool_name="cloud-run-pool",
        work_queue_name="serverless",
        parameters={"x": 100, "y": 50},
        infra_overrides={
            "image": "gcr.io/my-project/prefect-math:latest",
            "region": "us-central1",
            "cpu": "1000m",
            "memory": "512Mi",
            "timeout": 300,
            "max_concurrency": 10,
            "env": {
                "MATH_X": "100",
                "MATH_Y": "50",
                "GOOGLE_CLOUD_PROJECT": "my-project"
            },
            "labels": {
                "environment": "production",
                "team": "data-science"
            }
        }
    )

# Example 5: ECS Work Pool (AWS)
def create_ecs_deployment():
    """ECS work pool - runs on AWS ECS"""
    return Deployment.build_from_flow(
        flow=math_operations,
        name="ecs-math-ops",
        description="Runs on AWS ECS",
        work_pool_name="ecs-pool", 
        work_queue_name="production",
        parameters={"x": 75, "y": 30},
        infra_overrides={
            "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/prefect-math:latest",
            "cluster": "prefect-cluster",
            "family": "prefect-math-task",
            "cpu": 512,
            "memory": 1024,
            "execution_role_arn": "arn:aws:iam::123456789:role/ecsTaskExecutionRole",
            "task_role_arn": "arn:aws:iam::123456789:role/prefectTaskRole",
            "vpc_id": "vpc-12345",
            "subnet_ids": ["subnet-12345", "subnet-67890"],
            "security_group_ids": ["sg-12345"],
            "env": {
                "MATH_X": "75",
                "MATH_Y": "30",
                "AWS_DEFAULT_REGION": "us-east-1"
            },
            "tags": {
                "Environment": "production",
                "Application": "prefect-math"
            }
        }
    )

def deploy_infrastructure_examples():
    """Deploy examples for different infrastructure types"""
    deployments = [
        create_process_deployment(),
        create_docker_deployment(),
        create_kubernetes_deployment(),
        create_cloud_run_deployment(),
        create_ecs_deployment()
    ]
    
    print("Creating infrastructure-specific deployments...")
    for deployment in deployments:
        try:
            deployment_id = deployment.apply()
            print(f"✓ Created {deployment.name}")
        except Exception as e:
            print(f"✗ Failed to create {deployment.name}: {str(e)}")

if __name__ == "__main__":
    deploy_infrastructure_examples()