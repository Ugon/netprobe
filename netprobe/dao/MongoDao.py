class MongoDao(object):
    def __init__(self, client, db_name, collection_name):
        self.client = client
        self.db_name = db_name
        self.collection_name = collection_name
        self.collection = client[db_name][collection_name]

    def insert(self, measurement_id, sample_id, timestamp):
        self.collection.insert_one({
            'measurement_id': measurement_id,
            'sample_id': sample_id,
            'timestamp': timestamp})

    def get_all(self, measurement_id):
        result = list(self.collection.find(
            {'measurement_id': measurement_id},
            {'sample_id': 1, 'timestamp': 1, '_id': 0}))

        for obj in result:
            obj['sample_id'] = str(obj['sample_id'])

        return result

    def get_all_icmp(self, measurement_id):
        result = list(self.collection.find(
            {'measurement_id': measurement_id},
            {'sample_id': 1, 'timestamp': 1, '_id': 0}))

        return result
