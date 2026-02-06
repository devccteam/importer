from datetime import UTC, datetime, timedelta
from typing import Final

from converter.tasks.config import celery
from converter.uteis import config_logger
from converter.uteis.rest import rest_done

logger = config_logger.setup('app.tasks')

DAYS = 3


@celery.task(name='clear_db')
def clear_db() -> None:
    past_day = get_correct_day()
    rest_done(f'created_at=lte.{past_day}')


def get_correct_day() -> str:
    now: Final[datetime] = datetime.now(UTC)
    past_date: Final[datetime] = now - timedelta(days=DAYS)

    return past_date.strftime('%Y/%m/%d')
