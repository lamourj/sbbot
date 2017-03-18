class Friends:
"""
Handles relations of friends for users.
"""

	def __init__(self):
		self.table = dict()

	"""
	Adds the specified friend to the specified user's list of friends.
	"""
	def addFriendForUser(uid, friendUid):
		if uid in self.table:
			if not friendUid in self.table[uid]: # add only if friend not already present.
				self.table[uid].append(friendUid)
		else:
			self.table[uid] = [friendUid]