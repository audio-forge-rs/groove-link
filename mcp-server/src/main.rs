//! Groove Link Server
//!
//! TCP proxy between Python CLI and Bitwig Studio controller extension.
//!
//! Architecture:
//! - Bitwig extension connects to us on port 8417 as a TCP client
//! - Python CLI connects to us on port 8418
//! - We forward JSON-RPC requests between them

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

    info!("Groove Link Server starting...");
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

    // Wait for TCP listeners
    tokio::select! {
        _ = bitwig_handle => info!("Bitwig listener stopped"),
        _ = cli_handle => info!("CLI listener stopped"),
    }

    Ok(())
}
