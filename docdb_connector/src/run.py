import uvicorn

# from docdb_connector.main import app
if __name__ == "__main__":
    uvicorn.run(
        # app=app
        "docdb_connector.main:app"
        , host="0.0.0.0"
        , port=8081)
