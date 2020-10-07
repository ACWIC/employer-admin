import uuid

class Random:

	@staticmethod
	def get_uuid():
		return str(uuid.uuid4())
