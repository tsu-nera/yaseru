import invoke
import src.lib.weight as weight
import src.lib.activity as activity


@invoke.task
def get_weights(c):
    weight.get_weights()


@invoke.task
def get_activities(c):
    activity.get_activities()
