class FriendsTable:
"""
Handles relations of friends for users.
"""

    def __init__(self):
        self.table = dict()


    def addFriendForUser(self, uid, friendUid):
        """
        Adds the specified friend to the specified user's list of friends.
        """
        if uid in self.table:
            if not friendUid in self.table[uid]: # add only if friend not already present.
                self.table[uid].append(friendUid)
        else:
            self.table[uid] = [friendUid]

    def getFriendsForUser(self, uid):
        """
        Returns the friends uids for specified uid or None if
        uid has no registrated friends.
        """
        if uid in self.table:
            return self.table[uid]
        else:
            return None