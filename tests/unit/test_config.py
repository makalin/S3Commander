import os
import json
import tempfile
from src.utils.config import ConfigManager

def test_config_load_and_save():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, 'config.json')
        config = ConfigManager(config_path)
        config.set('theme', 'amber')
        config2 = ConfigManager(config_path)
        config2.load_config()
        assert config2.get('theme') == 'amber' 