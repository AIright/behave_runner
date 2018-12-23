import redis
from random import randint
from time import sleep


def before_all(context):
    context.redis_connection = redis.StrictRedis()
    context.test_id = "TestRun:{0}_{1}".format(randint(0, 99), randint(0, 99))
    context.redis_connection.set(context.test_id, "paused")


def after_all(context):
    context.redis_connection.delete(context.test_id)


def before_scenario(context, scenario):
    runs_statuses = get_all_values_from_db(context)
    if ("wait_for_block" in runs_statuses) or ("blocker" in runs_statuses):
        context.redis_connection.set(context.test_id, "paused")
        while True:
            print(context.test_id, ' : ', "PAUSED: ", context.feature.name, ' : ', runs_statuses)
            runs_statuses = get_all_values_from_db(context)
            if ("wait_for_block" in runs_statuses) or ("blocker" in runs_statuses):
                sleep(1)
            else:
                context.redis_connection.set(context.test_id, "in_progress")
                break


def before_tag(context, tag):
    if tag == "environment.lock":
        context.redis_connection.set(context.test_id, "paused")
        while True:
            runs_statuses = get_all_values_from_db(context)
            if ("wait_for_block" in runs_statuses) or ("blocker" in runs_statuses):
                sleep(1)
            else:
                context.redis_connection.set(context.test_id, "wait_for_block")
                break

        while True:
            runs_statuses = get_all_values_from_db(context)
            if "in_progress" in runs_statuses:
                sleep(1)
            elif ("wait_for_block" in runs_statuses) or ("blocker" in runs_statuses):
                context.redis_connection.set(context.test_id, "paused")
                sleep(randint(0, 10))
                context.redis_connection.set(context.test_id, "wait_for_block")
            else:
                context.redis_connection.set(context.test_id, "blocker")
                # Ensure that all on pause
                sleep(3)
                runs_statuses = get_all_values_from_db(context)
                if (("wait_for_block" in runs_statuses)
                        or ("blocker" in runs_statuses)
                        or ("in_progress" in runs_statuses)):
                    context.redis_connection.set(context.test_id, "wait_for_block")
                else:
                    print(context.test_id, ' : ', "ENVIRONMENT IS LOCKED: ", context.feature.name, ' : ', runs_statuses)
                    break


def after_tag(context, tag):
    if tag == "environment.lock":
        context.redis_connection.set(context.test_id, "in_progress")
        print(context.test_id, ' : ', "IN_PROGRESS ", context.feature.name)


def get_all_values_from_db(context):
    test_runs = context.redis_connection.keys('*')
    statuses = []
    for test_run in test_runs:
        if test_run.decode() != context.test_id:
            test_state = context.redis_connection.get(test_run)
            if test_state:
                statuses.append(test_state.decode())
    return statuses


def clear_db():
    con = redis.StrictRedis()
    test_runs = con.keys('*')
    for test_run in test_runs:
        con.delete(test_run)


# DEBUG ZONE
# clear_db()
