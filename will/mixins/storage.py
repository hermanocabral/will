import logging
import redis
import urlparse
import dill as pickle

from will import settings


class StorageMixin(object):
    def bootstrap_storage(self):
        # redis://localhost:6379/7
        # or
        # redis://rediscloud:asdfkjaslkdjflasdf@pub-redis-12345.us-east-1-1.2.ec2.garantiadata.com:12345
        url = urlparse.urlparse(settings.WILL_REDIS_URL)

        if hasattr(url, "path"):
            db = url.path[1:]
        else:
            db = 0

        self.storage = redis.Redis(host=url.hostname, port=url.port, db=db, password=url.password)

    def save(self, key, value):
        if not hasattr(self, "storage"):
            self.bootstrap_storage()
        print "saving %s...." % key
        print self.storage
        pipe = self.storage.pipeline()
        try:
            ret = pipe.set(key, pickle.dumps(value))
            # This really shouldn't be needed, but without it, a subsequent load fails.
            _ = pipe.get(key)
            # pipe.save()
            print ret
            pipe.execute()
            print pickle.loads(_)
            return ret
        except:
            import traceback; traceback.print_exc();
            logging.warn("Unable to save %s" % key)

    def clear(self, key):
        if not hasattr(self, "storage"):
            self.bootstrap_storage()
        return self.storage.delete(key)

    def clear_all_keys(self):
        if not hasattr(self, "storage"):
            self.bootstrap_storage()
        return self.storage.flushdb()

    def load(self, key, default=None):
        if not hasattr(self, "storage"):
            self.bootstrap_storage()

        try:
            val = self.storage.get(key)
            if val is not None:
                return pickle.loads(val)
                
        except:
            logging.warn("Unable to load %s" % key)

        return default
