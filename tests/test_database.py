import pytest

from app.database import Database

TEST_DB = 'sqlite:///test.db'
TEST_TIMELOG = [{'timelog_name': 'timelog_1',
                 'start_time': '8:00',
                 'end_time': '12:00',
                 'project_name': 'hyperlocal',
                 'employee': 'sara',
                 'user': 'Adam'}]

@pytest.fixture(scope="session")
def create_database():
    create_database = Database(timelogs=TEST_TIMELOG, database_name=TEST_DB)
    yield create_database


def test_database(create_database):
    sql_create = create_database.insert_bulk()
    assert sql_create == True


def test_sql_select(create_database):
    sql_select = create_database.select_query()
    timelog_name, start_time, end_time, project_name, employee = False, False, False, False, False
    for element in sql_select:
        if 'timelog_1' in str(element):
            timelog_name = True
        if '8:00' in str(element):
            start_time = True
        if '12:00' in str(element):
            end_time = True
        if 'hyperlocal' in str(element):
            project_name = True
        if 'sara' in str(element):
            employee = True

    assert timelog_name == True
    assert start_time == True
    assert end_time == True
    assert project_name == True
    assert employee == True
