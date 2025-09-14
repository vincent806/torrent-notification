## Purpose

This app acts as a backend tool to send torrent URLs to Transmission or qBittorrent downloaders. It is designed for integration with an MCP server and will serve as a component of a torrent operation agent, enabling automated torrent management and remote download operations.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure download client connection in `.env`:
   ```
   DOWNLOAD_CLIENT=transmission  # Options: transmission, qbittorrent

   # Transmission configuration
   TRANSMISSION_HOST=localhost
   TRANSMISSION_PORT=9091
   TRANSMISSION_USERNAME=your_username
   TRANSMISSION_PASSWORD=your_password

   # qBittorrent configuration
   QBITTORRENT_HOST=localhost
   QBITTORRENT_PORT=8080
   QBITTORRENT_USERNAME=admin
   QBITTORRENT_PASSWORD=adminadmin
   ```

3. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

## Endpoints

### 1. Test Download Client Connectivity

- **GET** `/test-connection`
- Returns success or failure message for the configured download client (Transmission or qBittorrent).

### 2. Trigger Torrent Download

- **POST** `/download-torrent`
- Request body (JSON):
  ```json
  {
    "torrent_url": "http://example.com/file.torrent",
    "download_dir": "/path/to/remote/folder"
  }
  ```
- Returns message if download is triggered successfully or failed.

## Notes

- Set `DOWNLOAD_CLIENT` in `.env` to choose between Transmission or qBittorrent
- Ensure the selected download client is running and accessible with the credentials provided in `.env`
- This backend supports both Transmission v3.00 and qBittorrent
