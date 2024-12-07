from pdb.tests.sqlite3_manager_test import Sqlite3ManagerTester
from pdb.tests.import_export_test import ImportExportTester


def sqlite3_test() -> None:
    tester = Sqlite3ManagerTester()
    tester.test_create()
    tester.test_insert()
    results = tester.test_select()

    print(results)


def import_test() -> None:
    tester = ImportExportTester()
    tester.test_import()


if __name__ == "__main__":
    # sqlite3_test()
    import_test()
