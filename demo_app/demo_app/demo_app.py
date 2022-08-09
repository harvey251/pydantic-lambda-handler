from handler_app import plh


@plh.get("/hello")
def hello_handler():
    return {"message": "Hello World"}


@plh.post("/hello")
def create_handler():
    return {"message": "success"}
