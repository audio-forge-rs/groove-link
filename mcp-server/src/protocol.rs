//! Wire protocol: Length-prefixed JSON-RPC 2.0 frames
//!
//! Frame format:
//! ```text
//! ┌──────────────────┬─────────────────────────────────┐
//! │ Length (4 bytes) │ JSON-RPC 2.0 Payload (UTF-8)    │
//! │ Big-endian u32   │                                 │
//! └──────────────────┴─────────────────────────────────┘
//! ```

use anyhow::{anyhow, Result};
use serde::{Deserialize, Serialize};
use tokio::io::{AsyncReadExt, AsyncWriteExt};

/// JSON-RPC 2.0 Request
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RpcRequest {
    pub jsonrpc: String,
    pub method: String,
    #[serde(default)]
    pub params: serde_json::Value,
    pub id: serde_json::Value,
}

/// JSON-RPC 2.0 Response
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RpcResponse {
    pub jsonrpc: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub result: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<RpcError>,
    pub id: serde_json::Value,
}

/// JSON-RPC 2.0 Error
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RpcError {
    pub code: i32,
    pub message: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub data: Option<serde_json::Value>,
}

impl RpcResponse {
    pub fn success(id: serde_json::Value, result: serde_json::Value) -> Self {
        Self {
            jsonrpc: "2.0".to_string(),
            result: Some(result),
            error: None,
            id,
        }
    }

    pub fn error(id: serde_json::Value, code: i32, message: String) -> Self {
        Self {
            jsonrpc: "2.0".to_string(),
            result: None,
            error: Some(RpcError {
                code,
                message,
                data: None,
            }),
            id,
        }
    }
}

/// Read a length-prefixed frame from a stream
pub async fn read_frame<R: AsyncReadExt + Unpin>(reader: &mut R) -> Result<Vec<u8>> {
    let mut len_buf = [0u8; 4];
    reader.read_exact(&mut len_buf).await?;
    let len = u32::from_be_bytes(len_buf) as usize;

    tracing::debug!("Reading frame of {} bytes", len);

    if len > 10 * 1024 * 1024 {
        return Err(anyhow!("Frame too large: {} bytes", len));
    }

    let mut payload = vec![0u8; len];
    reader.read_exact(&mut payload).await?;

    tracing::debug!(
        "Frame payload (first 50 bytes): {}",
        String::from_utf8_lossy(&payload[..payload.len().min(50)])
    );

    Ok(payload)
}

/// Write a length-prefixed frame to a stream
pub async fn write_frame<W: AsyncWriteExt + Unpin>(writer: &mut W, payload: &[u8]) -> Result<()> {
    let len = payload.len() as u32;
    let len_bytes = len.to_be_bytes();

    tracing::info!("Writing frame: {} byte payload", len);
    tracing::info!(
        "Length prefix bytes: {:02x} {:02x} {:02x} {:02x}",
        len_bytes[0], len_bytes[1], len_bytes[2], len_bytes[3]
    );
    tracing::info!(
        "Payload first 20 bytes: {}",
        payload[..payload.len().min(20)]
            .iter()
            .map(|b| format!("{:02x}", b))
            .collect::<Vec<_>>()
            .join(" ")
    );

    writer.write_all(&len_bytes).await?;
    writer.write_all(payload).await?;
    writer.flush().await?;

    tracing::info!("Frame written successfully");
    Ok(())
}

/// Read a JSON-RPC request from a stream
pub async fn read_request<R: AsyncReadExt + Unpin>(reader: &mut R) -> Result<RpcRequest> {
    let payload = read_frame(reader).await?;
    let request: RpcRequest = serde_json::from_slice(&payload)?;
    tracing::debug!("Received request: {:?}", request);
    Ok(request)
}

/// Write a JSON-RPC response to a stream
pub async fn write_response<W: AsyncWriteExt + Unpin>(
    writer: &mut W,
    response: &RpcResponse,
) -> Result<()> {
    let payload = serde_json::to_vec(response)?;
    tracing::debug!("Sending response: {:?}", response);
    write_frame(writer, &payload).await
}

/// Read a JSON-RPC response from a stream
pub async fn read_response<R: AsyncReadExt + Unpin>(reader: &mut R) -> Result<RpcResponse> {
    let payload = read_frame(reader).await?;
    let response: RpcResponse = serde_json::from_slice(&payload)?;
    tracing::debug!("Received response: {:?}", response);
    Ok(response)
}

/// Write a JSON-RPC request to a stream
pub async fn write_request<W: AsyncWriteExt + Unpin>(
    writer: &mut W,
    request: &RpcRequest,
) -> Result<()> {
    let payload = serde_json::to_vec(request)?;
    tracing::debug!("Sending request: {:?}", request);
    write_frame(writer, &payload).await
}
