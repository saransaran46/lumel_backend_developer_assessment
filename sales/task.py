from celery import shared_task
from django.utils import timezone
import logging
from .utils import load_sales_data_from_csv
import os

logger = logging.getLogger(__name__)


@shared_task
def scheduled_data_refresh():
    try:
        csv_file_path = os.path.join(os.path.dirname(__file__), 'data/sales_data.csv')
        if os.path.exists(csv_file_path):
            success, message = load_sales_data_from_csv(csv_file_path, overwrite=False)
            if success:
                logger.info(f"Scheduled data refresh successful: {message}")
                return {"status": "success", "message": message}
            else:
                logger.error(f"Scheduled data refresh failed: {message}")
                return {"status": "error", "message": message}
        else:
            error_msg = "CSV file not found for scheduled refresh"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
    except Exception as e:
        logger.error(f"Error in scheduled data refresh: {str(e)}")
        return {"status": "error", "message": str(e)}