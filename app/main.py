# (1.) FastAPI application entry point
# (2.) Initializes the workflow engine API server

from fastapi import FastAPI

from app.api.routes import router

# (1.) Create FastAPI application instance
# (2.) Configure metadata for API documentation
app = FastAPI(
    title="Agent Workflow Engine",
    description="A minimal graph-based workflow execution system",
    version="1.0.0"
)

# (1.) Include API routes
# (2.) All graph-related endpoints under /graph prefix
app.include_router(router, prefix="/graph", tags=["graph"])


@app.get("/health")
async def health_check():
    """
    (1.) Health check endpoint
    (2.) Returns service status for monitoring
    """
    return {"status": "healthy"}
