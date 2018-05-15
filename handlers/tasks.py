"""
The tasks module provides a handler class (TaskHandler) which allows a
tasklet to create other tasklets.

If a tasklet yields a generator object, it is installed into the scheduler
and will run concurrently with the tasklet.

If a tasklet yields a Wait object with a generator object as its argument,
it will install the generator into the scheduler (making it a tasklet) and 
pause its execution and wait until the new tasklet is finished.

"""

import types



class Finished(Exception):
    """Raised when a sub task finishes.
    """
    pass


class Async(object):
    """yield Async(task) to start another task and run it concurrently.
    """
    def __init__(self, task, watch=None):
        self.task = task
        self.watch = watch


class Return(object):
    """yield Return(value) from a spawned generator to return that value
    to the waiting task.
    """
    def __init__(self, value):
        self.value = value


class TasksHandler(object):
    """The task handler allows running tasks to start other tasks by 
    yielding generator, on_finish or spawn objects.
    """
    handled_types = [Async, StopIteration, types.GeneratorType, Return]
    def __init__(self):
        self.tasks = []
        self.waiting_tasks = {}
        self.handlers = dict((i, getattr(self, "handle_%s" % i.__name__)) for i in self.handled_types)

    def handle(self, new_task, task):
        self.handlers[type(new_task)](new_task, task)

    def handle_Return(self, event, task):
        try:
            waiting_task = self.waiting_tasks.pop(task)
        except KeyError, e:
            raise RuntimeError("Return yielded from a top level task.")
        self.schedule.unwatch(task)
        self.schedule.install(waiting_task, event.value)

    def handle_StopIteration(self, exception, task):
        try:
            v = None
            if task in self.schedule.watchers:
                self.schedule.unwatch(task)
                #v = Finished() #TODO only do this if requested.
            self.schedule.install(self.waiting_tasks.pop(task), v)
                
        except KeyError:
            pass

    def handle_Async(self, event, task):
        self.tasks.extend((event.task, task))
        if event.watch:
            self.schedule.watch(event.task, event.watch)

    def handle_generator(self, new_task, task):
        def watcher(e):
            parent = self.waiting_tasks.pop(new_task)
            self.schedule.install(parent, e)
        self.waiting_tasks[new_task] = task
        self.schedule.watch(new_task, watcher)
        self.tasks.append(new_task) 

    def pre_schedule(self): 
        for t in self.tasks:
            self.schedule.install(t)
        self.tasks[:] = []
        return len(self.tasks) > 0 or len(self.waiting_tasks) > 0