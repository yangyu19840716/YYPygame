# -*- coding:utf-8 -*-

import os
import time
import cProfile
from Core import Const


class Profiler(object):
	def __init__(self):
		self.saved_dir = Const.ROOT_PATH + 'tmp/PythonProfiling/'
		if not os.path.exists(self.saved_dir):
			os.makedirs(self.saved_dir)

		self.profile = cProfile.Profile()
		self.profile.enable()

		self.is_profiling = False
		self.start_ts = 0
		self.end_ts = 0
		self.cost_ts = 0
		self.can_dump = False

		self.label = 'NoLabel'

	def reset_states(self):
		self.is_profiling = False
		self.start_ts = 0
		self.end_ts = 0
		self.cost_ts = 0
		self.can_dump = False

	def start(self):
		if self.is_profiling is True:
			print('Profiler already working.')
			return

		self.reset_states()
		self.is_profiling = True
		self.start_ts = time.time()

	def stop(self):
		if self.is_profiling is False:
			print('Profiler already closed.')
			return

		self.is_profiling = False
		self.end_ts = time.time()
		self.cost_ts = self.end_ts - self.start_ts
		self.can_dump = True

		self.profile.disable()

		self.dump_data()

	def dump_data(self):
		if self.can_dump is False:
			print('Profiler can not dump yet')
			return

		full_file_name = self.saved_dir + "Profile_{label}.prof".format(label=self.label)
		self.profile.dump_stats(full_file_name)
		self.profile = None

		print('Profiling ended. File is saved to %s.' % full_file_name)

		simple_info = {
			'label': self.label,
			'start_ts': self.start_ts,
			'end_ts': self.end_ts,
			'duration': self.end_ts - self.start_ts,
		}

		print(simple_info)
