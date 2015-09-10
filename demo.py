#!/usr/bin/env python
try:
	from SudoInsults import get_insult
except:
	get_insult = None	

if get_insult: print get_insult()

