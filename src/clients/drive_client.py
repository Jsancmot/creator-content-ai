import io
import json
import logging
from typing import List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

logger = logging.getLogger(__name__)


class DriveClient:
    def __init__(self, service_account_json: str, credentials_path: Optional[str] = None):
        self.service_account_json = service_account_json
        self.credentials_path = credentials_path
        self._service = None
        self.input_folder_id: Optional[str] = None
        self.output_folder_id: Optional[str] = None

    def _get_service(self):
        if self._service is None:
            if self.service_account_json:
                credentials_info = json.loads(self.service_account_json)
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info,
                    scopes=['https://www.googleapis.com/auth/drive']
                )
            elif self.credentials_path:
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=['https://www.googleapis.com/auth/drive']
                )
            else:
                raise ValueError("No credentials provided")

            self._service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
        return self._service

    def list_images(self, folder_id: str) -> List[dict]:
        service = self._get_service()
        
        query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
        
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType, createdTime, modifiedTime)",
            orderBy="createdTime desc"
        ).execute()
        
        files = results.get('files', [])
        logger.info(f"Found {len(files)} images in folder {folder_id}")
        return files

    def download_image(self, file_id: str) -> bytes:
        service = self._get_service()
        
        request = service.files().get_media(fileId=file_id)
        content = request.execute()
        
        logger.info(f"Downloaded image {file_id} ({len(content)} bytes)")
        return content

    def get_file_metadata(self, file_id: str) -> dict:
        service = self._get_service()
        
        file = service.files().get(
            fileId=file_id,
            fields="id, name, mimeType, thumbnailLink"
        ).execute()
        
        return file

    def upload_image(self, folder_id: str, file_name: str, content: bytes, mime_type: str = "image/jpeg") -> str:
        service = self._get_service()
        
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        
        media = MediaInMemoryUpload(content, mimetype=mime_type, resumable=True)
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        logger.info(f"Uploaded image {file_name} to folder {folder_id}, file ID: {file['id']}")
        return file['id']

    def get_mime_type(self, file_id: str) -> str:
        service = self._get_service()
        file = service.files().get(fileId=file_id, fields="mimeType").execute()
        return file.get('mimeType', 'image/jpeg')