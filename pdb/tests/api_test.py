import json
from pdb.database.common import SupportedDb
from pdb.database.datatypes.datatypes import PdbDatatype
from pdb.database.models.pdb_column import PdbColumn
from time import time
from typing import Any

import requests


class ApiTester:
    _API_URL = "http://127.0.0.1:8000"

    def __init__(self) -> None:
        self._dbtype = SupportedDb.SQLITE3
        self._test_tablename: str = "customers"
        self._test_table_rename: str = "accounts"
        self._test_cols: list[PdbColumn] = [
            PdbColumn("name", PdbDatatype.TEXT),
            PdbColumn("account_opening_date", PdbDatatype.DATE),
            PdbColumn("company", PdbDatatype.TEXT),
            PdbColumn("industry", PdbDatatype.TEXT, is_dropdown=True),
            PdbColumn("total_orders", PdbDatatype.NUMBER),
            PdbColumn("is_settled", PdbDatatype.BOOL),
        ]
        self._test_col_rename: str = "account"
        self._test_col_add: PdbColumn = PdbColumn("is_active", PdbDatatype.BOOL)

        self._industry_drops: list[tuple[str, str, Any]] = [
            (self._test_tablename, "industry", "tech"),
            (self._test_tablename, "industry", "finance"),
            (self._test_tablename, "industry", "manufacturing"),
            (self._test_tablename, "industry", "hospitality"),
        ]

        self._test_users: list[tuple[str, str, str]] = [("Zewzki", "test-password", "Admin"), ("newguy", "another-pass", "User")]

        self._test_permissions: list[tuple[str, str, Any]] = [
            (self._test_tablename, "Zewzki", True, True),
            (self._test_tablename, "newguy", True, False),
        ]

        self._test_records: list[tuple[str, str, str, str, int, bool]] = [
            ("John Johnson", "12/15/1936", "WeMakeTires", "manufacturing", 23, True),
            ("Guy Fieri", "6/30/2006", "Diners, Drive-Ins, and Dives", "hospitality", 498, True),
            ("Scammy McScammerson", "4/1/2000", "ScamCentral", "finance", 1983, False),
            ("God Christ", "1/1/0001", "Heaven", "Hospitality", 1, True),
        ]

    def _get(self, endpoint: str, params: dict[str, str] | None = None) -> tuple[int, str, Any, float]:
        t0 = time()
        response = requests.get(
            url=f"{self._API_URL}/{endpoint}",
            params=params,
        )
        t1 = time()
        return (response.status_code, response.reason, response.json(), t1 - t0)

    def _post(self, endpoint: str, params: dict[str, str] | None = None, data: str | None = None) -> tuple[int, str, str, float]:
        t0 = time()
        response = requests.post(
            url=f"{self._API_URL}/{endpoint}",
            params=params,
            data=data,
        )
        t1 = time()
        return (response.status_code, response.reason, response.content, t1 - t0)

    def _put(self, endpoint: str, params: dict[str, str] | None = None, data: str | None = None) -> tuple[int, str, str, float]:
        t0 = time()
        response = requests.put(
            url=f"{self._API_URL}/{endpoint}",
            params=params,
            data=data,
        )
        t1 = time()
        return (response.status_code, response.reason, response.content, t1 - t0)

    def _delete(self, endpoint: str, params: dict[str, str] | None = None) -> tuple[int, str, str, float]:
        t0 = time()
        response = requests.delete(
            url=f"{self._API_URL}/{endpoint}",
            params=params,
        )
        t1 = time()
        return (response.status_code, response.reason, response.content, t1 - t0)

    def _print_api_response(self, response_tuple: tuple[int, str, str, float]) -> None:
        s, r, c, t = response_tuple[0], response_tuple[1], response_tuple[2], response_tuple[3]
        print(f"{s} - {r} ({round(t, 4)} seconds), {c}")

    def test_create(self) -> None:
        response_tuple = self._post("add-table", {"tablename": self._test_tablename}, json.dumps([self._pdb_column_to_dict(c) for c in self._test_cols]))
        self._print_api_response(response_tuple)

    def test_drops(self) -> None:
        for drop in self._industry_drops:
            drop_data = {
                "tablename": drop[0],
                "column_name": drop[1],
                "value": drop[2],
            }
            response_tuple = self._post("add-dropdown", drop_data)
            self._print_api_response(response_tuple)

    def test_perms(self) -> None:
        for perm in self._test_permissions:
            perm_data = {
                "tablename": perm[0],
                "username": perm[1],
                "can_read": perm[2],
                "can_write": perm[3],
            }
            response_tuple = self._post("add-permission", perm_data)
            self._print_api_response(response_tuple)

    def test_insert(self) -> None:
        for record in self._test_records:
            insert_data = {
                "name": record[0],
                "account_opening_date": record[1],
                "company": record[2],
                "industry": record[3],
                "total_orders": record[4],
                "is_settled": record[5],
            }
            response_tuple = self._post(f"{self._test_tablename}/insert", data=json.dumps(insert_data))
            self._print_api_response(response_tuple)

    def test_users(self) -> None:
        for user in self._test_users:
            user_data = {
                "username": user[0],
                "password": user[1],
                "role": user[2],
            }
            response_tuple = self._post("add-user", user_data)
            self._print_api_response(response_tuple)

    def test_auth(self) -> None:
        auth_data = {"username": "Zewzki", "password": "test-password"}
        response_tuple = self._post("auth", auth_data)
        self._print_api_response(response_tuple)

    def test_query(self, tablename: str) -> None:
        response_tuple = self._get(f"{tablename}/query")
        self._print_api_response(response_tuple)

    def test_table_rename(self) -> None:
        params = {
            "old_tablename": self._test_tablename,
            "new_tablename": self._test_table_rename,
        }
        response_tuple = self._put("rename-table", params)
        self._print_api_response(response_tuple)

    def test_column_rename(self) -> None:
        params = {
            "tablename": self._test_table_rename,
            "old_column_name": "name",
            "new_column_name": self._test_col_rename,
        }
        response_tuple = self._put("rename-column", params)
        self._print_api_response(response_tuple)

    def test_column_add(self) -> None:
        params = {"tablename": self._test_table_rename}
        data = json.dumps(self._pdb_column_to_dict(self._test_col_add))
        response_tuple = self._post("add-column", params, data)
        self._print_api_response(response_tuple)

    def test_column_drop(self) -> None:
        params = {
            "tablename": "accounts",
            "column_name": "is_active",
        }
        response_tuple = self._delete("remove-column", params)
        self._print_api_response(response_tuple)

    def test_table_drop(self) -> None:
        params = {"tablename": self._test_table_rename}
        response_tuple = self._delete("remove-table", params)
        self._print_api_response(response_tuple)

    def _pdb_column_to_dict(self, column: PdbColumn) -> dict[str, Any]:
        return {
            "col_name": column.col_name,
            "dtype": column.dtype.value,
            "is_dropdown": column.is_dropdown,
            "is_unique": column.is_unique,
        }
