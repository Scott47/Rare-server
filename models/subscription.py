from datetime import datetime

class Subscription:
    
    def __init__(self,
                id,
                follower_id,
                author_id,
                created_on,
                ended_on=None):
        
        self.id = id
        self.follower_id = follower_id
        self.author_id = author_id
        self.created_on = datetime.Today()
        self.ended_on = datetime