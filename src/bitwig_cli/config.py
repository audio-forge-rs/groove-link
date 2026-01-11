"""Configuration for the Bitwig CLI."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# Default connection settings
DEFAULT_HOST = "localhost"
DEFAULT_RPC_PORT = 8417
DEFAULT_OSC_PORT = 8418
DEFAULT_TIMEOUT = 5.0

# Environment variable names
ENV_HOST = "BITWIG_HOST"
ENV_RPC_PORT = "BITWIG_RPC_PORT"
ENV_OSC_PORT = "BITWIG_OSC_PORT"


@dataclass
class Config:
    """Configuration for connecting to the Bitwig controller."""

    host: str = DEFAULT_HOST
    rpc_port: int = DEFAULT_RPC_PORT
    osc_port: int = DEFAULT_OSC_PORT
    timeout: float = DEFAULT_TIMEOUT
    verbose: bool = False

    @classmethod
    def from_env(cls) -> Config:
        """Load configuration from environment variables."""
        return cls(
            host=os.environ.get(ENV_HOST, DEFAULT_HOST),
            rpc_port=int(os.environ.get(ENV_RPC_PORT, DEFAULT_RPC_PORT)),
            osc_port=int(os.environ.get(ENV_OSC_PORT, DEFAULT_OSC_PORT)),
        )


def get_config_dir() -> Path:
    """Get the configuration directory for bitwig-cli."""
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        return Path(xdg_config) / "bitwig-cli"
    return Path.home() / ".config" / "bitwig-cli"
