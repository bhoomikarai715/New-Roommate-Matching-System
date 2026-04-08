try:
    from backend.app import app
except Exception as e:
    import traceback
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    app = FastAPI()
    
    @app.get("/{rest_of_path:path}")
    async def catch_all(rest_of_path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Backend Initialization Failed",
                "details": str(e),
                "traceback": traceback.format_exc()
            }
        )
