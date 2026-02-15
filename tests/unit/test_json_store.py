import json
from pathlib import Path

import pytest
from app.infra.json_store import DataStoreError, JsonStore


def test_load_list_reads_json_array_of_objects(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    path.write_text(json.dumps([{"a": 1}, {"b": 2}]), encoding="utf-8")

    store = JsonStore()
    items = store.load_list(path)

    assert items == [{"a": 1}, {"b": 2}]


def test_load_list_raises_when_file_missing(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"

    store = JsonStore()

    with pytest.raises(DataStoreError) as exc:
        store.load_list(missing)

    assert "not found" in str(exc.value).lower()


def test_load_list_raises_on_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{not valid json]", encoding="utf-8")

    store = JsonStore()

    with pytest.raises(DataStoreError) as exc:
        store.load_list(path)

    assert "invalid json" in str(exc.value).lower()


def test_load_list_raises_when_root_is_not_list(tmp_path: Path) -> None:
    path = tmp_path / "root.json"
    path.write_text(json.dumps({"a": 1}), encoding="utf-8")

    store = JsonStore()

    with pytest.raises(DataStoreError) as exc:
        store.load_list(path)

    assert "expected a json array" in str(exc.value).lower()


def test_load_list_raises_when_any_item_is_not_object(tmp_path: Path) -> None:
    path = tmp_path / "items.json"
    path.write_text(json.dumps([{"a": 1}, 123]), encoding="utf-8")

    store = JsonStore()

    with pytest.raises(DataStoreError) as exc:
        store.load_list(path)

    assert "index 1" in str(exc.value).lower()
