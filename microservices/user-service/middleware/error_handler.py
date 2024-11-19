from fastapi import HTTPException

def handle_error(message: str, exception: Exception):
    """
    Handle generic errors by raising an HTTPException with status code 500.
    """
    raise HTTPException(status_code=500, detail=f"{message}: {str(exception)}")

def handle_invalid_id(message: str):
    """
    Handle invalid ObjectId format errors by raising an HTTPException with status code 400.
    """
    raise HTTPException(status_code=400, detail=message)

def handle_not_found(message: str):
    """
    Handle not-found errors by raising an HTTPException with status code 404.
    """
    raise HTTPException(status_code=404, detail=message)
