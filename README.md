# FastAPI Transmission Backend

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure Transmission connection in `.env`:
   ```
   TRANSMISSION_HOST=localhost
   TRANSMISSION_PORT=9091
   TRANSMISSION_USERNAME=your_username
   TRANSMISSION_PASSWORD=your_password
   ```

3. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

## Endpoints

### 1. Test Transmission Connectivity

- **GET** `/test-connection`
- Returns success or failure message for Transmission connection.

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

- Ensure Transmission is running and accessible with the credentials provided in `.env`.
- This backend uses Transmission v3.00 and `transmission-rpc` Python library.
