import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from modules.grammar.domain.models import (
    GrammarError,
    CorrectionResult
)


class SummaryGenerator:
    """Generates detailed correction summaries."""
    
    @staticmethod
    def generate_summary(
        result: CorrectionResult,
        version: str
    ) -> Dict[str, Any]:
        """Generate comprehensive summary."""
        return {
            "metadata": {
                "version": version,
                "timestamp": datetime.now().isoformat(),
                "original_file": result.original_file,
                "corrected_file": result.corrected_file
            },
            "statistics": {
                "total_errors": result.total_errors,
                "fixed_errors": result.fixed_errors,
                "unfixed_errors": (
                    result.total_errors - result.fixed_errors
                ),
                "fix_rate": round(
                    (result.fixed_errors / result.total_errors 
                     * 100) if result.total_errors > 0 else 0,
                    2
                )
            },
            "errors_by_type": (
                SummaryGenerator._group_by_type(
                    result.errors
                )
            ),
            "errors_by_severity": (
                SummaryGenerator._group_by_severity(
                    result.errors
                )
            ),
            "detailed_fixes": [
                error.to_dict() 
                for error in result.errors 
                if error.suggested_replacement
            ],
            "unfixed_errors": [
                error.to_dict() 
                for error in result.errors 
                if not error.suggested_replacement
            ]
        }
    
    @staticmethod
    def _group_by_type(
        errors: List[GrammarError]
    ) -> Dict[str, int]:
        """Group errors by type."""
        counts = {}
        for error in errors:
            type_name = error.error_type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts
    
    @staticmethod
    def _group_by_severity(
        errors: List[GrammarError]
    ) -> Dict[str, int]:
        """Group errors by severity."""
        counts = {}
        for error in errors:
            severity = error.severity.value
            counts[severity] = counts.get(severity, 0) + 1
        return counts
    
    @staticmethod
    def save_summary(
        summary: Dict[str, Any],
        output_path: Path
    ) -> None:
        """Save summary to JSON file."""
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(
                summary,
                f,
                indent=2,
                ensure_ascii=False
            )
