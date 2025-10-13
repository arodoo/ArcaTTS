import language_tool_python
from typing import List, Optional
from pathlib import Path
from modules.grammar.domain.models import (
    GrammarError,
    CorrectionResult
)
from modules.grammar.domain.checker import GrammarChecker
from modules.grammar.domain.versioning import (
    VersionManager
)
from modules.grammar.domain.summary import (
    SummaryGenerator
)


class TextCorrector:
    """Corrects grammar errors in text files."""
    
    def __init__(self, language: str = "es"):
        self.language = language
        self.checker = GrammarChecker(language)
        self.version_manager = VersionManager()
        self.summary_generator = SummaryGenerator()
    
    def correct_file(
        self, 
        input_path: str,
        output_dir: str,
        auto_fix: bool = True,
        version: Optional[str] = None
    ) -> CorrectionResult:
        """
        Correct grammar in file with versioning.
        Preserves original, creates versioned output.
        """
        try:
            # Generate version if not provided
            if version is None:
                version = self.version_manager.generate_version()
            
            # Create versioned filenames
            input_file = Path(input_path)
            output_path = Path(output_dir)
            
            versioned_file = (
                self.version_manager.create_versioned_filename(
                    input_file.name,
                    version
                )
            )
            summary_file = (
                self.version_manager.create_summary_filename(
                    input_file.name,
                    version
                )
            )
            
            corrected_path = output_path / versioned_file
            summary_path = output_path / summary_file
            
            # Read original file
            with open(input_path, 'r', encoding='utf-8') as f:
                original_text = f.read()
            
            # Check for errors
            errors = self.checker.check_text(original_text)
            
            # Apply corrections if auto_fix enabled
            corrected_text = original_text
            fixed_count = 0
            
            if auto_fix:
                corrected_text, fixed_count = (
                    self._apply_corrections(
                        original_text,
                        errors
                    )
                )
            
            # Write corrected file
            corrected_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )
            
            with open(corrected_path, 'w', encoding='utf-8') as f:
                f.write(corrected_text)
            
            # Create result
            result = CorrectionResult(
                original_file=input_path,
                corrected_file=str(corrected_path),
                total_errors=len(errors),
                fixed_errors=fixed_count,
                errors=errors,
                success=True
            )
            
            # Generate and save summary
            summary = self.summary_generator.generate_summary(
                result,
                version
            )
            self.summary_generator.save_summary(
                summary,
                summary_path
            )
            
            return result
        
        except Exception as e:
            return CorrectionResult(
                original_file=input_path,
                corrected_file="",
                total_errors=0,
                fixed_errors=0,
                errors=[],
                success=False,
                error_message=str(e)
            )
    
    def _apply_corrections(
        self,
        text: str,
        errors: List[GrammarError]
    ) -> tuple[str, int]:
        """Apply suggested corrections to text."""
        # Sort errors by offset (reverse) to maintain
        # positions
        sorted_errors = sorted(
            errors,
            key=lambda e: e.offset,
            reverse=True
        )
        
        corrected = text
        fixed_count = 0
        
        for error in sorted_errors:
            if error.suggested_replacement:
                start = error.offset
                end = start + error.length
                
                corrected = (
                    corrected[:start] +
                    error.suggested_replacement +
                    corrected[end:]
                )
                fixed_count += 1
        
        return corrected, fixed_count
    
    def close(self) -> None:
        """Close resources."""
        self.checker.close()
