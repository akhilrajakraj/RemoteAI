from app.memory import MemoryStore

def test_message_round_trip(tmp_path):
    store = MemoryStore(tmp_path / "test.db")
    store.add_message("conversation-1", "user", "Hello")
    messages = store.get_messages("conversation-1")
    assert len(messages) == 1
    assert messages[0]["content"] == "Hello"

def test_fact_and_task_creation(tmp_path):
    store = MemoryStore(tmp_path / "test.db")
    assert store.add_fact("User likes concise summaries") > 0
    assert store.add_task("Review project") > 0
    assert store.list_facts()[0]["fact"] == "User likes concise summaries"
    assert store.list_tasks()[0]["title"] == "Review project"
