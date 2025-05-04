"""
FILE: utilities/task_manager.py
DESCRIPTION:
    Provides utilities for managing asynchronous tasks across the application.
"""

import asyncio
import sys
import logging
from typing import Set, Callable, TypeVar, Any, Optional, Coroutine

# Configure logging to stderr
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Define type variables for better type hints
T = TypeVar("T")
R = TypeVar("R")

# Global set to track all active tasks
active_tasks: Set[asyncio.Task] = set()


def create_tracked_task(
    coro: Coroutine[Any, Any, T],
    timeout: Optional[float] = 60.0,
    name: Optional[str] = None,
) -> asyncio.Task[T]:
    """
    Create and track an asyncio task with timeout.

    Args:
        coro: The coroutine to run as a task
        timeout: Optional timeout in seconds (default: 60s)
        name: Optional name for the task for better debugging

    Returns:
        The created task object
    """
    # Apply timeout if specified
    if timeout:
        coro = asyncio.wait_for(coro, timeout)

    # Create a named task
    task = asyncio.create_task(coro, name=name)

    # Register the task for tracking
    active_tasks.add(task)
    task.add_done_callback(active_tasks.discard)

    return task


async def run_in_thread(
    func: Callable[..., R],
    *args: Any,
    timeout: Optional[float] = 60.0,
    name: Optional[str] = None,
    **kwargs: Any,
) -> R:
    """
    Run a blocking function in a thread pool with task tracking.

    Args:
        func: The blocking function to run
        *args: Positional arguments to pass to the function
        timeout: Optional timeout in seconds (default: 60s)
        name: Optional name for the task for better debugging
        **kwargs: Keyword arguments to pass to the function

    Returns:
        The result of the function call

    Raises:
        asyncio.TimeoutError: If the operation times out
        Exception: Any exception raised by the function
    """

    async def thread_task():
        try:
            return await asyncio.to_thread(func, *args, **kwargs)
        except asyncio.CancelledError:
            logger.warning("Thread operation '%s' was cancelled", name)
            raise
        except Exception as e:
            logger.error("Error in thread operation '%s': %s", name, str(e))
            raise

    task = create_tracked_task(thread_task(), timeout=timeout, name=name)
    return await task


async def cleanup_tasks():
    """
    Cancel all active tasks and wait for them to complete.
    Should be called during application shutdown.
    """
    if not active_tasks:
        return

    logger.info("Cancelling %d active tasks", len(active_tasks))

    # Create a copy of the set to avoid modification during iteration
    tasks_to_cancel = active_tasks.copy()

    # Cancel all tasks
    for task in tasks_to_cancel:
        if not task.done() and not task.cancelled():
            task.cancel()

    # Wait for all tasks to complete with cancellation
    if tasks_to_cancel:
        await asyncio.gather(*tasks_to_cancel, return_exceptions=True)

    logger.info("All tasks cancelled successfully")
