"""
Work Pool Management Script
Shows how to create and manage work pools programmatically
"""
from prefect.client.orchestration import get_client
from prefect.server.schemas.core import WorkPool
import asyncio
import json

async def create_work_pools():
    """Create different types of work pools"""
    async with get_client() as client:
        
        # 1. Process Work Pool
        process_pool = WorkPool(
            name="local-process-pool",
            type="process", 
            description="Local process execution",
            is_paused=False,
            base_job_template={
                "job_configuration": {
                    "command": "{{ command }}",
                    "env": "{{ env }}",
                    "working_dir": "{{ working_dir }}"
                },
                "variables": {
                    "properties": {
                        "command": {
                            "title": "Command", 
                            "description": "Command to run",
                            "default": ["python", "-m", "prefect.engine"],
                            "type": "array"
                        },
                        "env": {
                            "title": "Environment Variables",
                            "type": "object",
                            "default": {}
                        },
                        "working_dir": {
                            "title": "Working Directory", 
                            "type": "string",
                            "default": "/app"
                        }
                    }
                }
            }
        )
        
        # 2. Docker Work Pool
        docker_pool = WorkPool(
            name="docker-execution-pool",
            type="docker",
            description="Docker container execution",
            is_paused=False,
            base_job_template={
                "job_configuration": {
                    "image": "{{ image }}",
                    "command": "{{ command }}",
                    "env": "{{ env }}",
                    "volumes": "{{ volumes }}",
                    "networks": "{{ networks }}",
                    "cpu_limit": "{{ cpu_limit }}",
                    "memory_limit": "{{ memory_limit }}"
                },
                "variables": {
                    "properties": {
                        "image": {
                            "title": "Docker Image",
                            "type": "string", 
                            "default": "prefect:latest"
                        },
                        "command": {
                            "title": "Command",
                            "type": "array",
                            "default": ["python", "-m", "prefect.engine"]
                        },
                        "env": {
                            "title": "Environment Variables",
                            "type": "object",
                            "default": {}
                        },
                        "volumes": {
                            "title": "Volume Mounts",
                            "type": "array",
                            "default": []
                        },
                        "networks": {
                            "title": "Networks",
                            "type": "array", 
                            "default": []
                        },
                        "cpu_limit": {
                            "title": "CPU Limit",
                            "type": "string",
                            "default": "1.0"
                        },
                        "memory_limit": {
                            "title": "Memory Limit", 
                            "type": "string",
                            "default": "1G"
                        }
                    }
                }
            }
        )
        
        # 3. Kubernetes Work Pool
        k8s_pool = WorkPool(
            name="kubernetes-production-pool",
            type="kubernetes",
            description="Kubernetes job execution for production",
            is_paused=False,
            base_job_template={
                "job_configuration": {
                    "image": "{{ image }}",
                    "namespace": "{{ namespace }}",
                    "service_account_name": "{{ service_account_name }}",
                    "image_pull_policy": "{{ image_pull_policy }}",
                    "command": "{{ command }}",
                    "env": "{{ env }}",
                    "labels": "{{ labels }}",
                    "node_selector": "{{ node_selector }}",
                    "tolerations": "{{ tolerations }}",
                    "resources": "{{ resources }}"
                },
                "variables": {
                    "properties": {
                        "image": {
                            "title": "Container Image",
                            "type": "string",
                            "default": "prefect:latest"
                        },
                        "namespace": {
                            "title": "Kubernetes Namespace",
                            "type": "string", 
                            "default": "default"
                        },
                        "service_account_name": {
                            "title": "Service Account",
                            "type": "string",
                            "default": "default"
                        },
                        "image_pull_policy": {
                            "title": "Image Pull Policy",
                            "type": "string",
                            "enum": ["Always", "IfNotPresent", "Never"],
                            "default": "IfNotPresent"
                        },
                        "command": {
                            "title": "Command",
                            "type": "array",
                            "default": ["python", "-m", "prefect.engine"]
                        },
                        "env": {
                            "title": "Environment Variables",
                            "type": "object",
                            "default": {}
                        },
                        "labels": {
                            "title": "Pod Labels",
                            "type": "object",
                            "default": {}
                        },
                        "node_selector": {
                            "title": "Node Selector",
                            "type": "object", 
                            "default": {}
                        },
                        "tolerations": {
                            "title": "Pod Tolerations",
                            "type": "array",
                            "default": []
                        },
                        "resources": {
                            "title": "Resource Requirements",
                            "type": "object",
                            "default": {
                                "requests": {"memory": "256Mi", "cpu": "100m"},
                                "limits": {"memory": "1Gi", "cpu": "1000m"}
                            }
                        }
                    }
                }
            }
        )
        
        pools = [process_pool, docker_pool, k8s_pool]
        
        for pool in pools:
            try:
                await client.create_work_pool(work_pool=pool)
                print(f"✓ Created work pool: {pool.name}")
            except Exception as e:
                print(f"✗ Failed to create {pool.name}: {str(e)}")

async def list_work_pools():
    """List all work pools"""
    async with get_client() as client:
        work_pools = await client.read_work_pools()
        print("\n=== Available Work Pools ===")
        for pool in work_pools:
            print(f"Name: {pool.name}")
            print(f"Type: {pool.type}")
            print(f"Description: {pool.description}")
            print(f"Paused: {pool.is_paused}")
            print("-" * 40)

async def show_work_pool_details(pool_name: str):
    """Show detailed work pool configuration"""
    async with get_client() as client:
        try:
            pool = await client.read_work_pool(work_pool_name=pool_name)
            print(f"\n=== Work Pool: {pool_name} ===")
            print(f"Type: {pool.type}")
            print(f"Description: {pool.description}")
            print(f"Paused: {pool.is_paused}")
            print(f"Concurrency Limit: {pool.concurrency_limit}")
            print("\nJob Template:")
            print(json.dumps(pool.base_job_template, indent=2))
        except Exception as e:
            print(f"Error reading work pool {pool_name}: {str(e)}")

def main():
    print("Work Pool Management")
    print("1. Create example work pools")
    print("2. List all work pools")
    print("3. Show work pool details")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(create_work_pools())
    elif choice == "2":
        asyncio.run(list_work_pools())
    elif choice == "3":
        pool_name = input("Enter work pool name: ").strip()
        asyncio.run(show_work_pool_details(pool_name))
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()