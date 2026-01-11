//! MCP and CLI servers
//!
//! - MCP server over stdio for Claude Code
//! - JSON-RPC server over TCP for CLI

use anyhow::Result;
use rmcp::{
    handler::server::tool::ToolRouter,
    handler::server::ServerHandler,
    model::*,
    tool, tool_router, tool_handler,
    ServiceExt,
};
use tokio::net::TcpListener;
use tracing::{error, info};

use crate::bitwig::BitwigManager;
use crate::protocol::{self, RpcResponse};

/// MCP Server with Bitwig tools
#[derive(Clone)]
pub struct GrooveMcpServer {
    bitwig: BitwigManager,
    tool_router: ToolRouter<Self>,
}

#[tool_handler(router = self.tool_router)]
impl ServerHandler for GrooveMcpServer {}

#[tool_router]
impl GrooveMcpServer {
    pub fn new(bitwig: BitwigManager) -> Self {
        Self {
            bitwig,
            tool_router: Self::tool_router(),
        }
    }

    /// Get Bitwig and controller information
    #[tool(description = "Get Bitwig Studio and controller extension information")]
    async fn bitwig_info(&self) -> String {
        match self.bitwig.call("info.get", serde_json::json!({})).await {
            Ok(result) => {
                serde_json::to_string_pretty(&result).unwrap_or_else(|_| result.to_string())
            }
            Err(e) => format!("Error: {}", e),
        }
    }

    /// List tracks in Bitwig
    #[tool(description = "List all tracks in the current Bitwig project")]
    async fn bitwig_list_tracks(&self) -> String {
        match self.bitwig.call("list.tracks", serde_json::json!({})).await {
            Ok(result) => {
                serde_json::to_string_pretty(&result).unwrap_or_else(|_| result.to_string())
            }
            Err(e) => format!("Error: {}", e),
        }
    }

    /// Check if Bitwig is connected
    #[tool(description = "Check if Bitwig Studio is connected to the MCP server")]
    async fn bitwig_status(&self) -> String {
        let connected = self.bitwig.is_connected().await;
        format!("Bitwig connected: {}", connected)
    }
}

/// Run MCP server over stdio for Claude Code
pub async fn run_mcp_stdio(bitwig: BitwigManager) -> Result<()> {
    info!("Starting MCP server over stdio");

    let server = GrooveMcpServer::new(bitwig);

    // Create stdio transport
    let stdin = tokio::io::stdin();
    let stdout = tokio::io::stdout();
    let transport = (stdin, stdout);

    // Start the MCP server
    let running_server = server.serve(transport).await?;

    // Wait for the server to finish
    let _quit_reason = running_server.waiting().await?;

    info!("MCP server stopped");
    Ok(())
}

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

        // Dispatch to Bitwig
        let response = match bitwig.call(&request.method, request.params.clone()).await {
            Ok(result) => RpcResponse::success(request.id, result),
            Err(e) => RpcResponse::error(request.id, -32603, e.to_string()),
        };

        // Send response back to CLI
        if let Err(e) = protocol::write_response(&mut writer, &response).await {
            error!("Failed to send CLI response: {}", e);
            break;
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
