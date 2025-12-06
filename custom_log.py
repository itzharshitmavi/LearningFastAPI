from fastapi.requests import Request

def log(tag="", message="", request: Request = None):
  with open("log.txt", "w+") as log:
    log.write(f"{tag}: {message}\n")
    log.write(f"\t{request.url}\n")

# concurrency (async/await) -> functionality can be asynchronous, we don't want the execution to block, await means the process can be paused, async defines a function with suspendable points (if we dont want to put load on the server by giving request upron request upron request)
# templates -> provide ready made HTML (and CSS) content, any templating engine
# middleware -> function that intercepts the request and response, access to all related info without actually going and modifying each individual call, we can do processing before and after a request and we can modify the response appropriately
# background task -> functionality to be run after the call has been completed, can have access to request response
# websockets -> two way communication, keep connection open