import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from transmission_rpc import Client, error

load_dotenv()

TRANSMISSION_HOST = os.getenv("TRANSMISSION_HOST")
TRANSMISSION_PORT = int(os.getenv("TRANSMISSION_PORT", "9091"))
TRANSMISSION_USERNAME = os.getenv("TRANSMISSION_USERNAME")
TRANSMISSION_PASSWORD = os.getenv("TRANSMISSION_PASSWORD")

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

@app.get("/test-connection")
def test_connection():
    client = get_transmission_client()
    if client:
        return {"message": "Connection to Transmission successful."}
    else:
        return {"message": "Connection to Transmission failed."}

class DownloadRequest(BaseModel):
    torrent_url: str
    download_dir: str

@app.post("/download-torrent")
def download_torrent(req: DownloadRequest):
    client = get_transmission_client()
    if not client:
        raise HTTPException(status_code=500, detail="Connection to Transmission failed.")
    try:
        torrent = client.add_torrent(req.torrent_url, download_dir=req.download_dir)
        return {"message": "Download triggered successfully.", "torrent_id": torrent.id}
    except error.TransmissionError as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger download: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
