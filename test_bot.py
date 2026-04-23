import importlib
import os
import sys


def test_bot_module_imports():
    """Bot module loads without errors."""
    if "bot" in sys.modules:
        del sys.modules["bot"]
    os.environ.setdefault("BOT_TOKEN", "fake_token_for_tests")
    bot = importlib.import_module("bot")
    assert callable(bot.main)


def test_env_token_missing(monkeypatch):
    """main() raises RuntimeError when BOT_TOKEN is not set."""
    import bot

    monkeypatch.delenv("BOT_TOKEN", raising=False)
    try:
        bot.main()
    except RuntimeError as exc:
        assert "BOT_TOKEN" in str(exc)
