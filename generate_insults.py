#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   The MIT License (MIT)
   
   Copyright (C) 2015 Andris Raugulis (moo@arthepsy.eu)
   
   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:
   
   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.
   
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
"""
import os, sys, re, requests

INS_URL = 'http://www.sudo.ws/repos/sudo/raw-file/tip/plugins/sudoers/'
INSULTS = {'2001':'ins_2001.h', 
           'CLASSIC': 'ins_classic.h', 
           'GOONS':'ins_goons.h', 
           'CSOPS':'ins_csops.h'}

def usage(err=None):
	print "{0} <insults>\n".format(sys.argv[0])
	print "   <insults>  list of insults, separated by comma\n"
	print "   ALL        include all insults"
	print "   PC         use politically correct variations\n"
	print "   2001       HAL insults (paraphrased) from 2001"
	print "   CLASSIC    Insults from the original sudo"
	print "   GOONS      Insults from the Goon Show"
	print "   CSOPS      CSOps insults\n"
	print "example: {0} CLASSIC,2001,PC\n".format(sys.argv[0])
	if err is not None:
		print "{0}\n".format(err)
	sys.exit(1)

def parse_args():
	if len(sys.argv) != 2:
		usage()
	ins_types = set([x.upper() for x in sys.argv[1].split(',')])
	ins_all = False
	ins_pc = False
	for x in ins_types.copy():
		if x == 'ALL':
			ins_all = True
			ins_types.remove(x)
		elif x == 'PC':
			ins_pc = True
			ins_types.remove(x)
		elif x not in INSULTS:
			usage('error: unknown insult "{0}".'.format(x))
	if ins_all:
		ins_types.clear()
		ins_types = set(INSULTS.keys())
	if len(ins_types) == 0:
		usage('error: no insults defined.')
	return (ins_types, ins_pc)

def get_path(s):
	s = os.path.expanduser(s)
	if not os.path.isabs(s):
		cdir = os.path.dirname(os.path.realpath(__file__))
		s = os.path.join(cdir, s)
	return os.path.abspath(s)

def get_file(fn):
	url = INS_URL + fn
	r = requests.get(url, stream=True)
	if not r.ok:
		print "error: could not download {0}".format(url)
		sys.exit(1)
	data = ''
	for block in r.iter_content(1024):
		if not block:
			break
		data += block
	with open(get_path(fn), 'w') as fh:
		fh.write(data)

def get_insults(ins_types, ins_pc):
	insults = []
	state = 0 # normal insult
	for x in ins_types:
		ins_fn = INSULTS[x]
		if not os.path.isfile(ins_fn):
			get_file(ins_fn)
		fp = get_path(ins_fn)
		with open(fp, 'r') as fh:
			for rline in fh:
				line = rline.strip()
				if state == 0 and line == '#ifdef PC_INSULTS':
					state = 1 # politically correct
					continue
				if state == 1 and line == '#else':
					state = 2 # politically incorrect
					continue
				if state == 2 and line == '#endif':
					state = 0
					continue
				mx = re.match('^"(.*)",$', line)
				if mx:
					insult = mx.group(1)
					if insult.startswith('stty:'):
						continue
					if state == 1 and ins_pc == False:
						continue
					if state == 2 and ins_pc == True:
						continue
					insults.append(insult)
	return insults

def write_py_module(insults):
	py_head = '#!/usr/bin/env python\n'
	fp = get_path('SudoInsults.py')
	with open(fp, 'w') as fh:
		fh.write(py_head)
		fh.write('import time\n\n')
		fh.write('INSULTS = {0}\n\n'.format(insults))
		fh.write('def get_insult():\n')
		fh.write('\treturn INSULTS[int(round(time.time() * 1000)) % len(INSULTS)]\n\n')
	fp = get_path('demo.py')
	with open(fp, 'w') as fh:
		fh.write(py_head)
		fh.write('try:\n\tfrom SudoInsults import get_insult\n')
		fh.write('except:\n\tget_insult = None\t\n\n')
		fh.write('if get_insult: print get_insult()\n\n')

def main():
	(ins_types, ins_pc) = parse_args()
	insults = get_insults(ins_types, ins_pc)
	write_py_module(insults)
	
if __name__ == '__main__':
	main()

