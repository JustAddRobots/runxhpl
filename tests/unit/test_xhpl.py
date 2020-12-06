#!/usr/bin/env python3

from runxhpl.xhpl import get_result


def test_mem_percent(myxhpl):
    assert myxhpl.mem_percent == 30


def test_num_cores(myxhpl):
    assert isinstance(myxhpl.num_cores, int)


def test_mem_free(myxhpl):
    assert isinstance(myxhpl.mem_free, int)


def test_mem_xhpl(myxhpl):
    assert isinstance(myxhpl.mem_xhpl, int)


def test_P(myxhpl):
    assert isinstance(myxhpl.P, int)


def test_Q(myxhpl):
    assert isinstance(myxhpl.Q, int)


def test_N(myxhpl):
    assert isinstance(myxhpl.N, int)


def test_NB(myxhpl):
    assert isinstance(myxhpl.NB, int)


def test_hpl_dat(myxhpl):
    assert isinstance(myxhpl.hpl_dat, str)


def test_cmd(myxhpl):
    assert isinstance(myxhpl.cmd, str)


def test_status(myxhpl):
    assert isinstance(myxhpl.status, str)


def test_get_result(xhpl_result):
    assert get_result(xhpl_result) == ("PASSED", "0.19", "6.820e+01")
