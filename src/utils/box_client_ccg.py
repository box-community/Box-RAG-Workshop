"""
Handles the box client object creation
orchestrates the authentication process
"""

import os

import dotenv
from box_sdk_gen import (
    BoxCCGAuth,
    BoxClient,
    CCGConfig,
    FileWithInMemoryCacheTokenStorage,
    User,
)


class AppConfig:
    """application configurations"""

    dotenv.load_dotenv()

    def __init__(self) -> None:
        self.client_id = os.getenv("BOX_CLIENT_ID")
        self.client_secret = os.getenv("BOX_CLIENT_SECRET")
        self.enterprise_id = os.getenv("BOX_ENTERPRISE_ID")
        self.ccg_user_id = os.getenv("BOX_USER_ID")
        self.cache_file = os.getenv("BOX_CACHE_FILE", ".auth.ccg")

        self.box_root_demo_folder = os.getenv("BOX_ROOT_DEMO_FOLDER")

        self.local_folder_samples = "samples"
        self.local_folder_templates = f"{self.local_folder_samples}/Templates"
        self.local_folder_files = f"{self.local_folder_samples}/Files"

        self.local_file_csv = f"{self.local_folder_templates}/Leases.csv"
        self.local_file_template = f"{self.local_folder_templates}/Lease_Template.docx"

        self.box_folder_templates_name = "Templates"
        self.box_folder_leases_name = "Habitat Leases"

        self.open_ai_key = os.getenv("OPENAI_API_KEY")

    def __repr__(self) -> str:
        return f"ConfigCCG({self.__dict__})"

    __str__ = __repr__

    def to_dict(self) -> dict:
        return {
            k: v
            for k, v in self.__dict__.items()
            if k != "client_secret" and k != "cache_file"
        }


def __repr__(self) -> str:
    return f"ConfigCCG({self.__dict__})"


def get_ccg_enterprise_client(config: AppConfig) -> BoxClient:
    """Returns a box sdk Client object"""

    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        enterprise_id=config.enterprise_id,
        token_storage=FileWithInMemoryCacheTokenStorage(f"{config.cache_file}.ent"),
    )
    auth = BoxCCGAuth(ccg)
    # print(f"Auth Enterprise: {auth.token_storage}")
    client = BoxClient(auth)
    return client


def get_ccg_user_client(config: AppConfig, user_id: str) -> BoxClient:
    """Returns a box sdk Client object"""

    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        # enterprise_id=config.enterprise_id,
        user_id=config.ccg_user_id,
        token_storage=FileWithInMemoryCacheTokenStorage(f"{config.cache_file}.usr"),
    )
    auth = BoxCCGAuth(ccg)
    # print(f"Auth User: {auth.token_storage}")
    client = BoxClient(auth)
    return client


def whoami(client: BoxClient) -> User:
    user = client.users.get_user_me()
    return user
