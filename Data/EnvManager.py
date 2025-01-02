import os
from pathlib import Path
from dotenv import load_dotenv, set_key, find_dotenv
from typing import Optional


class EnvManager:
    def __init__(self, env_path: str = ".env"):
        """
        Initialize EnvManager with a path to the .env file.

        Args:
            env_path (str): Path to the .env file. Defaults to ".env" in current directory.
        """
        self.env_path = env_path
        self._ensure_env_file()
        load_dotenv(self.env_path)

    def _ensure_env_file(self) -> None:
        """Create .env file if it doesn't exist."""
        env_file = Path(self.env_path)
        if not env_file.exists():
            env_file.touch()

    def set_api_key(self, key: str, value: str) -> bool:
        """
        Set or update an API key in the .env file.

        Args:
            key (str): The name of the API key
            value (str): The value of the API key

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            set_key(self.env_path, key, value)
            os.environ[key] = value
            return True
        except Exception as e:
            print(f"Error setting API key: {e}")
            return False

    def get_api_key(self, key: str) -> Optional[str]:
        """
        Get an API key from the environment.

        Args:
            key (str): The name of the API key

        Returns:
            Optional[str]: The API key value if found, None otherwise
        """
        return os.getenv(key)

    def delete_api_key(self, key: str) -> bool:
        """
        Delete an API key from the .env file.

        Args:
            key (str): The name of the API key to delete

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            set_key(self.env_path, key, "")
            os.environ.pop(key, None)
            return True
        except Exception as e:
            print(f"Error deleting API key: {e}")
            return False

    def list_api_keys(self) -> dict:
        """
        List all API keys in the .env file.

        Returns:
            dict: Dictionary of key-value pairs from the .env file
        """
        keys = {}
        try:
            with open(self.env_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        keys[key.strip()] = value.strip()
        except Exception as e:
            print(f"Error listing API keys: {e}")
        return keys

    def validate_api_key(self, key: str) -> bool:
        """
        Check if an API key exists and is not empty.

        Args:
            key (str): The name of the API key to validate

        Returns:
            bool: True if key exists and has a value, False otherwise
        """
        value = self.get_api_key(key)
        return bool(value and value.strip())

    def backup_env(self, backup_path: str = ".env.backup") -> bool:
        """
        Create a backup of the .env file.

        Args:
            backup_path (str): Path for the backup file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import shutil
            shutil.copy2(self.env_path, backup_path)
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def restore_from_backup(self, backup_path: str = ".env.backup") -> bool:
        """
        Restore .env file from a backup.

        Args:
            backup_path (str): Path to the backup file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import shutil
            shutil.copy2(backup_path, self.env_path)
            load_dotenv(self.env_path)
            return True
        except Exception as e:
            print(f"Error restoring from backup: {e}")
            return False