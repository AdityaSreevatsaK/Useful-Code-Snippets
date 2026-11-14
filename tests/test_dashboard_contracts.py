import ast
from pathlib import Path


def test_dashboard_is_valid_python():
    ast.parse(Path("app.py").read_text(encoding="utf-8"))


def test_no_sensitive_server_features_enabled_by_default():
    app = Path("app.py").read_text(encoding="utf-8")
    assert 'os.environ.get("ENABLE_LOCAL_OPERATIONS") == "1"' in app
    assert 'disabled=not LOCAL_TOOLS_ENABLED' in app
    assert "validate_archive(zf)" in app
    assert 'confirm_delete = st.checkbox(' in app


def test_encryption_key_not_in_current_checkout():
    assert not Path("secret.key").exists()
