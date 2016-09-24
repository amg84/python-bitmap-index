# python-bitmap-index
A pure python bitmap index.

### Example usage

```python
In [1]: from bitmapindex import BitmapIndex

# construct an empty bitmap index
In [2]: b = BitmapIndex()

# set 47 to True
In [3]: b[47] = True

# run length encoding representation of the bitmap index
In [4]: b.rle
Out[4]: '470.1.'

# list of integers representation of the bitmap index
In [5]: b.ints
Out[5]: [47]

# check if 47 has been set to true
In [6]: 47 in b
Out[6]: True

# count the number of items set to true in the bitmap index
In [7]: len(b)
Out[7]: 1

# remove 47 from the bitmap index
In [8]: del b[47]

# check the status of 47 - it should've been set to False
In [9]: b[47]
Out[9]: False
```
