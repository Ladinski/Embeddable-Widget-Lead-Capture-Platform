from fastapi import FastAPI


app = FastAPI(
    title="Embeddable Widget & Lead Capture API",
    description="Backend API for managing embeddable widgets and handling public lead submissions.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Embeddable Widget & Lead Capture API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}