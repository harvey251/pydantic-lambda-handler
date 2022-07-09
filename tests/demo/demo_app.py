from tests.demo.app import app


@app.get("/")
def hello_handler():
    return {"message": "Hello World"}


@app.post("/")
def create_handler():
    return {"message": "success"}
