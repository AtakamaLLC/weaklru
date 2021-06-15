# weaklru

Simple combination of a weakref cache and a lru cache.

```

class Obj:
  pass


l = WeakLRU(max_size=2)

l.set("a", Obj())
l.set("b", Obj())
l.set("c", Obj())
l.get(a)        # none
l.get(b)        # obj
l.get(c)        # obj
```


You can add objects to the cache, and they will never expire as long as they are being used.

Also, a maximum number of objects will be stored in the LRU portion of the cache.
