"""
Simple deployment using modern serve() approach
This is the recommended way for Prefect 2.10+
"""
from prefect import serve
from task import math_operations

def simple_serve():
    """Simple serve deployment - easiest way to deploy"""
    serve(
        math_operations.to_deployment(
            name="simple-math-operations",
            description="Simple mathematical operations",
            tags=["simple", "math"],
            parameters={"x": 10, "y": 5}
        )
    )

def production_serve():
    """Production-ready serve deployment with multiple configurations"""
    serve(
        # Manual trigger
        math_operations.to_deployment(
            name="manual-math",
            description="Manual execution",
            parameters={"x": 10, "y": 5}
        ),
        
        # Scheduled every hour
        math_operations.to_deployment(
            name="hourly-math", 
            description="Runs every hour",
            schedule={"cron": "0 * * * *"},
            parameters={"x": 25, "y": 15}
        ),
        
        # Daily reports
        math_operations.to_deployment(
            name="daily-report",
            description="Daily mathematical report",
            schedule={"cron": "0 8 * * *"},
            parameters={"x": 100, "y": 50}
        ),
        
        host="0.0.0.0",
        port=8000
    )

if __name__ == "__main__":
    print("Choose deployment type:")
    print("1. Simple (single deployment)")
    print("2. Production (multiple deployments)")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        print("Starting simple deployment...")
        simple_serve()
    else:
        print("Starting production deployment...")
        production_serve()