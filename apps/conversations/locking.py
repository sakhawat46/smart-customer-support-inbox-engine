from django.core.cache import cache

LOCK_TIMEOUT = 300  # 5 minutes


class ConversationLockService:

    @staticmethod
    def get_key(conversation_id):
        return f"conversation:{conversation_id}:lock"

    @classmethod
    def acquire_lock(cls, conversation_id, user):

        key = cls.get_key(conversation_id)

        if cache.get(key):
            return False

        cache.set(key, user.id, timeout=LOCK_TIMEOUT)

        return True

    @classmethod
    def release_lock(cls, conversation_id, user):

        key = cls.get_key(conversation_id)

        owner = cache.get(key)

        if owner == user.id:
            cache.delete(key)
            return True

        return False

    @classmethod
    def get_lock_owner(cls, conversation_id):

        key = cls.get_key(conversation_id)

        return cache.get(key)

    @classmethod
    def is_locked(cls, conversation_id):

        return cache.get(cls.get_key(conversation_id)) is not None