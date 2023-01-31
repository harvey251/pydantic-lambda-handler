import logging
from collections import namedtuple
from typing import NamedTuple

from pydantic_lambda_handler.hooks.open_api_gen_hook import APIGenerationHook
from pydantic_lambda_handler.main import PydanticLambdaHandler

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)



# plh = PydanticLambdaHandler(title="PydanticLambdaHandler", logger=logger, hooks=[APIGenerationHook])
# plh.my_hook = APIGenerationHook

#  Maybe it should be a dataclass?
class Hooks(NamedTuple):
    api_generation: APIGenerationHook = APIGenerationHook()
    tracer: str

class DXPLH(PydanticLambdaHandler):
    hooks: Hooks

hooks = Hooks()

plh = DXPLH(title="PydanticLambdaHandler", logger=logger, hooks=hooks)

plh.hooks.api_generation
plh.hooks.tracer.
# needs to auto complete
# needs access to hook parameters
# needs access to other hooks