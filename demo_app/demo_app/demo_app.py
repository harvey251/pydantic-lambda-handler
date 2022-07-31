from handler_app import plh


@plh.get("/")
def hello_handler():
    return {"message": "Hello World"}


@plh.post("/")
def create_handler():
    return {"message": "success"}
