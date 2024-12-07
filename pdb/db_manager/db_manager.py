from abc import ABC, abstractmethod
from pdb.shared.op_status import OpStatus
from typing import Any


class DbManager(ABC):
    # Tables
    @abstractmethod
    def create_pdb_table(self, tablename: str, columns: list[tuple[str, type]]) -> OpStatus:
        pass

    @abstractmethod
    def get_pdb_tables(self) -> list[str]:
        pass

    @abstractmethod
    def remove_pdb_table(self, tablename: str) -> OpStatus:
        pass

    # Table Columns
    @abstractmethod
    def add_table_column(self, tablename: str, column_name: str, type: type) -> OpStatus:
        pass

    @abstractmethod
    def modify_table_column(self, tablename: str, column_name: str, new_type: type) -> OpStatus:
        pass

    @abstractmethod
    def remove_table_column(self, tablename: str, column_name: str) -> OpStatus:
        pass

    # Dropdowns
    @abstractmethod
    def add_dropdown_value(self, tablename: str, column_name: str, value: Any) -> OpStatus:
        pass

    @abstractmethod
    def remove_dropdown_value(self, tablename: str, column_name: str, value: Any) -> OpStatus:
        pass

    # Users
    @abstractmethod
    def add_user(self, username: str, password: str, role: str, algorithm: str) -> OpStatus:
        pass

    @abstractmethod
    def remove_user(self, username: str) -> OpStatus:
        pass

    # Perms
    @abstractmethod
    def add_user_permissions(self, tablename: str, username: str, can_read: bool, can_write: bool) -> OpStatus:
        pass

    # Table Data
    @abstractmethod
    def get_table(self, tablename: str) -> list[list[Any]]:
        pass

    @abstractmethod
    def add_record(self, tablename: str, record_data: dict[str, Any]) -> OpStatus:
        pass

    @abstractmethod
    def update_record(self, tablename: str, row_id: int, new_data: dict[str, Any]) -> OpStatus:
        pass

    @abstractmethod
    def remove_record(self, tablename: str, row_id: int) -> OpStatus:
        pass
