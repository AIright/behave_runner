# @given('run with the wolfs')
# @when('catching this rabbit')
# @then('block whole infrastructure')

Feature: Run 1

    @environment.lock
    Scenario: Number 1
        Given run with the wolfs
        When catching this rabbit
        Then block whole infrastructure
