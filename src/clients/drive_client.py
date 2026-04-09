"""Google Drive client module.

Provides functionality to interact with Google Drive API for listing,
downloading, and uploading images.
"""

import json
import logging
from typing import List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload


logger = logging.getLogger(__name__)


class DriveClient:
    """Client for interacting with Google Drive API.

    Attributes:
        service_account_json: JSON string containing service account credentials.
        credentials_path: Path to a service account JSON file.
        input_folder_id: ID of the Google Drive folder to monitor for new images.
        output_folder_id: ID of the Google Drive folder to save processed images.
    """

    def __init__(
        self,
        service_account_json: str = "",
        credentials_path: Optional[str] = None
    ):
        """Initialize the Drive client.

        Args:
            service_account_json: JSON string with service account credentials.
            credentials_path: Path to a credentials JSON file.
        """
        self.service_account_json = service_account_json
        self.credentials_path = credentials_path
        self._service = None
        self.input_folder_id: Optional[str] = None
        self.output_folder_id: Optional[str] = None

    def _get_service(self):
        """Get or create the Google Drive service instance.

        Returns:
            The Google Drive service object.

        Raises:
            ValueError: If no credentials are provided.
        """
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
        """List all image files in a specific folder.

        Args:
            folder_id: The ID of the Google Drive folder.

        Returns:
            List of dictionaries containing file metadata.
        """
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
        """Download an image file from Google Drive.

        Args:
            file_id: The ID of the file to download.

        Returns:
            The image file content as bytes.
        """
        service = self._get_service()

        request = service.files().get_media(fileId=file_id)
        content = request.execute()

        logger.info(f"Downloaded image {file_id} ({len(content)} bytes)")
        return content

    def get_file_metadata(self, file_id: str) -> dict:
        """Get metadata for a file.

        Args:
            file_id: The ID of the file.

        Returns:
            Dictionary containing file metadata.
        """
        service = self._get_service()

        file = service.files().get(
            fileId=file_id,
            fields="id, name, mimeType, thumbnailLink"
        ).execute()

        return file

    def upload_image(
        self,
        folder_id: str,
        file_name: str,
        content: bytes,
        mime_type: str = "image/jpeg"
    ) -> str:
        """Upload an image file to Google Drive.

        Args:
            folder_id: The ID of the destination folder.
            file_name: Name for the uploaded file.
            content: The image content as bytes.
            mime_type: MIME type of the image (default: image/jpeg).

        Returns:
            The ID of the uploaded file.
        """
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
        """Get the MIME type of a file.

        Args:
            file_id: The ID of the file.

        Returns:
            The MIME type of the file.
        """
        service = self._get_service()
        file = service.files().get(fileId=file_id, fields="mimeType").execute()
        return file.get('mime_type', 'image/jpeg')