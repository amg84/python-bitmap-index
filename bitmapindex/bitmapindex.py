"""
    bitmapindex
    ~~~~~~~~~~~
    :copyright: (c) 2016 by Andrew Grundy.
    :license: GNU GPL 3, see LICENSE for more details.
"""

import re


class BitmapIndex:
    bucket_size = 1000

    def __init__(self, data=None):
        """
            Class init optionally takes run length encoded data.
        """
        self._count = 0
        self._data = {}
        if isinstance(data, str):
            self._read_rle(data)

    @property
    def ints(self):
        """
            This property returns a list of ints that represent the items set to true.
        """
        return list(self.yield_ints())

    @property
    def rle(self):
        """
            This property returns a run length encoded representation of the entire bitmap index.
        """
        # calculate tuples of (run, value)
        rle = []
        next_expected = 0
        run = 0
        for i in self.yield_ints():
            if next_expected != i:
                if run:
                    rle.append((run, 1))
                    run = 0
                rle.append(((i - next_expected), 0))
            run += 1
            next_expected = i + 1
        if run:
            rle.append((run, 1))

        # stringify
        _rle = []
        for current_count, current in rle:
            if current_count > 1:
                _rle.append("{0}{1}".format(current_count, current))
            else:
                _rle.append(str(current))
        rle = ".".join(_rle)

        return rle + "."

    def __getitem__(self, key):
        """
            This method looks up a value to see if it has been marked as true via the python mappings interface.
        """
        if not isinstance(key, int):
            raise TypeError()
        bucket_idx = self._get_bucket_idx(int(key))
        if bucket_idx not in self._data:
            return False

        pos = self._get_bucket_pos(int(key))

        return self._data[bucket_idx][pos]

    def __setitem__(self, key, value):
        """
            This method allows access to modify the private data via the python mappings interface.
        """
        if not isinstance(key, int) or not isinstance(value, bool):
            raise TypeError()
        self._modify(key, value)

    def __delitem__(self, key):
        """
            This method allows disabling index values via the python mappings interface.
        """
        if not isinstance(key, int):
            raise TypeError()
        self._modify(key, False)

    def __contains__(self, key):
        """
            This method looks up a value to see if it has been marked as true via the python sequences interface.
        """
        if not isinstance(key, int):
            raise TypeError()
        return self[key]

    def __len__(self):
        """
            This method returns the number of values marked as true via the python sequences interface.
        """
        return self._count

    def _read_rle(self, data):
        """
            This private method is used to read run length encoded data into the bitmap index instance.
        """
        re_read = re.compile("([0-9]*)([0-1]).")
        data = re_read.findall(data)
        idx = 0
        for _run, _bin in data:
            if _bin == '0':
                idx += int(_run or 1)
            else:
                for i in range(int(_run or 1)):
                    self.enable(idx)
                    idx += 1

    def _get_bucket_idx(self, key):
        """
            This method acquires the index of the bucket this value should reside in.
        """
        bucket_idx = int(key / self.bucket_size)
        return bucket_idx

    def _get_bucket_pos(self, key):
        """
            This method returns the index position this value should occupy within its bucket.
        """
        return (key % self.bucket_size)

    def _modify(self, key, value):
        """
            This private method allows access to modify the private data.
        """
        if not isinstance(key, int) or not isinstance(value, bool):
            raise TypeError()
        self._count += 1 if value else -1
        bucket_idx = self._get_bucket_idx(key)
        if bucket_idx not in self._data:
            self._data[bucket_idx] = [False] * self.bucket_size
        pos = self._get_bucket_pos(key)
        self._data[bucket_idx][pos] = value
    
    def enable(self, key):
        """
            This method is a thin wrapper around modify to set a value to true.
        """
        self._modify(key, True)

    def disable(self, key):
        """
            This method is a thin wrapper around modify to set a value to false.
        """
        self._modify(key, False)

    def yield_ints(self):
        """
            This generator yields integers that have been enabled.
        """
        bucket_indexes = list(self._data.keys())
        bucket_indexes.sort()
        for di in bucket_indexes:
            for i, v in enumerate(self._data[di]):
                if v:
                    yield (di * self.bucket_size) + i

