import invoke
import src.lib.weight as weight
import src.lib.calory as calory


@invoke.task
def get_weights(c):
    weight.get_weights()


@invoke.task
def get_calories(c):
    calory.get_calories()
