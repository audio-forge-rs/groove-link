"""JSON-RPC 2.0 protocol over length-prefixed TCP frames."""

from __future__ import annotations

import json
import struct
from dataclasses import dataclass, field
from typing import Any

# Frame format: 4-byte big-endian length prefix + UTF-8 JSON payload
FRAME_HEADER_SIZE = 4
FRAME_HEADER_FORMAT = ">I"  # Big-endian unsigned 32-bit int


@dataclass
class RPCRequest:
    """JSON-RPC 2.0 request."""

    method: str
    params: dict[str, Any] = field(default_factory=dict)
    id: int | str | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"jsonrpc": "2.0", "method": self.method}
        if self.params:
            d["params"] = self.params
        if self.id is not None:
            d["id"] = self.id
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class RPCError:
    """JSON-RPC 2.0 error."""

    code: int
    message: str
    data: Any = None

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RPCError:
        return cls(code=d["code"], message=d["message"], data=d.get("data"))


@dataclass
class RPCResponse:
    """JSON-RPC 2.0 response."""

    id: int | str | None
    result: Any = None
    error: RPCError | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RPCResponse:
        error = None
        if "error" in d:
            error = RPCError.from_dict(d["error"])
        return cls(id=d.get("id"), result=d.get("result"), error=error)

    @classmethod
    def from_json(cls, data: str) -> RPCResponse:
        return cls.from_dict(json.loads(data))

    def raise_for_error(self) -> None:
        """Raise RPCException if this response is an error."""
        if self.error:
            raise RPCException(self.error)


class RPCException(Exception):
    """Exception raised when an RPC call returns an error."""

    def __init__(self, error: RPCError):
        self.error = error
        super().__init__(f"RPC Error {error.code}: {error.message}")


def encode_frame(payload: bytes) -> bytes:
    """Encode a payload with a 4-byte length prefix."""
    return struct.pack(FRAME_HEADER_FORMAT, len(payload)) + payload


def decode_frame_header(header: bytes) -> int:
    """Decode the 4-byte length prefix, return payload length."""
    return struct.unpack(FRAME_HEADER_FORMAT, header)[0]


def request_to_frame(request: RPCRequest) -> bytes:
    """Encode an RPC request as a framed message."""
    payload = request.to_json().encode("utf-8")
    return encode_frame(payload)


def batch_to_frame(requests: list[RPCRequest]) -> bytes:
    """Encode a batch of RPC requests as a framed message."""
    payload = json.dumps([r.to_dict() for r in requests]).encode("utf-8")
    return encode_frame(payload)


def parse_response(data: bytes) -> RPCResponse | list[RPCResponse]:
    """Parse a response payload (single or batch)."""
    decoded = json.loads(data.decode("utf-8"))
    if isinstance(decoded, list):
        return [RPCResponse.from_dict(d) for d in decoded]
    return RPCResponse.from_dict(decoded)
