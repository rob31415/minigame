#
# this is a minigame
#
# it looks like this, for example:
#
#   5   1   0   -3
#   1   1   0   -4
#
#
# first row is computer numbers, changing randomly
# second row is controlled by player
#
# keys Q and W, de- and increase 1st value
# E&R 2nd, U&I 3rd, O&P 4th
#
# 
# a game lasts about 10 seconds in which the player
# has to match the first line of numbers as close as possible
#
# at the end, a "rapport" percentage is displayed
#
# my best was 92.5%
#
# this is just a little feasibility study for testing out and finetuning timing, mechanics etc.
# tje purpose is to find an applealing minigame to embed as small element
# in a bigger game. maybe as dialog minigame in an rpc or adventure game to make
# it challenging for a player to unlock some dialog options.
#

import curses	# for keypress polling
from random import randint
import datetime as dt


def deviate(direction):
	return randint(1,max(1,remainingGameTime())) * direction	#remainingGameTime()


def clip(val, mi, ma):
	val = mi if val < mi else val
	val = ma if val > ma else val
	return val


def changeMoodRandomly(value):
	value += randint(deviate(-1),deviate(1))
	value = clip(value,minValue,maxValue)
	return value

def changeMood(value, direction):
	value += direction
	value = clip(value,minValue,maxValue)
	return value

def now():
	return dt.datetime.now()  # you never get the same value twice

def remainingGameTime():
	return (gameTimeEnd - now()).seconds

def diff(int1, int2):
	return max(int1, int2) - min(int1, int2)

print("""to get ready, place your left hand fingers on "QWER", right hand on "UIOP".
	press ENTER to start""")
input()

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.nodelay(1)

npcMoodDimensions = [0, 0, 0, 0]
playerMoodDimensions = [0, 0, 0, 0]
minValue = -5
maxValue = 5
playTimeInSeconds = 7 	# seven seconds awäähhi
turnTimeInMs = 500
gameTimeEnd = now() + dt.timedelta(seconds=playTimeInSeconds)
t = now() - dt.timedelta(milliseconds=turnTimeInMs*2)



while now() < gameTimeEnd:

	stdscr.addstr(5,20, "t=" + str(remainingGameTime())+" ")

	if( int((now() - t).microseconds)/1000 >= turnTimeInMs-1 ):
		npcMoodDimensions = [changeMoodRandomly(e) for e in npcMoodDimensions]
		t = now()

	c = stdscr.getch()

	if c == ord('q'):
		playerMoodDimensions[0] = changeMood(playerMoodDimensions[0], deviate(-1))
	elif c == ord('w'):
		playerMoodDimensions[0] = changeMood(playerMoodDimensions[0], deviate(1))
	if c == ord('e'):
		playerMoodDimensions[1] = changeMood(playerMoodDimensions[1], deviate(-1))
	elif c == ord('r'):
		playerMoodDimensions[1] = changeMood(playerMoodDimensions[1], deviate(1))

	if c == ord('u'):
		playerMoodDimensions[2] = changeMood(playerMoodDimensions[2], deviate(-1))
	elif c == ord('i'):
		playerMoodDimensions[2] = changeMood(playerMoodDimensions[2], deviate(1))
	if c == ord('o'):
		playerMoodDimensions[3] = changeMood(playerMoodDimensions[3], deviate(-1))
	elif c == ord('p'):
		playerMoodDimensions[3] = changeMood(playerMoodDimensions[3], deviate(1))

	elif c == ord(' '):
		break

	stdscr.addstr(0,10, str(npcMoodDimensions[0])+" ")
	stdscr.addstr(0,20, str(npcMoodDimensions[1])+" ")
	stdscr.addstr(0,30, str(npcMoodDimensions[2])+" ")
	stdscr.addstr(0,40, str(npcMoodDimensions[3])+" ")

	stdscr.addstr(2,10, str(playerMoodDimensions[0])+" ")
	stdscr.addstr(2,20, str(playerMoodDimensions[1])+" ")
	stdscr.addstr(2,30, str(playerMoodDimensions[2])+" ")
	stdscr.addstr(2,40, str(playerMoodDimensions[3])+" ")


curses.nocbreak()
curses.echo()
curses.endwin()


summedDiffs = diff(playerMoodDimensions[0], npcMoodDimensions[0]) + \
		diff(playerMoodDimensions[1], npcMoodDimensions[1]) + \
		diff(playerMoodDimensions[2], npcMoodDimensions[2]) + \
		diff(playerMoodDimensions[3], npcMoodDimensions[3])

worstDiff = diff(minValue, maxValue)*4 #best is 0

rapportPercent = ((float(worstDiff)-float(summedDiffs))/worstDiff)*100


for e in npcMoodDimensions:
	print(e)

print("")

for e in playerMoodDimensions:
	print(e)

print("")

print ("play time was " + str(playTimeInSeconds))
print ("turn time ms was " + str(turnTimeInMs))
print ("")
print ("worst possible diff " + str(worstDiff))
print ("summedDiffs " + str(summedDiffs))
print ("")
print ("you scored a rapport value of " + str(rapportPercent) + "%")
