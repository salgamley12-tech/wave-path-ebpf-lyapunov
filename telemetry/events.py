from dataclasses import dataclass, asdict
import json

@dataclass(frozen=True)
class Event:
    timestamp: float
    source: str
    event_type: str
    bytes: int=0
    pid: int=0
    src_ip: str=''
    dst_ip: str=''
    authorized: bool=True

def to_json(event: Event) -> str:
    return json.dumps(asdict(event), sort_keys=True)
