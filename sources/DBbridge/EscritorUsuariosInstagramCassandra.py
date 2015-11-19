from Escritor import Escritor
from Cassandra.ConexionCassandra import ConexionCassandra

class EscritorUsuariosInstagramCassandra(Escritor):
	"""docstring for EscritorUsuariosInstagramCassandra"""
	def __init__(self, searchID):
		super(EscritorUsuariosInstagramCassandra, self).__init__(searchID)
		self.session = ConexionCassandra().getSessionInstagram()
		self.asinc = False

	def escribe(self, data):
		"""
		'CREATE TABLE users ('
		             'id bigint PRIMARY KEY'
		             ', username varchar'
		             ', full_name varchar'
		             ', followers int'
		             ', following int'
		             ', bio varchar'
		             ', profile_picture varchar'
		             ', last_media_collected bigint);'

		"id": "1574083",
        "username": "snoopdogg",
        "full_name": "Snoop Dogg",
        "profile_picture": "http://distillery.s3.amazonaws.com/profiles/profile_1574083_75sq_1295469061.jpg",
        "bio": "This is my bio",
        "website": "http://snoopdogg.com",
        "counts": {
            "media": 1320,
            "follows": 420,
            "followed_by": 3410
        }
		"""

		for u in data:
			try:
				query = """INSERT INTO users (id, username, full_name, followers, following, bio, profile_picture) 
				VALUES (%s, %s, %s, %s, %s, %s, %s)"""

				if self.asinc:
					self.session.execute_async(query,(long(u.id), u.username, u.full_name, u.counts["followed_by"], u.counts["follows"],
						u.bio, u.profile_picture))
				else:
					self.session.execute(query,(long(u.id), u.username, u.full_name, u.counts["followed_by"], u.counts["follows"],
						u.bio, u.profile_picture))

			except Exception, e:
				query = """INSERT INTO users (id, username, full_name, profile_picture)
				VALUES (%s, %s, %s, %s)"""

				if self.asinc:
					self.session.execute_async(query,(long(u.id), u.username, u.full_name, u.profile_picture))
				else:
					self.session.execute(query,(long(u.id), u.username, u.full_name, u.profile_picture))



