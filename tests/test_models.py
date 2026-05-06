from extractbot.models import Task, Urgency, Importance, Priority

#def test_something():
#    result = my_function()
#    assert result == expected_value


def test_task():
    task = Task(title="Complete IT331 Assignment")

    assert task.title == "Complete IT331 Assignment"

def test_do_task():
    do_task = Task(
            title = "Quiz",
            urgency=Urgency.URGENT,
            importance = Importance.IMPORTANT)
    assert do_task.quadrant == Priority.DO


def test_delegate_task():
    delegate_task = Task(
            title = "Discussion Post",
            urgency = Urgency.URGENT,
            importance = Importance.NOT_IMPORTANT)
    assert delegate_task.quadrant == Priority.DELEGATE

def test_schedule_task():
    schedule_task = Task(
            title = "Seminar Summary",
            urgency = Urgency.NOT_URGENT,
            importance= Importance.IMPORTANT)
    assert schedule_task.quadrant == Priority.SCHEDULE


def test_eliminate_task():
    eliminate_task = Task(
            title = "Pay Classes",
            urgency = Urgency.NOT_URGENT,
            importance= Importance.NOT_IMPORTANT)
    assert eliminate_task.quadrant == Priority.ELIMINATE



