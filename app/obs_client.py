from obs import ObsClient
from dotenv import load_dotenv
import os

load_dotenv()

AK = os.getenv("OBS_AK")
SK = os.getenv("OBS_SK")
ENDPOINT = os.getenv("OBS_ENDPOINT")
BUCKET = os.getenv("OBS_BUCKET")

obs_client = ObsClient(access_key_id=AK, secret_access_key=SK, server=f"https://{ENDPOINT}")

def upload_file(file_bytes: bytes, object_name: str) -> str:
    # 1️⃣ Upload the file
    resp = obs_client.putObject(
        bucketName=BUCKET,
        objectKey=object_name,
        content=file_bytes
    )
    if resp.status >= 300:
        raise Exception(f"OBS upload failed: {resp.errorCode}, {resp.errorMessage}")

    # 3️⃣ Return public URL
    return f"https://{BUCKET}.{ENDPOINT}/{object_name}"