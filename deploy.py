"""
Deployment configuration for mathematical operations workflow
Demonstrates both modern serve() and classic Deployment patterns
"""
import os
from prefect import serve
from datetime import timedelta
from task import math_operations

def create_modern_deployments():
    """Create deployments using modern flow.deploy() approach"""
    
    print("Creating deployments with modern API...")
    
    # Deployment 1: Manual trigger deployment
    try:
        math_operations.deploy(
            name="manual-math-operations",
            description="Manual execution of mathematical operations",
            tags=["math", "manual", "basic"],
            parameters={
                "x": float(os.getenv("MATH_X", 10)),
                "y": float(os.getenv("MATH_Y", 5))
            },
            work_pool_name="local-process-pool",
            job_variables={
                "working_dir": "/app",
                "env": {"PYTHONPATH": "/app"}
            }
        )
        print("✓ Created deployment 'manual-math-operations'")
    except Exception as e:
        print(f"✗ Failed to create manual deployment: {str(e)}")
    
    # Deployment 2: Scheduled every 5 minutes
    try:
        math_operations.deploy(
            name="scheduled-math-operations",
            description="Scheduled mathematical operations (every 5 minutes)",
            tags=["math", "scheduled", "interval"],
            schedule={"interval": 300},  # 5 minutes in seconds
            parameters={
                "x": float(os.getenv("MATH_X", 20)),
                "y": float(os.getenv("MATH_Y", 8))
            },
            work_pool_name="local-process-pool",
            job_variables={
                "working_dir": "/app",
                "env": {"PYTHONPATH": "/app"}
            }
        )
        print("✓ Created deployment 'scheduled-math-operations'")
    except Exception as e:
        print(f"✗ Failed to create scheduled deployment: {str(e)}")
    
    # Deployment 3: Daily cron schedule
    try:
        math_operations.deploy(
            name="daily-math-operations",
            description="Daily mathematical operations at 9 AM UTC",
            tags=["math", "daily", "cron"],
            schedule={"cron": "0 9 * * *", "timezone": "UTC"},
            parameters={
                "x": float(os.getenv("MATH_X", 100)),
                "y": float(os.getenv("MATH_Y", 25))
            },
            work_pool_name="local-process-pool",
            job_variables={
                "working_dir": "/app",
                "env": {"PYTHONPATH": "/app"}
            }
        )
        print("✓ Created deployment 'daily-math-operations'")
    except Exception as e:
        print(f"✗ Failed to create daily deployment: {str(e)}")
    
    # Deployment 4: Test deployment
    try:
        math_operations.deploy(
            name="test-math-operations",
            description="Test deployment with various parameter combinations",
            tags=["math", "test", "parameterized"],
            parameters={"x": 15, "y": 3},
            work_pool_name="local-process-pool",
            job_variables={
                "working_dir": "/app",
                "env": {"PYTHONPATH": "/app"}
            }
        )
        print("✓ Created deployment 'test-math-operations'")
    except Exception as e:
        print(f"✗ Failed to create test deployment: {str(e)}")

def deploy_all():
    """Deploy all configurations using modern API"""
    create_modern_deployments()
    
    print("\nDeployments created successfully!")
    print("You can now see them in the Prefect UI under 'Deployments' tab")
    print("Start a worker to execute scheduled flows:")
    print("  prefect worker start --pool local-process-pool")

def serve_deployments():
    """Modern serve-based deployment approach"""
    print("Starting serve-based deployments...")
    
    # This creates and starts multiple deployments in a single process
    serve(
        # Manual execution deployment
        math_operations.to_deployment(
            name="serve-manual-math",
            description="Manual math operations using serve()",
            tags=["serve", "manual", "modern"],
            parameters={"x": 10, "y": 5}
        ),
        
        # Scheduled every 10 minutes
        math_operations.to_deployment(
            name="serve-scheduled-math",
            description="Scheduled math operations every 10 minutes",
            tags=["serve", "scheduled", "modern"],
            schedule={"interval": 600},  # 10 minutes in seconds
            parameters={"x": 20, "y": 8}
        ),
        
        # Daily at 9 AM
        math_operations.to_deployment(
            name="serve-daily-math",
            description="Daily math operations at 9 AM UTC",
            tags=["serve", "daily", "modern"],
            schedule={"cron": "0 9 * * *"},
            parameters={"x": 100, "y": 25}
        ),
        
        # Test deployment with different parameters
        math_operations.to_deployment(
            name="serve-test-math",
            description="Test deployment with custom parameters",
            tags=["serve", "test", "modern"],
            parameters={"x": 15, "y": 3}
        )
    )

def deploy_choice():
    """Choose deployment method"""
    print("Choose deployment method:")
    print("1. Modern serve() approach (recommended)")
    print("2. Modern flow.deploy() approach")
    print("3. Deploy both for comparison")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        print("\n=== Using Modern serve() Approach ===")
        serve_deployments()
    elif choice == "2":
        print("\n=== Using Modern flow.deploy() Approach ===")
        deploy_all()
    elif choice == "3":
        print("\n=== Creating deployments with flow.deploy() ===")
        deploy_all()
        print("\n=== Starting Modern serve() Approach ===")
        print("Note: serve() will run continuously. Press Ctrl+C to stop.")
        serve_deployments()
    else:
        print("Invalid choice. Using modern serve() approach.")
        serve_deployments()

if __name__ == "__main__":
    deploy_choice()