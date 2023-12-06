"""StorageManagers for File Fortress

Todo:
    * Documentatioon
    * Implement S3Storage Manager
    * Change LocalStorageManager get_file(s) methods to return file streams
"""
from abc import ABC, abstractmethod
from typing import BinaryIO
from pathlib import Path
from datetime import datetime
from pymysql import IntegrityError


class StorageManager(ABC):
    """
    Handles storing, retrieving, and deletion of files and collections.

    Attributes:
        db (): a database session which connections can be created from
        _system_id (str): UUID of system user in database
    """

    def __init__(self, db):
        self.db = db
        with self.db.connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE name = "system"')
            self._system_id = cursor.fetchone()['id']
            cursor.close()

    @abstractmethod
    def allocate_url(self, uploader_id: str, filename: str) -> str:
        pass

    def lookup_link(self, short_link: str) -> str:
        """
        Resolves a short link into to the resource uri

        Args:
            short_link: the short_link to be queried

        Returns:
            the location where the storage manager can find the associated file

        Raises:
            FileNotFoundError: if short_link is not found in the database
        """
        with self.db.connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT url FROM files WHERE short_link=%s', short_link)
            result = cursor.fetchone()
            cursor.close()
        if result is None or 'url' not in result:
            raise FileNotFoundError(f"Cannot resolve short_link: {short_link}")
        return result['url']

    def create_link(self, short_link: str, uploader_id=None,
                    mime_type=None, expires: int = 0,
                    privacy: str = 'public', url: str = None) -> None:
        """
        Creates a short link pointing to a resource uri as an entry
        in the files table.

        Args:
            short_link: the link to be created"
            uploader_id: file uploader_id, must be UUID
            mime_type: mimetype of the uploaded file
            expires: utc epoch timestamp of when the file expires
            privacy: privacy settings for the uploaded file
            url: the location where the storage manager can find the resource

        Raises:
            FileExistsError: if the short_link is already in use
        """
        with self.db.connection() as conn:
            cursor = conn.cursor()
            try:
                insert_query = """INSERT INTO files (uploader_id, short_link, url, mime_type, expires, privacy)
                VALUES (%s, %s, %s, %s, %s, %s)"""
                expires = datetime.utcfromtimestamp(expires) if expires is not None else expires
                file_info = (uploader_id, short_link, url, mime_type, expires, privacy)
                conn.begin()
                cursor.execute(insert_query, file_info)
                conn.commit()
                cursor.close()
            except IntegrityError:
                cursor.close()
                conn.rollback()
                raise FileExistsError(f"short_link {short_link} is already in use!")

    @abstractmethod
    def cannonical_location(self, uri) -> str:
        pass

    @abstractmethod
    def push_file(self, file: bytes, uri) -> None:
        pass

    @abstractmethod
    def delete_file(self, uri) -> None:
        pass

    @abstractmethod
    def get_file(self, uri) -> bytes:
        pass

    @abstractmethod
    def get_files(self, uris) -> [bytes]:
        pass

    @abstractmethod
    def add_to_collection(self, file_uri, collection_uri):
        pass

    @abstractmethod
    def remove_from_collection(self, file_uri, collection_uri):
        pass

    @abstractmethod
    def get_collection(self, uri):
        pass


class LocalStorageManager(StorageManager):
    """
    A storage manger that handles local files

    Attributes:
        db (): a database session which connections can be created from
        _system_id (str): UUID of system user in database
    """

    def __init__(self, db, root_dir: str):
        super().__init__(db)
        self.root = Path(root_dir)

    def allocate_url(self, uploader_id: str, filename: str):
        file_path = self.root / uploader_id / filename
        i = 0
        while file_path.exists():
            i += 1
            file_path = self.root / uploader_id / f'{filename}_{i}'

        return str(file_path.relative_to(self.root))

    def cannonical_location(self, rel_path: str) -> str:
        """
        Creates an absolute path from a given relative path

        Args:
            rel_path: relative path from self.root
        """
        return self.root.joinpath(rel_path).as_posix()

    def push_file(self, file_stream: BinaryIO, rel_path: str) -> None:
        """
        Write from a file stream to disk at a path relative to storage root

        Args:
            file_stream: the file stream to read from
            rel_path: relative path to write to

        Raises:
            FileExistsError: if a file exists at self.root/rel_path
        """
        file_path = self.root.joinpath(rel_path)
        if file_path.exists():
            raise FileExistsError(f'Cannot create file, {rel_path} already exists')

        # Guarantee parent directories exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Read stream and write its contents to disk
        with file_path.open('wb') as f:
            f.write(file_stream.read())

    def delete_file(self, rel_path: str) -> None:
        """
        Delete a file from disk
        """
        file_path = self.root.joinpath(rel_path)
        file_path.unlink()

    def get_file(self, rel_path: str) -> bytes:
        """
        Read a file from disk
        """
        file_path = self.root.joinpath(rel_path)
        return file_path.read_bytes()

    def get_files(self, rel_paths: [str]) -> [bytes]:
        return [self.get_file(rel_path) for rel_path in rel_paths]

    def delete_files(self, rel_paths: [str]) -> None:
        for rel_path in rel_paths:
            self.delete_file(rel_path)

    def add_to_collection(self, file_uri, collection_uri):
        raise NotImplementedError

    def remove_from_collection(self, file_uri, collection_uri):
        raise NotImplementedError

    def get_collection(self, uri):
        raise NotImplementedError


class S3StorageManager(StorageManager):
    """
    A storage manager for remote storage via S3.

    Attributes:
        db (): a database session which connections can be created from
        _system_id (str): UUID of system user in database
    """

    def __init__(self, db, aws_credentials):
        super().__init__(db)
        raise NotImplementedError

    def cannonical_uri(self, uri) -> str:
        raise NotImplementedError

    def push_file(self, file: bytes, link):
        raise NotImplementedError

    def delete_file(self, link) -> None:
        raise NotImplementedError

    def get_file(self, link):
        raise NotImplementedError

    def add_to_collection(self, file_uri, collection_uri):
        raise NotImplementedError

    def remove_from_collection(self, file_uri, collection_uri):
        raise NotImplementedError

    def get_collection(self, uri):
        raise NotImplementedError
