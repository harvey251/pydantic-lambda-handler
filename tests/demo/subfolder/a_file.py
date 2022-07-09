from tests.demo.app import app


@app.get("/index/")
def index_handler():
    return {"message": "Hello World"}


@app.get("/teapot/", status_code=418)
def hello_teapot():
    return {"message": "I'm a teapot"}


@app.get("/pets/{petId}")
def pets_handler(petId):
    return {"message": "Hello World"}
