import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from transmission_rpc import Client, error
from qbittorrentapi import Client as QBClient, LoginFailed

load_dotenv()

DOWNLOAD_CLIENT = os.getenv("DOWNLOAD_CLIENT", "transmission")

# Transmission configuration
TRANSMISSION_HOST = os.getenv("TRANSMISSION_HOST")
TRANSMISSION_PORT = int(os.getenv("TRANSMISSION_PORT", "9091"))
TRANSMISSION_USERNAME = os.getenv("TRANSMISSION_USERNAME")
TRANSMISSION_PASSWORD = os.getenv("TRANSMISSION_PASSWORD")

# qBittorrent configuration
QBITTORRENT_HOST = os.getenv("QBITTORRENT_HOST")
QBITTORRENT_PORT = int(os.getenv("QBITTORRENT_PORT", "8080"))
QBITTORRENT_USERNAME = os.getenv("QBITTORRENT_USERNAME")
QBITTORRENT_PASSWORD = os.getenv("QBITTORRENT_PASSWORD")

app = FastAPI()

def get_transmission_client():
    try:
        client = Client(
            host=TRANSMISSION_HOST,
            port=TRANSMISSION_PORT,
            username=TRANSMISSION_USERNAME,
            password=TRANSMISSION_PASSWORD,
        )
        # Simple call to test connection
        client.session_stats()
        return client
    except Exception:
        return None

def get_qbittorrent_client():
    try:
        client = QBClient(
            host=QBITTORRENT_HOST,
            port=QBITTORRENT_PORT,
            username=QBITTORRENT_USERNAME,
            password=QBITTORRENT_PASSWORD,
        )
        # Test connection
        client.auth_log_in()
        return client
    except (LoginFailed, Exception):
        return None

def get_download_client():
    if DOWNLOAD_CLIENT == "qbittorrent":
        return get_qbittorrent_client()
    else:
        return get_transmission_client()

@app.get("/test-connection")
def test_connection():
    client = get_download_client()
    if client:
        if DOWNLOAD_CLIENT == "qbittorrent":
            return {"message": "Connection to qBittorrent successful."}
        else:
            return {"message": "Connection to Transmission successful."}
    else:
        if DOWNLOAD_CLIENT == "qbittorrent":
            return {"message": "Connection to qBittorrent failed."}
        else:
            return {"message": "Connection to Transmission failed."}

class DownloadRequest(BaseModel):
    torrent_url: str
    download_dir: str

@app.post("/download-torrent")
def download_torrent(req: DownloadRequest):
    client = get_download_client()
    if not client:
        if DOWNLOAD_CLIENT == "qbittorrent":
            raise HTTPException(status_code=500, detail="Connection to qBittorrent failed.")
        else:
            raise HTTPException(status_code=500, detail="Connection to Transmission failed.")
    
    try:
        if DOWNLOAD_CLIENT == "qbittorrent":
            # qBittorrent download
            torrent = client.torrents_add(urls=req.torrent_url, save_path=req.download_dir)
            return {"message": "Download triggered successfully in qBittorrent."}
        else:
            # Transmission download
            torrent = client.add_torrent(req.torrent_url, download_dir=req.download_dir)
            return {"message": "Download triggered successfully.", "torrent_id": torrent.id}
    except Exception as e:
        if DOWNLOAD_CLIENT == "qbittorrent":
            raise HTTPException(status_code=500, detail=f"Failed to trigger download in qBittorrent: {str(e)}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to trigger download: {str(e)}")
