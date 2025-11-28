from dataclasses import dataclass
from typing import Any, Dict, Union
import uuid


@dataclass
class MessageDTO:
    id: Union[int , uuid.UUID]
    message: str
    extra_data: Dict[str, Any]