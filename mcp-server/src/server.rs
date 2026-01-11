//! TCP proxy server
//!
//! JSON-RPC proxy between Python CLI and Bitwig controller extension.
//! Claude Code uses the Python CLI via Bash - no MCP tools needed.

use anyhow::Result;
use tokio::net::TcpListener;
use tracing::{error, info};

use crate::bitwig::BitwigManager;
use crate::protocol::{self, RpcResponse};

/// Handle a single CLI connection
async fn handle_cli_connection(
    mut stream: tokio::net::TcpStream,
    bitwig: BitwigManager,
) -> Result<()> {
    let (mut reader, mut writer) = stream.split();

    loop {
        // Read request from CLI
        let request = match protocol::read_request(&mut reader).await {
            Ok(req) => req,
            Err(e) => {
                // Connection closed or error
                info!("CLI connection closed: {}", e);
                break;
            }
        };

        // Check if this is a method that produces progress notifications
        let uses_progress = request.method == "track.create";

        if uses_progress {
            // Use call_with_progress and forward notifications
            match bitwig
                .call_with_progress(&request.method, request.params.clone())
                .await
            {
                Ok((result, notifications)) => {
                    // Send notifications first
                    for notif in notifications {
                        if let Err(e) = protocol::write_notification(&mut writer, &notif).await {
                            error!("Failed to send progress notification: {}", e);
                            // Continue anyway - CLI might have disconnected
                        }
                    }
                    // Then send final response
                    let response = RpcResponse::success(request.id, result);
                    if let Err(e) = protocol::write_response(&mut writer, &response).await {
                        error!("Failed to send CLI response: {}", e);
                        break;
                    }
                }
                Err(e) => {
                    let response = RpcResponse::error(request.id, -32603, e.to_string());
                    if let Err(e) = protocol::write_response(&mut writer, &response).await {
                        error!("Failed to send CLI error response: {}", e);
                        break;
                    }
                }
            }
        } else {
            // Standard call without progress
            let response = match bitwig.call(&request.method, request.params.clone()).await {
                Ok(result) => RpcResponse::success(request.id, result),
                Err(e) => RpcResponse::error(request.id, -32603, e.to_string()),
            };

            if let Err(e) = protocol::write_response(&mut writer, &response).await {
                error!("Failed to send CLI response: {}", e);
                break;
            }
        }
    }

    Ok(())
}

/// Listen for CLI connections
pub async fn cli_listener(port: u16, bitwig: BitwigManager) -> Result<()> {
    let listener = TcpListener::bind(format!("127.0.0.1:{}", port)).await?;
    info!("CLI listener started on port {}", port);

    loop {
        match listener.accept().await {
            Ok((stream, addr)) => {
                info!("CLI connected from {}", addr);

                let bitwig = bitwig.clone();
                tokio::spawn(async move {
                    if let Err(e) = handle_cli_connection(stream, bitwig).await {
                        error!("CLI handler error: {}", e);
                    }
                });
            }
            Err(e) => {
                error!("Failed to accept CLI connection: {}", e);
            }
        }
    }
}
