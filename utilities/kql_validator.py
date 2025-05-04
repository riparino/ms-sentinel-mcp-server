"""
FILE: utilities/kql_validator.py
DESCRIPTION:
    Provides offline KQL validation using the Kusto.Language library via Python.NET.
"""

import os
from typing import List, Tuple
from utilities.logging import get_tool_logger
from utilities.path_utils import find_file, get_project_root

logger = get_tool_logger("kql_validator")

# Import pythonnet conditionally since it might not be available in all environments
try:
    # Only import what we need
    import pythonnet

    PYTHONNET_AVAILABLE = True
except ImportError:
    PYTHONNET_AVAILABLE = False
    logger.warning("pythonnet not found. Offline KQL validation will be unavailable.")


class KQLValidator:
    """Class for validating KQL syntax without connecting to Azure."""

    def __init__(self):
        """Initialize the KQL validator."""
        self.initialized = False
        self.dll_path = None
        self.kusto_language_loaded = False
        # Reference to KustoCode class, to be populated during initialization
        self.kusto_code = None

        # Try to initialize if pythonnet is available
        if PYTHONNET_AVAILABLE:
            self._initialize()

    def _initialize(self) -> bool:
        """
        Initialize the Kusto.Language assembly with minimal dependencies.

        Returns:
            bool: True if initialization succeeded, False otherwise.
        """
        if self.initialized:
            return True

        # Use the path_utils to find the DLL in various locations
        dll_filename = "Kusto.Language.dll"
        search_dirs = ["lib", os.path.join("utilities", "lib"), ".", get_project_root()]

        self.dll_path = find_file(dll_filename, search_dirs)

        if not self.dll_path:
            logger.warning(
                "Kusto.Language.dll not found. Offline validation will be unavailable."
            )
            return False

        logger.info("Found Kusto.Language.dll at: %s", self.dll_path)

        try:
            # Initialize Pythonnet runtime
            logger.info("Initializing Pythonnet runtime")
            pythonnet.load()
            logger.info("Pythonnet runtime initialized")

            # Use System.Reflection to load the assembly
            logger.info("Loading assembly from: %s", self.dll_path)
            try:
                from System import Reflection  # type: ignore  # pylint: disable=import-outside-toplevel  # noqa: E402
            except ImportError as e:
                logger.error("Unable to import System.Reflection: %s", e, exc_info=True)
                return False

            Reflection.Assembly.LoadFrom(self.dll_path)
            logger.info("Assembly loaded via System.Reflection")

            # Import only the essential KustoCode class for validation
            # This is more resilient to changes in the DLL structure
            try:
                from Kusto.Language import KustoCode  # type: ignore  # pylint: disable=import-outside-toplevel  # noqa: E402

                # Store reference to class for later use
                self.kusto_code = KustoCode

                # Test if we can parse a query
                test_query = "Heartbeat | take 10"
                test_code = KustoCode.Parse(test_query)
                diagnostics = list(test_code.GetDiagnostics())
                logger.info(
                    "KQL test parse successful with %d diagnostics", len(diagnostics)
                )

                self.kusto_language_loaded = True
                self.initialized = True
                logger.info("Successfully initialized Kusto.Language library")
                return True
            except ImportError as e:
                logger.error(
                    "Error importing Kusto.Language.KustoCode: %s", e, exc_info=True
                )
                return False
        except Exception as e:
            logger.error("Error initializing Kusto.Language: %s", e, exc_info=True)
            return False

    def validate_query(self, query_text: str) -> Tuple[bool, List[str]]:
        """
        Validate a KQL query syntax without connecting to Azure.

        Args:
            query_text: The KQL query text to validate.

        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_error_messages)
        """
        if not PYTHONNET_AVAILABLE:
            return False, ["Python.NET not available. Unable to validate KQL."]

        if not self.initialized and not self._initialize():
            return False, ["KQL validator not initialized. Cannot validate query."]

        try:
            # Parse the query using KustoCode.Parse
            code = self.kusto_code.Parse(query_text)  # type: ignore

            # Get diagnostics (syntax errors)
            diagnostics = list(code.GetDiagnostics())

            if diagnostics:
                # Convert diagnostics to readable error messages
                error_messages = []
                for diag in diagnostics:
                    # Extract line and position if available
                    try:
                        line_pos = (
                            f"Line {diag.Start.Line}, Position {diag.Start.Column}"
                        )
                    except Exception:
                        line_pos = "Unknown position"

                    # Extract message if available
                    try:
                        message = diag.Message
                    except Exception:
                        message = str(diag)

                    error_messages.append(f"{line_pos}: {message}")
                return False, error_messages

            return True, []
        except Exception as e:
            return False, [f"Error validating query: {str(e)}"]


# Singleton instance of the validator
_VALIDATOR = None


def get_validator() -> KQLValidator:
    """
    Get the KQLValidator singleton instance.

    Returns:
        KQLValidator: The validator instance.
    """
    global _VALIDATOR  # pylint: disable=global-statement
    if _VALIDATOR is None:
        _VALIDATOR = KQLValidator()
    return _VALIDATOR


def validate_kql(query: str) -> Tuple[bool, List[str]]:
    """
    Validate a KQL query.

    Args:
        query: The KQL query to validate.

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_error_messages)
    """
    validator = get_validator()
    if not validator.initialized:
        return False, [
            "KQL validation unavailable: Could not initialize validator.",
            "For syntax validation, please use the query tool to validate against your workspace.",
        ]
    return validator.validate_query(query)
