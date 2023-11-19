from abc import ABC, abstractmethod
from pathlib import Path


class StorageManager(ABC):
    """
    Handles storing, retrieving, and deletion of files and collections.
    """

    def __init__(self, db_conn):
        self.db = db_conn

    def lookup_link(self, short_link: str) -> str:
        """
        Resolves a short link into to the resource uri
        """
        with self.db.cursor() as cursor:
            cursor.execute('SELECT url FROM files WHERE short_link=%s', short_link)
            result = cursor.fetchone()
        if result is None or 'url' not in result:
            raise FileNotFoundError(f"Cannot resolve short_link: {short_link}")
        return result['url']

    def create_link(self, short_link: str, details):
        """
        Creates a short link pointing to a resource uri
        """
        with self.db.cursor() as cursor:
            raise NotImplementedError

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
    """

    def __init__(self, db_conn, root_dir: str):
        super().__init__(db_conn)
        self.root = Path(root_dir)

    def cannonical_location(self, rel_path: str) -> str:
        return self.root.joinpath(rel_path).as_posix()

    def push_file(self, file: bytes, rel_path: str) -> None:
        """
        Write bytes to disk at rel_path
        """
        file_path = self.root.joinpath(rel_path)
        if file_path.exists():
            raise FileExistsError(f'Cannot create file, {rel_path} already exists')
        file_path.write_bytes(file)

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
        # FIXME: loading multiple files into memory is expensive and dangerous
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
    """

    def __init__(self, db_conn, aws_credentials):
        super().__init__(db_conn)
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
