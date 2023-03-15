import ape
import pytest


def test_standard_deposit(alice, weth9):
    weth9.deposit(value=10**18, sender=alice)

    assert weth9.balanceOf(alice) == 10**18
    assert weth9.totalSupply() == 10**18


def test_deposit_via_receive(alice, weth9):
    alice.transfer(weth9, value=10**18)

    assert weth9.balanceOf(alice) == 10**18
    assert weth9.totalSupply() == 10**18


def test_deposit_with_wrong_calldata(alice, weth9):
    with ape.reverts():
        alice.transfer(weth9, value=10**18, data=b"foo()")


def test_name(weth9):
    assert weth9.name() == "Wrapped Ether"


def test_symbol(weth9):
    assert weth9.symbol() == "WETH"


def test_decimals(weth9):
    assert weth9.decimals() == 18


@pytest.fixture
def setup(alice, weth9):
    alice.transfer(weth9, value=10**18)


def test_withdraw(alice, weth9, setup):
    pre_balance = alice.balance
    weth9.withdraw(10**18, sender=alice)

    assert weth9.balanceOf(alice) == 0
    assert alice.balance == pre_balance + 10**18


def test_withdraw_insufficient_balance(alice, weth9, setup):
    with ape.reverts():
        weth9.withdraw(10**19, sender=alice)


def test_transfer(alice, bob, weth9, setup):
    weth9.transfer(bob, 10**18, sender=alice)

    assert weth9.balanceOf(bob) == 10**18
    assert weth9.balanceOf(alice) == 0


def test_transfer_insufficient_balance(alice, bob, weth9, setup):
    with ape.reverts():
        weth9.transfer(bob, 10**19, sender=alice)


def test_approval(alice, bob, weth9):
    weth9.approve(bob, 10**18, sender=alice)

    assert weth9.allowance(alice, bob) == 10**18


def test_transfer_from(alice, bob, weth9, setup):
    weth9.approve(bob, 10**18, sender=alice)

    weth9.transferFrom(alice, bob, 10**18, sender=bob)

    assert weth9.balanceOf(alice) == 0
    assert weth9.balanceOf(bob) == 10**18


def test_transfer_from_insufficient_balance(alice, bob, weth9, setup):
    weth9.approve(bob, 10**18, sender=alice)

    with ape.reverts():
        weth9.transferFrom(alice, bob, 10**19, sender=bob)


def test_transfer_from_insufficient_allowance(alice, bob, weth9, setup):
    with ape.reverts():
        weth9.transferFrom(alice, bob, 10**18, sender=bob)
