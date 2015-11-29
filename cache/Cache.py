__author__ = 'yousefhamza'
import abc
from collections import namedtuple
from math import log


class Cache:
    __metaclass__ = abc.ABCMeta
    def __init__(self, number_of_blocks, words_per_block, memory_address_size, byte_addressed=True):
        assert words_per_block % 2 == 0 or words_per_block == 1 , 'words per block multiple of 2 or 1'
        assert memory_address_size % 4 == 0, 'address memory size multiple of 4 only'
        self._memory_address_size = memory_address_size
        self._words_per_block = words_per_block
        self._byte_addressed = byte_addressed

        self._word_index_size = int(log(words_per_block, 2))
        self._index_size = int(log(number_of_blocks, 2))

        words_string = "word0"
        for i in range(words_per_block - 1):
            words_string += " word%d" % (i + 1,)
        self._cache_block = namedtuple("cache_block", "valid tag %s" % words_string)
        self._cache = [None] * number_of_blocks

        self._hits = 0
        self._misses = 0

    def cache(self, address):
        assert len(address) * 4 == self._memory_address_size
        binary_address = self._hexStringToBinary(address)

        base = 0
        if self._byte_addressed:
            base = -2


        words = self._completeBlock(binary_address, base - self._word_index_size, base)
        base -= self._word_index_size

        index = binary_address[base - self._index_size: base]
        index = int(index, 2)
        base -= self._index_size

        tag = binary_address[:base]

        if self.isHit(binary_address, index):
            self._hits += 1
        else:
            self._misses += 1
            self._addToCache(index, tag, words)

    @abc.abstractmethod
    def isHit(self, address, index):
        """
        :param address: address to save
        :param index: index to save in (not used for full associative)
        :return: True if in cache, false if not
        """
        return

    @abc.abstractmethod
    def _addToCache(self, index, tag, words):
        """
        :param index: index to add to in cache (not used for full associative)
        :param tag: tag of the address to add
        :param words: the list of words per block
        :return: nothing
        """
        return

    @abc.abstractmethod
    def getCacheTable(self):
        """
        :return: a string of the table to print
        """
        return

    def getMissRate(self):
        print 'miss: ', self._misses
        print 'hit: ',  self._hits
        return self._misses / float(self._hits + self._misses)

    def _hexStringToBinary(self, hexString):
        return bin(int(hexString, 16))[2:].zfill(self._memory_address_size)

    def _completeBlock(self, binaryAddress, startIndex, endIndex):
        size = endIndex - startIndex
        if size == 0:
            return [binaryAddress]
        words = []
        for i in range(size + 1):
            currentAddress = list(binaryAddress)
            currentAddress[startIndex: endIndex] = bin(i)[2:].zfill(size)
            words += [''.join(currentAddress)]
        return words