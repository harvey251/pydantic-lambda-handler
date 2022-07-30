from handler_app import plh  # type: ignore


@plh.get("/index/")
def index_handler():
    print("made it")
    return {"message": "Hello World"}


@plh.get("/teapot/", status_code=418)
def hello_teapot():
    return {"message": "I'm a teapot"}


@plh.get("/pets/{petId}", operation_id="Create Pet")
def pets_handler(petId):
    return {"message": "Hello World"}
