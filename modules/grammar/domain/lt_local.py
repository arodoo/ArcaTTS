import subprocess
import json
import os
from typing import List
from modules.grammar.domain.models import (
    GrammarError,
    ErrorType,
    Severity
)


class LanguageToolLocal:
    """Direct LanguageTool JAR wrapper."""
    
    def __init__(self, language: str = "es"):
        self.language = language
        self.jar_path = self._get_jar_path()
    
    def _get_jar_path(self) -> str:
        """Get cached LanguageTool JAR."""
        cache = os.path.expanduser(
            "~/.cache/language_tool_python/"
            "LanguageTool-6.8-SNAPSHOT/"
            "languagetool-commandline.jar"
        )
        
        if not os.path.exists(cache):
            raise FileNotFoundError(
                f"LanguageTool not cached at {cache}. "
                "Run once with internet to download."
            )
        
        return cache
    
    def check(self, text: str) -> List[dict]:
        """Check text using JAR directly."""
        # Write text to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            suffix='.txt',
            delete=False
        ) as f:
            f.write(text)
            temp_file = f.name
        
        try:
            # Run LanguageTool JAR with more memory
            result = subprocess.run(
                [
                    'java',
                    '-Xmx2G',
                    '-Dfile.encoding=UTF-8',
                    '-jar',
                    self.jar_path,
                    '-l',
                    self.language,
                    '--json',
                    temp_file
                ],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=600
            )
            
            # Parse JSON output
            if result.returncode == 0:
                if result.stdout:
                    data = json.loads(result.stdout)
                    return data.get('matches', [])
                return []
            else:
                raise Exception(
                    f"LanguageTool error: {result.stderr}"
                )
        
        finally:
            os.unlink(temp_file)

