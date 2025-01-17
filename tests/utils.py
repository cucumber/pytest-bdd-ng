from __future__ import annotations

from operator import ge
from typing import TYPE_CHECKING

from pytest_bdd.packaging import compare_distribution_version

if TYPE_CHECKING:  # pragma: no cover
    from pytest_bdd.typing.pytest import RunResult

PYTEST_6 = compare_distribution_version("pytest", "6", ge)


if PYTEST_6:

    def assert_outcomes(
        result: RunResult,
        passed: int = 0,
        skipped: int = 0,
        failed: int = 0,
        errors: int = 0,
        xpassed: int = 0,
        xfailed: int = 0,
    ) -> None:
        """Compatibility function for result.assert_outcomes"""
        result.assert_outcomes(
            errors=errors, passed=passed, skipped=skipped, failed=failed, xpassed=xpassed, xfailed=xfailed
        )

else:

    def assert_outcomes(
        result: RunResult,
        passed: int = 0,
        skipped: int = 0,
        failed: int = 0,
        errors: int = 0,
        xpassed: int = 0,
        xfailed: int = 0,
    ) -> None:
        """Compatibility function for result.assert_outcomes"""
        result.assert_outcomes(
            error=errors,  # Pytest < 6 uses the singular form
            passed=passed,
            skipped=skipped,
            failed=failed,
            xpassed=xpassed,
            xfailed=xfailed,
        )
