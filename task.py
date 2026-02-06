import logging
import os
from typing import Tuple
from prefect import task, flow, get_run_logger
from prefect.logging import get_logger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@task(retries=2, retry_delay_seconds=1)
def add(x: float, y: float) -> float:
    """Add two numbers with logging and error handling."""
    logger = get_run_logger()
    
    try:
        logger.info(f"Adding {x} + {y}")
        
        # Validate inputs
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Both inputs must be numbers")
        
        result = x + y
        logger.info(f"Addition result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in addition task: {str(e)}")
        raise

@task(retries=2, retry_delay_seconds=1)
def multiply(x: float, y: float) -> float:
    """Multiply two numbers with logging and error handling."""
    logger = get_run_logger()
    
    try:
        logger.info(f"Multiplying {x} * {y}")
        
        # Validate inputs
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Both inputs must be numbers")
        
        result = x * y
        logger.info(f"Multiplication result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in multiplication task: {str(e)}")
        raise

@task(retries=2, retry_delay_seconds=1)
def subtract(x: float, y: float) -> float:
    """Subtract two numbers with logging and error handling."""
    logger = get_run_logger()
    
    try:
        logger.info(f"Subtracting {x} - {y}")
        
        # Validate inputs
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Both inputs must be numbers")
        
        result = x - y
        logger.info(f"Subtraction result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in subtraction task: {str(e)}")
        raise

@task(retries=1)
def summarize_results(sum_result: float, product_result: float, difference_result: float) -> dict:
    """Create a summary of all mathematical operations."""
    logger = get_run_logger()
    
    try:
        logger.info("Creating summary of all results")
        
        summary = {
            "addition": sum_result,
            "multiplication": product_result,
            "subtraction": difference_result,
            "total_operations": 3,
            "max_value": max(sum_result, product_result, difference_result),
            "min_value": min(sum_result, product_result, difference_result)
        }
        
        logger.info(f"Summary created: {summary}")
        return summary
        
    except Exception as e:
        logger.error(f"Error creating summary: {str(e)}")
        raise

@flow(name="mathematical-operations", log_prints=True, validate_parameters=True)
def math_operations(x: float = None, y: float = None) -> dict:
    """
    Execute mathematical operations on two numbers.
    
    Args:
        x: First number (defaults to environment variable or 10)
        y: Second number (defaults to environment variable or 5)
    
    Returns:
        Dictionary containing all results and summary
    """
    logger = get_run_logger()
    
    # Get values from environment variables if not provided
    if x is None:
        x = float(os.getenv("MATH_X", 10))
    if y is None:
        y = float(os.getenv("MATH_Y", 5))
    
    logger.info(f"Starting mathematical operations flow with x={x}, y={y}")
    
    try:
        # Execute mathematical operations
        sum_result = add(x, y)
        product_result = multiply(x, y)
        difference_result = subtract(x, y)
        
        # Create summary
        summary = summarize_results(sum_result, product_result, difference_result)
        
        # Create final result
        final_result = {
            "inputs": {"x": x, "y": y},
            "results": {
                "addition": sum_result,
                "multiplication": product_result,
                "subtraction": difference_result
            },
            "summary": summary
        }
        
        logger.info(f"Flow completed successfully: {final_result}")
        return final_result
        
    except Exception as e:
        logger.error(f"Flow failed with error: {str(e)}")
        raise

if __name__ == "__main__":
    # Configuration from environment variables
    x_value = float(os.getenv("MATH_X", 10))
    y_value = float(os.getenv("MATH_Y", 5))
    
    print(f"Running mathematical operations with x={x_value}, y={y_value}")
    
    # Run the flow
    result = math_operations(x_value, y_value)
    
    print("\n" + "="*50)
    print("FINAL RESULTS:")
    print("="*50)
    print(f"Addition: {result['results']['addition']}")
    print(f"Multiplication: {result['results']['multiplication']}")
    print(f"Subtraction: {result['results']['subtraction']}")
    print(f"Max value: {result['summary']['max_value']}")
    print(f"Min value: {result['summary']['min_value']}")
    print("="*50)