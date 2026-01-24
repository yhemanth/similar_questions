import base64

from image_to_questions import (
    convert_scanned_text_to_questions,
    initialize_openai_client,
    scan_questions_page,
)


def test_initialize_openai_client_calls_openai_and_loads_env(monkeypatch):
    calls = {"dotenv": 0, "openai": 0}

    def fake_load_dotenv():
        calls["dotenv"] += 1

    class DummyOpenAI:
        def __init__(self):
            calls["openai"] += 1

    monkeypatch.setattr("image_to_questions.load_dotenv", fake_load_dotenv)
    monkeypatch.setattr("image_to_questions.OpenAI", DummyOpenAI)

    client = initialize_openai_client()

    assert isinstance(client, DummyOpenAI)
    assert calls["dotenv"] == 1
    assert calls["openai"] == 1


def test_scan_questions_page_reads_image_and_calls_chat(monkeypatch, tmp_path):
    img_bytes = b"\x89PNG\r\n\x1a\nfake-image"
    img_path = tmp_path / "page.png"
    img_path.write_bytes(img_bytes)

    calls = {}

    class DummyResponse:
        def __init__(self):
            message = type("DummyMessage", (), {"content": "OK"})()
            choice = type("DummyChoice", (), {"message": message})()
            self.choices = [choice]

    class DummyCompletions:
        def create(self, **kwargs):
            calls["kwargs"] = kwargs
            return DummyResponse()

    class DummyChat:
        completions = DummyCompletions()

    class DummyClient:
        chat = DummyChat()

    result = scan_questions_page(DummyClient(), str(img_path), model_name="test-model")

    assert result == "OK"
    assert calls["kwargs"]["model"] == "test-model"
    messages = calls["kwargs"]["messages"]
    assert messages[0]["role"] == "system"
    assert "Extract the math questions" in messages[0]["content"]
    assert messages[1]["role"] == "user"
    assert messages[1]["content"][0]["type"] == "text"

    expected_b64 = base64.b64encode(img_bytes).decode("utf-8")
    image_url = messages[1]["content"][1]["image_url"]["url"]
    assert image_url == f"data:image/png;base64,{expected_b64}"


def test_convert_scanned_text_to_questions_writes_one_line_per_block(tmp_path):
    scanned_text = (
        "<start>1. First line\nSecond line<end>\n"
        "<start>2. Single line<end>"
    )
    output_file = tmp_path / "out.md"

    convert_scanned_text_to_questions(scanned_text, str(output_file))

    assert output_file.read_text().splitlines() == [
        "1. First line Second line",
        "2. Single line",
    ]
