import importlib
import sys
from pathlib import Path


def test_disable_feed(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "feeds_gaming.yaml").write_text(
        "- name: IGN\n  url: https://feeds.ign.com/ign/all\n  enabled: false\n",
        encoding="utf-8",
    )
    (config_dir / "tags.yaml").write_text("[]", encoding="utf-8")
    (config_dir / "breaking.yaml").write_text("[]", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    sys.modules.pop("intl_news.config", None)
    cfg = importlib.import_module("intl_news.config")
    assert "IGN" not in cfg.FEEDS
