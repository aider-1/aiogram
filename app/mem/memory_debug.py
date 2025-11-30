import asyncio
import logging
import os

import psutil

logger = logging.getLogger(__name__)
process = psutil.Process(os.getpid())


async def log_memory_loop(interval: int = 60) -> None:
    """
    Периодически логирует использование памяти процессом.
    interval — интервал в секундах.
    """
    while True:
        try:
            mem = process.memory_info()  # или memory_full_info() при желании
            # rss — то, что обычно показывает docker stats (resident set size)
            rss_mb = mem.rss / 1024 ** 2
            # vms можно не логировать, но иногда полезно
            vms_mb = mem.vms / 1024 ** 2

            try:
                import asyncio
                tasks_count = len(asyncio.all_tasks())
            except RuntimeError:
                tasks_count = -1  # если вызывается не из event loop

            logger.info(
                "Memory usage: rss=%.1f MB, vms=%.1f MB, tasks=%s",
                rss_mb,
                vms_mb,
                tasks_count,
            )
        except Exception as e:
            logger.exception("Error while logging memory usage: %s", e)

        await asyncio.sleep(interval)