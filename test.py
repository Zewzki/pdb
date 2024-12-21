from pdb.tests.api_test import ApiTester
from pdb.tests.import_export_test import ImportExportTester
from pdb.tests.sqlite3_manager_test import Sqlite3ManagerTester


def sqlite3_test() -> None:
    tester = Sqlite3ManagerTester()
    # tester.test_create()
    # tester.test_insert()
    # results = tester.test_select()

    # print(results)


def import_test() -> None:
    tester = ImportExportTester()
    tester.test_import()


def api_test() -> None:
    tester = ApiTester()
    tester.test_users()
    tester.test_create()
    tester.test_drops()
    tester.test_insert()
    tester.test_perms()
    tester.test_auth()
    tester.test_query("customers")
    tester.test_table_rename()
    tester.test_column_rename()
    tester.test_column_add()
    tester.test_query("accounts")
    tester.test_column_drop()
    tester.test_table_drop()


if __name__ == "__main__":
    # sqlite3_test()
    # import_test()
    api_test()
