try:
    from backend.app import app
except Exception as e:
    import traceback
    from fastapi import FastAPI
    from fastapi.requests import Request
    from fastapi.responses import JSONResponse
    
    app = FastAPI()
    
    error_traceback = traceback.format_exc()
    
    @app.middleware("http")
    async def catch_all_errors(request: Request, call_next):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Backend Startup Failed",
                "details": str(e),
                "traceback": error_traceback
            }
        )
