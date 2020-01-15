import invoke
import src.lib.weight as weight


@invoke.task
def get_weights(c):
    weight.get_weights()
