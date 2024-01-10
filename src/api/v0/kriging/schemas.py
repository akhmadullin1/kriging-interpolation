from pydantic import BaseModel

from entity.kriging import ProcessStatus


class KrigingStatusResponse(BaseModel):
    status: ProcessStatus
