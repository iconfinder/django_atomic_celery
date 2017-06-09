from celery.task import task as base_task, Task
from django.db import transaction
from functools import partial


class PostTransactionTask(Task):
    """Task delayed until after the outermost atomic block is exited.

    If the atomic transaction block within which the task is scheduled is
    successful, ie. no exception is raised and the transaction is not rolled
    back, the task is promoted to the outside block. Otherwise, the task is
    discarded.

    When exiting the outside block, all surviving tasks are scheduled.
    """

    abstract = True

    @classmethod
    def apply_async(cls, *args, **kwargs):
        transaction.on_commit(lambda: super(PostTransactionTask, cls)
                              .apply_async(*args, **kwargs))

    @classmethod
    def delay(cls, *args, **kwargs):
        return cls.apply_async(args, kwargs)


task = partial(base_task, base=PostTransactionTask)

