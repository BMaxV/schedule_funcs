# schedule_funcs

Module to do calculations around tasks, on a weekly base for now.

Goals are to add functionality around feedback / reporting, functions to serialize and deserialize.

Later as a separate object, maybe desktop notifications or something.

There is a rendering function over here https://github.com/BMaxV/schedule_render but that won't work because what I'm doing it with is code I will keep private.

# functionality

The key idea is to have different tasks, with different priorities, prefered and "must have" scheduled times, and finding the time slots for other things.

I plan to extend this to provide different kinds of schedules and info, for example you might schedule a vacation, and plan certain events for that vacation, but to outside observer, all that time should just be "reserved/not available".

Alternatively, it might be interesting to other members of your team, when you have scheduled certain activities and events, but you don't really need anyone else having access to that kind of information.

So the need for different kinds of users and user groups and priorities and "interruptability" is kind of obvious.

Here is an example of input:

```
def test(vertical=True):
    tasks=[
            task_class("Task 1",0.5,4,priority=2),
            task_class("wake up",1,0,priority=0),
            task_class("work session",3,prefered_time=9,prefered_day_type="work",priority=0),
            task_class("work session2",5,prefered_time=14,prefered_day_type="work",priority=0),
            task_class("Task 2",1,prefered_day_frequency=1,priority=2),
            task_class("lunch break",2,prefered_time=12,priority=1),
            task_class("sleep",9,prefered_time=22,prefered_day_frequency=0,priority=0),
            ]
    schedule=schedule_tasks(tasks)
    build_table(schedule,"regular",vertical=vertical)
    
    schedule=convert_to_external(schedule)
    build_table(schedule,"blocked",vertical=vertical)
```

Here is a picture of output:

![hello there](regular.svg)
