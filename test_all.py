# test_all.py = run all tests

from ulib import lintest

#---------------------------------------------------------------------

group = lintest.TestGroup()

import test_board
group.add(test_board.group)

import test_movegen
group.add(test_movegen.group)

import test_evalpos
group.add(test_evalpos.group)

if __name__=='__main__': group.run()

#end
