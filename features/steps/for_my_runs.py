from behave import *
from time import sleep


@given('run with the wolfs')
def run_with_wolfs(context):
    a = 3
    print("I am running and my name is {}".format(context.scenario.name))
    sleep(a)
    print("I am {0} and I was running for {1} seconds".format(context.scenario.name, a))


@when('catching this rabbit')
def catch_this_rabbit(context):
    a = 4
    print("I will catch it because I am {}".format(context.scenario.name))
    sleep(a)
    print("Oh, sorry, I was sleeping for {0} seconds. It is {1} fault!".format(a, context.scenario.name))


@then('block whole infrastructure')
def infrastructure_blocker(context):
    a = 5
    print("I am {} and I have just blocked the infrastructure".format(context.scenario.name))
    sleep(a)
    print("OK! Now it is free. Kind regards {}".format(context.scenario.name))