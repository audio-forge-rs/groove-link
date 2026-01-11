"""JSON-RPC client for communicating with the Bitwig controller extension."""

from __future__ import annotations

import logging
import socket
from typing import Any

from .protocol import (
    FRAME_HEADER_SIZE,
    RPCException,
    RPCRequest,
    RPCResponse,
    batch_to_frame,
    decode_frame_header,
    parse_response,
    request_to_frame,
)

logger = logging.getLogger(__name__)

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8418  # CLI port on MCP server (Bitwig connects to 8417)
DEFAULT_TIMEOUT = 5.0


class BitwigClient:
    """Client for communicating with the Bitwig controller extension.

    Uses JSON-RPC 2.0 over length-prefixed TCP frames.
    """

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: socket.socket | None = None
        self._request_id = 0

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def connect(self) -> None:
        """Connect to the Bitwig controller extension."""
        if self._sock is not None:
            return
        logger.debug("Connecting to %s:%d", self.host, self.port)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(self.timeout)
        self._sock.connect((self.host, self.port))
        logger.debug("Connected")

    def disconnect(self) -> None:
        """Disconnect from the Bitwig controller extension."""
        if self._sock is not None:
            logger.debug("Disconnecting")
            self._sock.close()
            self._sock = None

    def __enter__(self) -> BitwigClient:
        self.connect()
        return self

    def __exit__(self, *args: object) -> None:
        self.disconnect()

    def _send(self, data: bytes) -> None:
        """Send data to the server."""
        if self._sock is None:
            raise RuntimeError("Not connected")
        logger.debug("Sending %d bytes: %s", len(data), data[:20].hex())
        self._sock.sendall(data)

    def _recv_exactly(self, n: int) -> bytes:
        """Receive exactly n bytes from the server."""
        if self._sock is None:
            raise RuntimeError("Not connected")
        chunks: list[bytes] = []
        remaining = n
        while remaining > 0:
            chunk = self._sock.recv(remaining)
            if not chunk:
                raise ConnectionError("Connection closed by server")
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    def _recv_frame(self) -> bytes:
        """Receive a length-prefixed frame from the server."""
        header = self._recv_exactly(FRAME_HEADER_SIZE)
        payload_length = decode_frame_header(header)
        logger.debug("Receiving frame of %d bytes", payload_length)
        return self._recv_exactly(payload_length)

    def call(self, method: str, params: dict[str, Any] | None = None) -> Any:
        """Make a single RPC call and return the result.

        Args:
            method: The RPC method name (e.g., "info.get")
            params: Optional parameters dict

        Returns:
            The result from the RPC call

        Raises:
            RPCException: If the server returns an error
            ConnectionError: If not connected or connection lost
        """
        request = RPCRequest(method=method, params=params or {}, id=self._next_id())
        logger.debug("Calling %s(%s)", method, params)

        self._send(request_to_frame(request))
        response_data = self._recv_frame()
        response = parse_response(response_data)

        if isinstance(response, list):
            raise RuntimeError("Unexpected batch response for single call")

        response.raise_for_error()
        logger.debug("Result: %s", response.result)
        return response.result

    def batch(self, calls: list[tuple[str, dict[str, Any] | None]]) -> list[Any]:
        """Make a batch of RPC calls and return the results.

        Args:
            calls: List of (method, params) tuples

        Returns:
            List of results in the same order as the calls

        Raises:
            RPCException: If any call returns an error (first error raised)
            ConnectionError: If not connected or connection lost
        """
        requests = [
            RPCRequest(method=method, params=params or {}, id=self._next_id())
            for method, params in calls
        ]
        logger.debug("Batch calling %d methods", len(requests))

        self._send(batch_to_frame(requests))
        response_data = self._recv_frame()
        responses = parse_response(response_data)

        if not isinstance(responses, list):
            raise RuntimeError("Unexpected single response for batch call")

        # Sort responses by id to match request order
        id_to_response = {r.id: r for r in responses}
        results: list[Any] = []
        for req in requests:
            resp = id_to_response.get(req.id)
            if resp is None:
                raise RuntimeError(f"Missing response for request {req.id}")
            resp.raise_for_error()
            results.append(resp.result)

        return results


def get_client(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    timeout: float = DEFAULT_TIMEOUT,
) -> BitwigClient:
    """Get a connected BitwigClient instance.

    This is a convenience function for one-off calls.
    For multiple calls, use BitwigClient as a context manager.
    """
    client = BitwigClient(host=host, port=port, timeout=timeout)
    client.connect()
    return client
