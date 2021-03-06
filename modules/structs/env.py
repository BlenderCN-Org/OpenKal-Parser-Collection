#!/usr/bin/python3.5

import sys
import utility

from struct import unpack
from utility import ValidationError
from utility import VersionError


class ENVLight(object):
    __slots__ = [
        'r',
        'g',
        'b',
        'a',
    ]

    def parse(self, stream):
        _ = unpack('<I', stream.read(4))[0] # Boolean

        self.r, \
        self.g, \
        self.b, \
        self.a = utility.read_d3dx_color(stream)
        return self

    def write(self, stream):
        raise NotImplementedError


class ENVLayer(object):
    __slots__ = [
        'scale_u',
        'scale_v',
        'path',
    ]

    def parse(self, stream):
        self.scale_u = unpack('<I', stream.read(4))[0]
        self.scale_v = unpack('<I', stream.read(4))[0]
        self.path    = utility.read_string_pre(stream)
        return self

    def write(self, stream):
        raise NotImplementedError


class ENVFile(object):
    __slots__ = [
        'decals',
        'lights',
        'layers',
    ]

    def parse(self, stream):
        _, _, _, _, \
        _, _, _, _, \
        version = unpack('<9I', stream.read(9 * 4))

        if version != 7:
            raise VersionError('ENV version %d is unsupported' % version)

        self.decals = []
        self.lights = []
        self.layers = []

        for _ in range(unpack('<I', stream.read(4))[0]):
            self.decals.append(
                (unpack('<I', stream.read(4))[0], utility.read_string_pre(stream))
            )

        for _ in range(24):
            self.lights.append(ENVLight().parse(stream))

        for _ in range(unpack('<I', stream.read(4))[0]):
            self.layers.append(ENVLayer().parse(stream))

        # Verify
        if stream.read(1):
            raise ValidationError('Too many bytes in ENV structure')

        return self

    def write(self, stream):
        raise NotImplementedError
