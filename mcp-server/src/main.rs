//! Groove MCP Server
//!
//! MCP server that bridges Claude Code to Bitwig Studio.
//!
//! Architecture:
//! - Bitwig extension connects to us on port 8417 as a TCP client
//! - Claude Code talks to us via MCP over stdio
//! - CLI talks to us via JSON-RPC over TCP on port 8418

mod bitwig;
mod protocol;
mod server;

use anyhow::Result;
use tracing::info;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

const BITWIG_PORT: u16 = 8417;
const CLI_PORT: u16 = 8418;

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logging
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::new(
            std::env::var("RUST_LOG").unwrap_or_else(|_| "info".into()),
        ))
        .with(tracing_subscriber::fmt::layer().with_writer(std::io::stderr))
        .init();

    info!("Groove MCP Server starting...");
    info!("Bitwig port: {}", BITWIG_PORT);
    info!("CLI port: {}", CLI_PORT);

    // Create the shared Bitwig connection manager
    let bitwig_manager = bitwig::BitwigManager::new();

    // Start the Bitwig TCP listener
    let bitwig_handle = {
        let manager = bitwig_manager.clone();
        tokio::spawn(async move {
            if let Err(e) = bitwig::listen(BITWIG_PORT, manager).await {
                tracing::error!("Bitwig listener error: {}", e);
            }
        })
    };

    // Start the CLI TCP listener
    let cli_handle = {
        let manager = bitwig_manager.clone();
        tokio::spawn(async move {
            if let Err(e) = server::cli_listener(CLI_PORT, manager).await {
                tracing::error!("CLI listener error: {}", e);
            }
        })
    };

    // Run MCP server over stdio only if stdin is a TTY or --stdio flag is passed
    // For now, skip MCP stdio when running as daemon
    let run_stdio = std::env::args().any(|arg| arg == "--stdio");

    if run_stdio {
        let manager = bitwig_manager.clone();
        tokio::spawn(async move {
            if let Err(e) = server::run_mcp_stdio(manager).await {
                tracing::error!("MCP server error: {}", e);
            }
        });
    }

    // Wait for TCP listeners
    tokio::select! {
        _ = bitwig_handle => info!("Bitwig listener stopped"),
        _ = cli_handle => info!("CLI listener stopped"),
    }

    Ok(())
}
