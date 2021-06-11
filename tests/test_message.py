import pytest

from app.message import Message

TEST_USER = 'Adam'
MESSAGE_TEXT = "Hey sara 8:00 to 12:00 hyperlocal"

@pytest.fixture(scope="session")
def load_message():
    load_message = Message(text=MESSAGE_TEXT, user=TEST_USER)
    yield load_message

def test_parts_of_speech(load_message):
    parts_of_speech = load_message.nlp_pipe()
    intj, num, noun, adj = False, False, False, False
    for element in parts_of_speech:
        if 'INTJ' in str(element):
            intj = True
        if 'NOUN' in str(element):
            noun = True
        if 'NUM' in str(element):
            num = True
        if 'ADJ' in str(element):
            adj = True

    assert intj == True
    assert noun == True
    assert num == True
    assert adj == True

def test_to_records(load_message):
    records = load_message.to_records()
    assert records[0]['start_time'] == '8:00'
    assert records[0]['end_time'] == '12:00'
    assert records[0]['project_name'] == 'hyperlocal'
    assert records[0]['employee'] == 'sara'
    assert records[0]['user'] == 'Adam'
