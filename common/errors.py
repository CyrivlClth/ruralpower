from dataclasses import dataclass


@dataclass
class HandlerException(Exception):
    status_code: int
    message: str

    def to_dict(self) -> dict:
        return dict(code=self.status_code, message=self.message)
