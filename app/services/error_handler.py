# app/services/error_handler.py

import logging
from typing import Dict, Any, Optional
import traceback
from datetime import datetime
import json
import os

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.errors_path = "logs/errors"
        os.makedirs(self.errors_path, exist_ok=True)

    def handle_error(
        self,
        error: Exception,
        context: Dict[str, Any],
        retry_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Handle errors with context and optional retry information
        """
        error_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        error_data = {
            'error_id': error_id,
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context,
            'retry_count': retry_count
        }

        # Log error
        self.logger.error(
            f"Error {error_id}: {error_data['error_type']} - {error_data['error_message']}"
        )

        # Save error details
        self._save_error(error_data)

        return error_data

    def _save_error(self, error_data: Dict[str, Any]):
        """
        Save error details to file
        """
        filename = f"error_{error_data['error_id']}.json"
        filepath = os.path.join(self.errors_path, filename)

        with open(filepath, 'w') as f:
            json.dump(error_data, f, indent=4)

# Created/Modified files:
# - logs/errors/error_{error_id}.json