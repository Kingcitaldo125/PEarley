'''test_earley.py'''
import sys
import pytest

sys.path.insert(0, '..')

from earley.earley import load_grammar, process_grammar, earley_parse


@pytest.fixture
def grammar_raw():
	gramm = load_grammar('..\\grammars\\grammar.txt')
	return gramm

@pytest.fixture
def grammar(grammar_raw):
	gram_dict = process_grammar(grammar_raw)
	return gram_dict


def test_process_grammar_pass(grammar):
	assert(grammar=={'P': 'S', 'S': 'S + M | M', 'M': 'M * T | T', 'T': 'number'})

def test_single_number_pass(grammar):
	res = earley_parse("1", grammar)
	
	assert(res)

def test_full_example_pass(grammar):
	res = earley_parse("2+3*4", grammar)
	
	assert(res)

def test_all_integers_pass(grammar):
	res = earley_parse("0+1+2+3+4+5+6+7+8+9", grammar)
	
	assert(res)

def test_addition_pass_1(grammar):
	res = earley_parse("1+2", grammar)
	
	assert(res)
	
def test_addition_pass_2(grammar):
	res = earley_parse("1+2+3", grammar)
	
	assert(res)

def test_addition_mul_pass(grammar):
	res = earley_parse("1+2*3", grammar)
	
	assert(res)

def test_fail_1(grammar):
	res = earley_parse("1+", grammar)
	
	assert res == False

def test_fail_2(grammar):
	res = earley_parse("1+2*", grammar)
	
	assert res == False

def test_fail_3(grammar):
	res = earley_parse("1+2*3/", grammar)
	
	assert res == False

def test_sub_fail_1(grammar):
	res = earley_parse("1-2", grammar)
	
	assert res == False

def test_sub_fail_2(grammar):
	res = earley_parse("1-", grammar)
	
	assert res == False

def test_div_fail_1(grammar):
	res = earley_parse("1/2", grammar)
	
	assert res == False

def test_div_fail_2(grammar):
	res = earley_parse("1/", grammar)
	
	assert res == False
