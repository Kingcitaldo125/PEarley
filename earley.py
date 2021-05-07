'''earley.py'''

import re

dot = chr(8226)# •
prod_split = " | "

nonterminals = set(['P', 'S', 'M', 'T'])

parts_of_speech = ['+','*']
for i in range(1,5):
	parts_of_speech.append(str(i))

def init(words):
	# Generate the primary container that will be used
	# to hold all of the productions across the length of
	# the user's input
	S = [[] for x in range(len(words)+1)]
	return S

def is_finished(state, dot):
	global nonterminals
	# Check to see if the '•' is at the end of a particular production
	cond = state[1][-1] == dot # and first_item in nonterminals
	return cond

def is_nonterminal(element):
	global nonterminals
	# Check to see if a single (char or string of length '1')
	# is in the collection of known nonterminals
	return element in nonterminals

def swap_around_dot(state, dot):
	global nonterminals
	global parts_of_speech
	lax = list(state[1])
	#print("swap_around_dot lax",lax)
	swap_around_terminal = False
	idx = lax.index(dot)
	x=lax[idx + 1]

	# Locate the index of the '•', and swap its position in the 'lax'
	# list with the position of the item that is in front of it
	# return the string representation of the 'lax' list
	if x not in nonterminals and x not in parts_of_speech:
		swap_around_terminal = True
	if swap_around_terminal:
		lax = "".join("".join(lax).split(dot))
		lax+=dot
		lax=lax.split()
	else:
		tmp_dot = lax[idx]
		lax[idx] = lax[idx+1]
		lax[idx+1] = tmp_dot
	
	return "".join(lax)

def get_next_element(state, dot):
	global nonterminals
	global parts_of_speech
	state_payload = state[1]
	#print("get_next_element state_payload", state_payload])
	#print("state_payload.index(dot)", state_payload.index(dot))
	dotIdx = state_payload.index(dot)
	if dotIdx == len(state_payload)-1:
		#print("CANNOT GET NEXT STATE ELEM")
		return ""

	nxt_elem = None
	is_terminal = False
	# Logic here is in place to know if the next element that we're trying
	# to retrieve, relative to the '•', is either a terminal or nonterminal
	# symbol
	nxt_item = state_payload[state_payload.index(dot)+1]
	#print("nxt_item",nxt_item)
	if nxt_item not in nonterminals and nxt_item not in parts_of_speech:
		is_terminal = True

	if is_terminal:
		nxt_elem = "".join(state_payload.split(dot))
	else:
		nxt_elem = state_payload[state_payload.index(dot)+1]

	#print("nxt_elem:",nxt_elem)
	return nxt_elem

def state_print(S):
	# Helper code to print out the current state of the main collection
	for i,ss in enumerate(S):
		print(i,ss)

def predict(S, k, element, words, grammar, do_state_print=False):
	global dot
	global prod_split
	#print(f"PREDICTING k={k}")
	#print(f"{szero} in nonterminals")
	added = False
	prod = element
	gprod = grammar[prod]
	#print("prod",prod,"->","gprod",gprod)

	# continue to process each of the processed productions
	# split out each nonterminal's RHS, and then split on the '|'(pipe)
	# symbol. Add the splitted out pipe to the main collection, relative
	# to S[k]
	for prodd in gprod.split(prod_split):
		dProd = dot + prodd
		n_state = (prod, "".join(dProd.split(" ")), k)
		if not n_state in S[k]:
			#print("Adding production",n_state)
			S[k].append(n_state)
			added = True

	if do_state_print:
		state_print(S)

	return added


def scan(S, k, state, words, do_state_print=False):
	global dot
	global parts_of_speech
	#print(f"SCANNING; k={k}")
	#print("words[k]", words[k])
	#print("state[1]", state[1])
	nxt_elem_scanner = get_next_element(state, dot)
	#print("nxt_elem_scanner", nxt_elem_scanner)
	added = False
	if k > len(words)-1:
		return added
	# Check to see if the terminal symbol is a member of the language
	# If we've either gone 'over the deep end(k is out of range)', or we're in range,
	# but the word is not a part of speech, then we can be reasonably certain that
	# the input is not within the language
	if words[k] in parts_of_speech and (nxt_elem_scanner == words[k] or nxt_elem_scanner == 'number'):
		n_lax = swap_around_dot(state, dot)
		#print("Adding Scanner", n_lax, "to set", k)
		nitem = (state[0], n_lax, state[2])
		if not nitem in S[k+1]:
			S[k+1].append(nitem)
			added = True

	if do_state_print:
		state_print(S)

	return added


def complete(S, k, state, do_state_print=False):
	global dot
	#print(f"COMPLETING; k={k}")
	x = state[2]
	scopy = S[x].copy()
	added = False
	# Go through the list of copies and try to find
	# a collection of existing nonterminals.
	# This should be a reasonably good way of indicating
	# that certain productions in the 'set' are ready to
	# be completed, and that they're associated with 'state'
	# as it relates to S[k]
	for ss in scopy:
		ss_sym = "".join(ss[1].split(dot))
		#print("ss_sym:",ss_sym)
		if ss_sym[0] in nonterminals:
			n_lax = swap_around_dot(ss, dot)
			#print("Adding Completer", n_lax, "to set", k)
			# Assemble the new state, as it relates to 'ss'
			# and throw it in the associated set in the main container
			nitem = (ss[0], n_lax, ss[2])
			if not nitem in S[k]:
				S[k].append(nitem)
				added = True

	if do_state_print:
		state_print(S)

	return added


def earley_parse(words, grammar, do_state_print=False):
	global dot
	global nonterminals
	global prod_split
	expected = (("P",grammar["P"]+dot,0))

	# Create the data structure used to hold the sets
	S = init(words)
	# add to the set
	S[0].append(("P",dot+grammar["P"],0))
	done = False
	for k in range(len(words)+1):
		#print(f"k loop {k}")
		#print("S",S[k])
		added = True
		if done:
			break
		# Since the original pseudocode on Wikipedia is a bit lacking for the
		# original portion of the state sequence,
		# 'bootstrap' the algorithm foward by having it only move to the next state/set
		# when we did not add anything to 'S'
		while added and not done:
			added = False
			for state in S[k].copy():
				if expected in S[len(words)]:
					done = True
					break
				#print("state loop")
				#print("state",state)
				if not is_finished(state, dot):
					nxt_elem = get_next_element(state, dot)
					if is_nonterminal(nxt_elem): # predict
						#print("Predicting")
						added = predict(S, k, nxt_elem, words, grammar)
						#added = predict(S, k, nxt_elem, words, grammar, do_state_print = do_state_print)
						#print("Predicted", added)
					else: # scanner(terminal)
						#print("Scanning")
						added = scan(S, k, state, words)
						#added = scan(S, k, state, words, do_state_print = do_state_print)
						#print("Scanned", k)
				else: # we should be finished with a particular production
					#print("Completing")
					#added = complete(S, k, state)
					added = complete(S, k, state, do_state_print = do_state_print)
					#print("Completed", k)
			#print("")
			#print("")
			#print("")

	return expected in S[len(words)]


def load_grammar(location):
	g=""
	with open(location, "r") as f:
		for ff in f:
			g+=ff
	return g


def process_grammar(grammar):
	gmap = {}
	glist = grammar.split("\n")
	# regex to tokenize the number to a lexeme
	number_regex = re.compile(r"(\d\s[|]\s)+\d",re.M | re.I)
	for g in glist:
		#print("g",g)
		x = g.split(" -> ")
		#print(x)
		lhs = x[0]
		rhs = x[1]
		if re.match(number_regex, rhs):
			gmap[lhs] = "number"
			continue
		gmap[lhs] = rhs
	return gmap


def main():
	grammar = load_grammar(".\\grammar.txt")
	#print("Grammar:",grammar)
	pgrammar = process_grammar(grammar)
	#print("Processed Grammar:", pgrammar)
	print(earley_parse("2+3*4", pgrammar)) # True
	print(earley_parse("1", pgrammar)) # True
	print(earley_parse("1+", pgrammar)) # False
	print(earley_parse("1+2", pgrammar)) # True
	print(earley_parse("1+2*", pgrammar)) # False
	print(earley_parse("1+2*3", pgrammar)) # True
	print(earley_parse("1+2*3/", pgrammar)) # False

if __name__ == "__main__":
	main()
