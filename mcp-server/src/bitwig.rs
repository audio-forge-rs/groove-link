//! Bitwig connection manager
//!
//! Manages TCP connections from Bitwig Studio controller extensions.
//! Bitwig connects to us as a client (inverted from typical server model).

use anyhow::{anyhow, Result};
use std::sync::Arc;
use tokio::io::{ReadHalf, WriteHalf};
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::{Mutex, RwLock};
use tracing::{error, info, warn};

use crate::protocol::{self, RpcRequest};

/// A single Bitwig connection
struct BitwigConnection {
    reader: Mutex<ReadHalf<TcpStream>>,
    writer: Mutex<WriteHalf<TcpStream>>,
    request_id: Mutex<u64>,
}

impl BitwigConnection {
    fn new(stream: TcpStream) -> Self {
        let (reader, writer) = tokio::io::split(stream);
        Self {
            reader: Mutex::new(reader),
            writer: Mutex::new(writer),
            request_id: Mutex::new(0),
        }
    }

    async fn next_id(&self) -> u64 {
        let mut id = self.request_id.lock().await;
        *id += 1;
        *id
    }

    /// Send a request to Bitwig and wait for response
    async fn call(&self, method: &str, params: serde_json::Value) -> Result<serde_json::Value> {
        let id = self.next_id().await;

        let request = RpcRequest {
            jsonrpc: "2.0".to_string(),
            method: method.to_string(),
            params,
            id: serde_json::json!(id),
        };

        // Send request
        {
            let mut writer = self.writer.lock().await;
            protocol::write_request(&mut *writer, &request).await?;
        }

        // Read response
        let response = {
            let mut reader = self.reader.lock().await;
            protocol::read_response(&mut *reader).await?
        };

        // Check for error
        if let Some(error) = response.error {
            return Err(anyhow!("RPC error {}: {}", error.code, error.message));
        }

        response
            .result
            .ok_or_else(|| anyhow!("No result in response"))
    }
}

/// Manager for Bitwig connections
#[derive(Clone)]
pub struct BitwigManager {
    connection: Arc<RwLock<Option<Arc<BitwigConnection>>>>,
}

impl BitwigManager {
    pub fn new() -> Self {
        Self {
            connection: Arc::new(RwLock::new(None)),
        }
    }

    /// Set the active Bitwig connection
    async fn set_connection(&self, conn: BitwigConnection) {
        let mut lock = self.connection.write().await;
        *lock = Some(Arc::new(conn));
        info!("Bitwig connection established");
    }

    /// Clear the active connection
    async fn clear_connection(&self) {
        let mut lock = self.connection.write().await;
        *lock = None;
        info!("Bitwig connection cleared");
    }

    /// Check if Bitwig is connected
    pub async fn is_connected(&self) -> bool {
        self.connection.read().await.is_some()
    }

    /// Call a method on Bitwig
    pub async fn call(&self, method: &str, params: serde_json::Value) -> Result<serde_json::Value> {
        let conn = {
            let lock = self.connection.read().await;
            lock.clone()
        };

        match conn {
            Some(conn) => conn.call(method, params).await,
            None => Err(anyhow!("Bitwig not connected")),
        }
    }
}

/// Listen for Bitwig connections
pub async fn listen(port: u16, manager: BitwigManager) -> Result<()> {
    let listener = TcpListener::bind(format!("127.0.0.1:{}", port)).await?;
    info!("Bitwig listener started on port {}", port);

    loop {
        match listener.accept().await {
            Ok((stream, addr)) => {
                info!("Bitwig connected from {}", addr);

                // Set TCP_NODELAY for lower latency
                if let Err(e) = stream.set_nodelay(true) {
                    warn!("Failed to set TCP_NODELAY: {}", e);
                }

                let conn = BitwigConnection::new(stream);
                manager.set_connection(conn).await;

                // TODO: Handle disconnection detection
                // For now, we just replace the connection on new connect
            }
            Err(e) => {
                error!("Failed to accept Bitwig connection: {}", e);
            }
        }
    }
}
