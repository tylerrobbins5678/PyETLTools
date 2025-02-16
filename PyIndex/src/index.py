
from math import inf
from typing import Hashable, Iterable, Optional, TypeVar

T = TypeVar('T')

class Index:

    def __init__(self, objects: Optional[list[T]] = []) -> None:
        self._index: dict[str:dict[Hashable:set[T]]] = {}

    def add_object(
        self, 
        obj: T, 
        add_attrs: Optional[set[str]] = set(),
        ignore_attrs: Optional[set[str]] = set(),
        attr_default: Hashable = None
    ):
        '''
        adds the object to the index
         - object - the object to be added to the index
         - add - list of attributes to explicitly add
         - ignore - list of attributes to explicitly ignore
         - attr_default - the default of explicitly added attributes
        ignore occurs before add, so all attributes ignored will be added if included in both
        if an attribute that exist in add that does not exist in the object, it will become the value of attr_default
        '''
        # get all attrs of object T
        attrs: set = set(obj.__dict__.keys())
        attrs.update(ignore_attrs)
        attrs -= add_attrs
        for attr in attrs:
            self._update_index(obj, attr, attr_default)

        
    def _update_index(self, obj: T, attr: str, attr_default: Hashable = None):
        '''
        updates the index for a single attribute 
        '''
        if attr not in self._index:
            self._index[attr] = {}
        attr_val = getattr(obj, attr, attr_default)
        
        if not isinstance(attr_val, Hashable):
            raise TypeError(f"Unhashable type {type(attr)}")

        if attr_val not in self._index[attr]:
            self._index[attr][attr_val] = set()

        self._index[attr][attr_val].update({obj})

    def _get_search_order(self, attrs):
        counts = {}

        # use inf to denote 0 since that search will return 0 results
        # it will exclude the most objects since 0 are found
        for attr in attrs:
            if attr in self._index.keys():
                counts[attr] = len(self._index[attr]) or inf
            else:
                counts[attr] = inf
        
        order = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        return {attr:attrs[attr] for attr, _ in order}


    def get_by_attribute(self, **attrs) -> set[T]:
        
        # order attrs by most diversity first - performance improvement
        attrs = self._get_search_order(attrs)

        res: Optional[set[T]] = None
        for attr, vals in attrs.items():

            if not isinstance(vals, Iterable) or isinstance(vals, str):
                vals = [vals]

            single_arrt_val = set()
            for val in vals:
                if attr in self._index and val in self._index[attr]:
                    single_arrt_val.update(self._index[attr][val])

            if res == None:
                res = single_arrt_val
            else:
                res &= single_arrt_val

            if len(res) == 0:
                break
        
        return res
