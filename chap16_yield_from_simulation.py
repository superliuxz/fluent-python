from collections import namedtuple
from queue import PriorityQueue
import random

Event = namedtuple('Event', 'time proc action')

def taxi_process(ident, trips, start_time=0):
	time = yield Event(start_time, ident, 'leaving garage')
	for t in range(trips):
		time = yield Event(time, ident, 'pick up passenger')
		time = yield Event(time, ident, 'drop off passenger')
	yield Event(time, ident, 'going home')

def calc_time(prev_action):
	if prev_action == 'leaving garage' or 'drop off passenger':
		interval = 5
	elif prev_action == 'pick up passenger':
		interval = 20
	elif prev_action == 'going home':
		interval = 1
	return int(random.expovariate(1/interval))+1

class Sim:
	def __init__(self, process_map):
		self.events = PriorityQueue()
		self.procs = dict(process_map)

	def run(self):
		for key, proc in self.procs.items():
			first_event = next(proc)
			self.events.put(first_event)

		while not self.events.empty():
			curr_event = self.events.get()
			event_time, proc_id, prev_action = curr_event
			print('taxi', proc_id, proc_id*'\t', curr_event)
			active_proc = self.procs[proc_id]
			next_time = event_time + calc_time(prev_action)
			try:
				next_event = active_proc.send(next_time)
			except StopIteration:
				del self.procs[proc_id]
			else:
				self.events.put(next_event)
		else:
			print('*** END OF SIM***')

random.seed(42)
# taxi 0: start at 0, 2 trips
# taxi 1: start at 5, 4 trips
# taxi 2: start at 10, 6 trips
taxis = {i: taxi_process(i, (i+1)*2, i*5) for i in range(3)}
s = Sim(taxis)
s.run()