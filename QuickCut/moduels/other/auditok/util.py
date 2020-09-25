"""
Class summary
=============

.. autosummary::

        AudioEnergyValidator
        AudioReader
        Recorder
"""
from __future__ import division
import sys
from abc import ABC, abstractmethod
import warnings
from functools import partial
from audioop import tomono
from .io import (
    AudioIOError,
    AudioSource,
    from_file,
    BufferAudioSource,
    PyAudioSource,
    get_audio_source,
)
from .exceptions import (
    DuplicateArgument,
    TooSamllBlockDuration,
    TimeFormatError,
)

try:
    from . import signal_numpy as signal
except ImportError:
    from . import signal


__all__ = [
    "make_duration_formatter",
    "DataSource",
    "DataValidator",
    "StringDataSource",
    "ADSFactory",
    "AudioDataSource",
    "AudioReader",
    "Recorder",
    "AudioEnergyValidator",
]


def make_duration_formatter(fmt):
    """
    Accepted format directives: %i %s %m %h
    """
    if fmt == "%S":

        def fromatter(seconds):
            return "{:.3f}".format(seconds)

    elif fmt == "%I":

        def fromatter(seconds):
            return "{0}".format(int(seconds * 1000))

    else:
        fmt = fmt.replace("%h", "{hrs:02d}")
        fmt = fmt.replace("%m", "{mins:02d}")
        fmt = fmt.replace("%s", "{secs:02d}")
        fmt = fmt.replace("%i", "{millis:03d}")
        try:
            i = fmt.index("%")
            raise TimeFormatError(
                "Unknow time format directive '{0}'".format(fmt[i : i + 2])
            )
        except ValueError:
            pass

        def fromatter(seconds):
            millis = int(seconds * 1000)
            hrs, millis = divmod(millis, 3600000)
            mins, millis = divmod(millis, 60000)
            secs, millis = divmod(millis, 1000)
            return fmt.format(hrs=hrs, mins=mins, secs=secs, millis=millis)

    return fromatter


def make_channel_selector(sample_width, channels, selected=None):
    fmt = signal.FORMAT.get(sample_width)
    if fmt is None:
        err_msg = "'sample_width' must be 1, 2 or 4, given: {}"
        raise ValueError(err_msg.format(sample_width))
    if channels == 1:
        return lambda x: x

    if isinstance(selected, int):
        if selected < 0:
            selected += channels
        if selected < 0 or selected >= channels:
            err_msg = "Selected channel must be >= -channels and < 'channels'"
            err_msg += ", given: {}"
            raise ValueError(err_msg.format(selected))
        return partial(
            signal.extract_single_channel,
            fmt=fmt,
            channels=channels,
            selected=selected,
        )

    if selected in ("mix", "avg", "average"):
        if channels == 2:
            # when data is stereo, using audioop when possible is much faster
            return partial(
                signal.average_channels_stereo, sample_width=sample_width
            )

        return partial(signal.average_channels, fmt=fmt, channels=channels)

    if selected in (None, "any"):
        return partial(signal.separate_channels, fmt=fmt, channels=channels)

    raise ValueError(
        "Selected channel must be an integer, None (alias 'any') or 'average' "
        "(alias 'avg' or 'mix')"
    )


class DataSource(ABC):
    """
    Base class for objects passed to
    :func:`auditok.core.StreamTokenizer.tokenize`.
    Subclasses should implement a :func:`DataSource.read` method.
    """

    @abstractmethod
    def read(self):
        """
        Read a piece of data read from this source.
        If no more data is available, return None.
        """


class DataValidator(ABC):
    """
    Base class for a validator object used by :class:`.core.StreamTokenizer`
    to check if read data is valid.
    Subclasses should implement :func:`is_valid` method.
   """

    @abstractmethod
    def is_valid(self, data):
        """
        Check whether `data` is valid
        """


class AudioEnergyValidator(DataValidator):
    def __init__(
        self, energy_threshold, sample_width, channels, use_channel=None
    ):
        self._sample_width = sample_width
        self._selector = make_channel_selector(
            sample_width, channels, use_channel
        )
        if channels == 1 or use_channel not in (None, "any"):
            self._energy_fn = signal.calculate_energy_single_channel
        else:
            self._energy_fn = signal.calculate_energy_multichannel
        self._energy_threshold = energy_threshold

    def is_valid(self, data):
        log_energy = self._energy_fn(self._selector(data), self._sample_width)
        return log_energy >= self._energy_threshold


class StringDataSource(DataSource):
    """
    A class that represent a :class:`DataSource` as a string buffer.
    Each call to :func:`DataSource.read` returns on character and moves one
    step forward. If the end of the buffer is reached, :func:`read` returns
    None.

    :Parameters:

        `data` :
            a str object.

    """

    def __init__(self, data):

        self._data = None
        self._current = 0
        self.set_data(data)

    def read(self):
        """
        Read one character from buffer.

        :Returns:

            Current character or None if end of buffer is reached
        """

        if self._current >= len(self._data):
            return None
        self._current += 1
        return self._data[self._current - 1]

    def set_data(self, data):
        """
        Set a new data buffer.

        :Parameters:

            `data` : a str object
                New data buffer.
        """

        if not isinstance(data, str):
            raise ValueError("data must an instance of str")
        self._data = data
        self._current = 0


class ADSFactory:
    """
    Factory class that makes it easy to create an
    :class:`ADSFactory.AudioDataSource` object that implements
    :class:`DataSource` and can therefore be passed to
    :func:`auditok.core.StreamTokenizer.tokenize`.

    Whether you read audio data from a file, the microphone or a memory buffer,
    this factory instantiates and returns the right
    :class:`ADSFactory.AudioDataSource` object.

    There are many other features you want your
    :class:`ADSFactory.AudioDataSource` object to have, such as: memorize all
    read audio data so that you can rewind and reuse it (especially useful when
    reading data from the microphone), read a fixed amount of data (also useful
    when reading from the microphone), read overlapping audio frames
    (often needed when dosing a spectral analysis of data).

    :func:`ADSFactory.ads` automatically creates and return object with the
    desired behavior according to the supplied keyword arguments.
    """

    @staticmethod  # noqa: C901
    def _check_normalize_args(kwargs):

        for k in kwargs:
            if k not in [
                "block_dur",
                "hop_dur",
                "block_size",
                "hop_size",
                "max_time",
                "record",
                "audio_source",
                "filename",
                "data_buffer",
                "frames_per_buffer",
                "sampling_rate",
                "sample_width",
                "channels",
                "sr",
                "sw",
                "ch",
                "asrc",
                "fn",
                "fpb",
                "db",
                "mt",
                "rec",
                "bd",
                "hd",
                "bs",
                "hs",
            ]:
                raise ValueError("Invalid argument: {0}".format(k))

        if "block_dur" in kwargs and "bd" in kwargs:
            raise DuplicateArgument(
                "Either 'block_dur' or 'bd' must be specified, not both"
            )

        if "hop_dur" in kwargs and "hd" in kwargs:
            raise DuplicateArgument(
                "Either 'hop_dur' or 'hd' must be specified, not both"
            )

        if "block_size" in kwargs and "bs" in kwargs:
            raise DuplicateArgument(
                "Either 'block_size' or 'bs' must be specified, not both"
            )

        if "hop_size" in kwargs and "hs" in kwargs:
            raise DuplicateArgument(
                "Either 'hop_size' or 'hs' must be specified, not both"
            )

        if "max_time" in kwargs and "mt" in kwargs:
            raise DuplicateArgument(
                "Either 'max_time' or 'mt' must be specified, not both"
            )

        if "audio_source" in kwargs and "asrc" in kwargs:
            raise DuplicateArgument(
                "Either 'audio_source' or 'asrc' must be specified, not both"
            )

        if "filename" in kwargs and "fn" in kwargs:
            raise DuplicateArgument(
                "Either 'filename' or 'fn' must be specified, not both"
            )

        if "data_buffer" in kwargs and "db" in kwargs:
            raise DuplicateArgument(
                "Either 'filename' or 'db' must be specified, not both"
            )

        if "frames_per_buffer" in kwargs and "fbb" in kwargs:
            raise DuplicateArgument(
                "Either 'frames_per_buffer' or 'fpb' must be specified, not "
                "both"
            )

        if "sampling_rate" in kwargs and "sr" in kwargs:
            raise DuplicateArgument(
                "Either 'sampling_rate' or 'sr' must be specified, not both"
            )

        if "sample_width" in kwargs and "sw" in kwargs:
            raise DuplicateArgument(
                "Either 'sample_width' or 'sw' must be specified, not both"
            )

        if "channels" in kwargs and "ch" in kwargs:
            raise DuplicateArgument(
                "Either 'channels' or 'ch' must be specified, not both"
            )

        if "record" in kwargs and "rec" in kwargs:
            raise DuplicateArgument(
                "Either 'record' or 'rec' must be specified, not both"
            )

        kwargs["bd"] = kwargs.pop("block_dur", None) or kwargs.pop("bd", None)
        kwargs["hd"] = kwargs.pop("hop_dur", None) or kwargs.pop("hd", None)
        kwargs["bs"] = kwargs.pop("block_size", None) or kwargs.pop("bs", None)
        kwargs["hs"] = kwargs.pop("hop_size", None) or kwargs.pop("hs", None)
        kwargs["mt"] = kwargs.pop("max_time", None) or kwargs.pop("mt", None)
        kwargs["asrc"] = kwargs.pop("audio_source", None) or kwargs.pop(
            "asrc", None
        )
        kwargs["fn"] = kwargs.pop("filename", None) or kwargs.pop("fn", None)
        kwargs["db"] = kwargs.pop("data_buffer", None) or kwargs.pop(
            "db", None
        )

        record = kwargs.pop("record", False)
        if not record:
            record = kwargs.pop("rec", False)
            if not isinstance(record, bool):
                raise TypeError("'record' must be a boolean")

        kwargs["rec"] = record

        # keep long names for arguments meant for BufferAudioSource
        # and PyAudioSource
        if "frames_per_buffer" in kwargs or "fpb" in kwargs:
            kwargs["frames_per_buffer"] = kwargs.pop(
                "frames_per_buffer", None
            ) or kwargs.pop("fpb", None)

        if "sampling_rate" in kwargs or "sr" in kwargs:
            kwargs["sampling_rate"] = kwargs.pop(
                "sampling_rate", None
            ) or kwargs.pop("sr", None)

        if "sample_width" in kwargs or "sw" in kwargs:
            kwargs["sample_width"] = kwargs.pop(
                "sample_width", None
            ) or kwargs.pop("sw", None)

        if "channels" in kwargs or "ch" in kwargs:
            kwargs["channels"] = kwargs.pop("channels", None) or kwargs.pop(
                "ch", None
            )

    @staticmethod
    def ads(**kwargs):
        """
        Create an return an :class:`ADSFactory.AudioDataSource`. The type and
        behavior of the object is the result
        of the supplied parameters.

        :Parameters:

        *No parameters* :
           read audio data from the available built-in microphone with the
           default parameters. The returned :class:`ADSFactory.AudioDataSource`
           encapsulate an :class:`io.PyAudioSource` object and hence it accepts
           the next four parameters are passed to use instead of their default
           values.

        `sampling_rate`, `sr` : *(int)*
            number of samples per second. Default = 16000.

        `sample_width`, `sw` : *(int)*
            number of bytes per sample (must be in (1, 2, 4)). Default = 2

        `channels`, `ch` : *(int)*
            number of audio channels. Default = 1 (only this value is currently
            accepted)

        `frames_per_buffer`, `fpb` : *(int)*
            number of samples of PyAudio buffer. Default = 1024.

        `audio_source`, `asrc` : an `AudioSource` object
            read data from this audio source

        `filename`, `fn` : *(string)*
            build an `io.AudioSource` object using this file (currently only
            wave format is supported)

        `data_buffer`, `db` : *(string)*
            build an `io.BufferAudioSource` using data in `data_buffer`.
            If this keyword is used,
            `sampling_rate`, `sample_width` and `channels` are passed to
            `io.BufferAudioSource` constructor and used instead of default
            values.

        `max_time`, `mt` : *(float)*
            maximum time (in seconds) to read. Default behavior: read until
            there is no more data
            available.

        `record`, `rec` : *(bool)*
            save all read data in cache. Provide a navigable object which has a
            `rewind` method.
            Default = False.

        `block_dur`, `bd` : *(float)*
            processing block duration in seconds. This represents the quantity
            of audio data to return each time the :func:`read` method is
            invoked. If `block_dur` is 0.025 (i.e. 25 ms) and the sampling rate
            is 8000 and the sample width is 2 bytes, :func:`read` returns a
            buffer of 0.025 * 8000 * 2 = 400 bytes at most. This parameter will
            be looked for (and used if available) before `block_size`. If
            neither parameter is given, `block_dur` will be set to 0.01 second
            (i.e. 10 ms)

        `hop_dur`, `hd` : *(float)*
            quantity of data to skip from current processing window. if
            `hop_dur` is supplied then there will be an overlap of `block_dur`
            - `hop_dur` between two adjacent blocks. This parameter will be
            looked for (and used if available) before `hop_size`.
            If neither parameter is given, `hop_dur` will be set to `block_dur`
            which means that there will be no overlap between two consecutively
            read blocks.

        `block_size`, `bs` : *(int)*
            number of samples to read each time the `read` method is called.
            Default: a block size that represents a window of 10ms, so for a
            sampling rate of 16000, the default `block_size` is 160 samples,
            for a rate of 44100, `block_size` = 441 samples, etc.

        `hop_size`, `hs` : *(int)*
            determines the number of overlapping samples between two adjacent
            read windows. For a `hop_size` of value *N*, the overlap is
            `block_size` - *N*. Default : `hop_size` = `block_size`, means that
            there is no overlap.

        :Returns:

        An AudioDataSource object that has the desired features.

        :Exampels:

        1. **Create an AudioDataSource that reads data from the microphone
        (requires Pyaudio) with default audio parameters:**

        .. code:: python

            from auditok import ADSFactory
            ads = ADSFactory.ads()
            ads.get_sampling_rate()
            16000
            ads.get_sample_width()
            2
            ads.get_channels()
            1

        2. **Create an AudioDataSource that reads data from the microphone with
        a sampling rate of 48KHz:**

        .. code:: python

            from auditok import ADSFactory
            ads = ADSFactory.ads(sr=48000)
            ads.get_sampling_rate()
            48000

        3. **Create an AudioDataSource that reads data from a wave file:**

        .. code:: python

            from auditok import ADSFactory
            from auditok import dataset
            file = dataset.was_der_mensch_saet_mono_44100_lead_trail_silence
            ads = ADSFactory.ads(fn=file)
            ads.get_sampling_rate()
            44100
            ads.get_sample_width()
            2
            ads.get_channels()
            1

        4. **Define size of read blocks as 20 ms**

        .. code:: python

            from auditok import ADSFactory
            from auditok import dataset
            file = dataset.was_der_mensch_saet_mono_44100_lead_trail_silence
            #we know samling rate for previous file is 44100 samples/second
            #so 10 ms are equivalent to 441 samples and 20 ms to 882
            block_size = 882
            ads = ADSFactory.ads(bs=882, fn=file)
            ads.open()
            # read one block
            data = ads.read()
            ads.close()
            len(data)
            1764
            assert len(data) ==  ads.get_sample_width() * block_size

        5. **Define block size as a duration (use block_dur or bd):**

        .. code:: python

            from auditok import ADSFactory
            from auditok import dataset
            file = dataset.was_der_mensch_saet_mono_44100_lead_trail_silence
            dur = 0.25 # second
            ads = ADSFactory.ads(bd=dur, fn=file)

            # we know samling rate for previous file is 44100 samples/second
            # for a block duration of 250 ms, block size should be
            # 0.25 * 44100 = 11025
            ads.get_block_size()
            11025
            assert ads.get_block_size() ==  int(0.25 * 44100)
            ads.open()
            # read one block
            data = ads.read()
            ads.close()
            len(data)
            22050
            assert len(data) ==  ads.get_sample_width() * ads.get_block_size()

        6. **Read overlapping blocks (when one of hope_size, hs, hop_dur or hd
            is > 0):**

        For a better readability we'd use :class:`auditok.io.BufferAudioSource`
        with a string buffer:

        .. code:: python

            from auditok import ADSFactory
            '''
            we supply a data beffer instead of a file (keyword 'bata_buffer' or
            'db')
            sr : sampling rate = 16 samples/sec
            sw : sample width = 1 byte
            ch : channels = 1
            '''
            buffer = "abcdefghijklmnop" # 16 bytes = 1 second of data
            bd = 0.250 # block duration = 250 ms = 4 bytes
            hd = 0.125 # hop duration = 125 ms = 2 bytes
            ads = ADSFactory.ads(db="abcdefghijklmnop",
                                 bd=bd,
                                 hd=hd,
                                 sr=16,
                                 sw=1,
                                 ch=1)
            ads.open()
            ads.read()
            'abcd'
            ads.read()
            'cdef'
            ads.read()
            'efgh'
            ads.read()
            'ghij'
            data = ads.read()
            assert data == 'ijkl'

        7. **Limit amount of read data (use max_time or mt):**

        .. code:: python

            '''
            We know audio file is larger than 2.25 seconds
            We want to read up to 2.25 seconds of audio data
            '''
            from auditok import dataset
            from auditok import ADSFactory
            file = dataset.was_der_mensch_saet_mono_44100_lead_trail_silence
            ads = ADSFactory.ads(mt=2.25, fn=file)
            ads.open()
            data = []
            while True:
                d = ads.read()
                if d is None:
                    break
                data.append(d)

            ads.close()
            data = b''.join(data)
            assert len(data) == int(ads.get_sampling_rate() *
                                 2.25 * ads.get_sample_width() *
                                 ads.get_channels())
        """
        warnings.warn(
            "'ADSFactory' is deprecated and will be removed in a future "
            "release. Please use AudioReader(...) instead.",
            DeprecationWarning,
        )

        # check and normalize keyword arguments
        ADSFactory._check_normalize_args(kwargs)

        block_dur = kwargs.pop("bd")
        hop_dur = kwargs.pop("hd")
        block_size = kwargs.pop("bs")
        hop_size = kwargs.pop("hs")
        max_time = kwargs.pop("mt")
        audio_source = kwargs.pop("asrc")
        filename = kwargs.pop("fn")
        data_buffer = kwargs.pop("db")
        record = kwargs.pop("rec")

        # Case 1: an audio source is supplied
        if audio_source is not None:
            if (filename, data_buffer) != (None, None):
                raise Warning(
                    "You should provide one of 'audio_source', 'filename' or \
                    'data_buffer' keyword parameters. 'audio_source' will be \
                    used"
                )

        # Case 2: a file name is supplied
        elif filename is not None:
            if data_buffer is not None:
                raise Warning(
                    "You should provide one of 'filename' or 'data_buffer'\
                 keyword parameters. 'filename' will be used"
                )
            audio_source = from_file(filename)

        # Case 3: a data_buffer is supplied
        elif data_buffer is not None:
            audio_source = BufferAudioSource(data=data_buffer, **kwargs)

        # Case 4: try to access native audio input
        else:
            audio_source = PyAudioSource(**kwargs)

        if block_dur is not None:
            if block_size is not None:
                raise DuplicateArgument(
                    "Either 'block_dur' or 'block_size' can be specified, not \
                    both"
                )
        elif block_size is not None:
            block_dur = block_size / audio_source.sr
        else:
            block_dur = 0.01  # 10 ms

        # Read overlapping blocks of data
        if hop_dur is not None:
            if hop_size is not None:
                raise DuplicateArgument(
                    "Either 'hop_dur' or 'hop_size' can be specified, not both"
                )
        elif hop_size is not None:
            hop_dur = hop_size / audio_source.sr

        ads = AudioDataSource(
            audio_source,
            block_dur=block_dur,
            hop_dur=hop_dur,
            record=record,
            max_read=max_time,
        )
        return ads


class _AudioSourceProxy:
    def __init__(self, audio_source):

        self._audio_source = audio_source

    def rewind(self):
        if self.rewindable:
            self._audio_source.rewind()
        else:
            raise AudioIOError("Audio stream is not rewindable")

    def rewindable(self):
        try:
            return self._audio_source.rewindable
        except AttributeError:
            return False

    def is_open(self):
        return self._audio_source.is_open()

    def open(self):
        self._audio_source.open()

    def close(self):
        self._audio_source.close()

    def read(self, size):
        return self._audio_source.read(size)

    @property
    def data(self):
        err_msg = "AudioDataSource is not a recorder, no recorded data can "
        err_msg += "be retrieved"
        raise AttributeError(err_msg)

    def __getattr__(self, name):
        return getattr(self._audio_source, name)


class _Recorder(_AudioSourceProxy):
    """
    A class for AudioSource objects that can record all audio data they read,
    with a rewind facility.
    """

    def __init__(self, audio_source):
        super(_Recorder, self).__init__(audio_source)
        self._cache = []
        self._read_block = self._read_and_cache
        self._read_from_cache = False
        self._data = None

    def read(self, size):
        return self._read_block(size)

    @property
    def data(self):
        if self._data is None:
            err_msg = "Unrewinded recorder. Call rewind before accessing "
            err_msg += "recorded data"
            raise RuntimeError(err_msg)
        return self._data

    def rewindable(self):
        return True

    def rewind(self):
        if self._read_from_cache:
            self._audio_source.rewind()
        else:
            self._data = b"".join(self._cache)
            self._cache = None
            self._audio_source = BufferAudioSource(
                self._data, self.sr, self.sw, self.ch
            )
            self._read_block = self._audio_source.read
            self.open()
            self._read_from_cache = True

    def _read_and_cache(self, size):
        # Read and save read data
        block = self._audio_source.read(size)
        if block is not None:
            self._cache.append(block)
        return block


class _Limiter(_AudioSourceProxy):
    """
    A class for AudioDataSource objects that can read a fixed amount of data.
    This can be useful when reading data from the microphone or from large
    audio files.
    """

    def __init__(self, audio_source, max_read):
        super(_Limiter, self).__init__(audio_source)
        self._max_read = max_read
        self._max_samples = round(max_read * self.sr)
        self._bytes_per_sample = self.sw * self.ch
        self._read_samples = 0

    @property
    def data(self):
        data = self._audio_source.data
        max_read_bytes = self._max_samples * self._bytes_per_sample
        return data[:max_read_bytes]

    @property
    def max_read(self):
        return self._max_read

    def read(self, size):
        size = min(self._max_samples - self._read_samples, size)
        if size <= 0:
            return None
        block = self._audio_source.read(size)
        if block is None:
            return None
        self._read_samples += len(block) // self._bytes_per_sample
        return block

    def rewind(self):
        super(_Limiter, self).rewind()
        self._read_samples = 0


class _FixedSizeAudioReader(_AudioSourceProxy):
    def __init__(self, audio_source, block_dur):
        super(_FixedSizeAudioReader, self).__init__(audio_source)

        if block_dur <= 0:
            raise ValueError(
                "block_dur must be > 0, given: {}".format(block_dur)
            )

        self._block_size = int(block_dur * self.sr)
        if self._block_size == 0:
            err_msg = "Too small block_dur ({0:f}) for sampling rate ({1}). "
            err_msg += "block_dur should cover at least one sample "
            err_msg += "(i.e. 1/{1})"
            raise TooSamllBlockDuration(
                err_msg.format(block_dur, self.sr), block_dur, self.sr
            )

    def read(self):
        return self._audio_source.read(self._block_size)

    @property
    def block_size(self):
        return self._block_size

    @property
    def block_dur(self):
        return self._block_size / self.sr

    def __getattr__(self, name):
        return getattr(self._audio_source, name)


class _OverlapAudioReader(_FixedSizeAudioReader):
    """
    A class for AudioDataSource objects that can read and return overlapping
    audio frames
    """

    def __init__(self, audio_source, block_dur, hop_dur):

        if hop_dur >= block_dur:
            raise ValueError('"hop_dur" should be < "block_dur"')

        super(_OverlapAudioReader, self).__init__(audio_source, block_dur)

        self._hop_size = int(hop_dur * self.sr)
        self._blocks = self._iter_blocks_with_overlap()

    def _iter_blocks_with_overlap(self):
        while not self.is_open():
            yield AudioIOError
        block = self._audio_source.read(self._block_size)
        if block is None:
            yield None

        _hop_size_bytes = (
            self._hop_size * self._audio_source.sw * self._audio_source.ch
        )
        cache = block[_hop_size_bytes:]
        yield block

        while True:
            block = self._audio_source.read(self._hop_size)
            if block:
                block = cache + block
                cache = block[_hop_size_bytes:]
                yield block
                continue
            yield None

    def read(self):
        try:
            block = next(self._blocks)
            if block == AudioIOError:
                raise AudioIOError("Audio Stream is not open.")
            return block
        except StopIteration:
            return None

    def rewind(self):
        super(_OverlapAudioReader, self).rewind()
        self._blocks = self._iter_blocks_with_overlap()

    @property
    def hop_size(self):
        return self._hop_size

    @property
    def hop_dur(self):
        return self._hop_size / self.sr

    def __getattr__(self, name):
        return getattr(self._audio_source, name)


class AudioReader(DataSource):
    """
    Base class for AudioReader objects.
    It inherits from DataSource and encapsulates an AudioSource object.
    """

    def __init__(
        self,
        input,
        block_dur=0.01,
        hop_dur=None,
        record=False,
        max_read=None,
        **kwargs
    ):
        if not isinstance(input, AudioSource):
            input = get_audio_source(input, **kwargs)
        self._record = record
        if record:
            input = _Recorder(input)
        if max_read is not None:
            input = _Limiter(input, max_read)
            self._max_read = max_read
        if hop_dur is not None:
            input = _OverlapAudioReader(input, block_dur, hop_dur)
        else:
            input = _FixedSizeAudioReader(input, block_dur)
        self._audio_source = input

    def __repr__(self):
        block_dur, hop_dur, max_read = None, None, None
        if self.block_dur is not None:
            block_dur = "{:.3f}".format(self.block_dur)
        if self.hop_dur is not None:
            hop_dur = "{:.3f}".format(self.hop_dur)
        if self.max_read is not None:
            max_read = "{:.3f}".format(self.max_read)
        return (
            "{cls}(block_dur={block_dur}, "
            "hop_dur={hop_dur}, record={rewindable}, "
            "max_read={max_read})"
        ).format(
            cls=self.__class__.__name__,
            block_dur=block_dur,
            hop_dur=hop_dur,
            rewindable=self._record,
            max_read=max_read,
        )

    @property
    def rewindable(self):
        return self._record

    @property
    def block_dur(self):
        return self._audio_source.block_size / self._audio_source.sr

    @property
    def hop_dur(self):
        if hasattr(self._audio_source, "hop_dur"):
            return self._audio_source.hop_size / self._audio_source.sr
        return self.block_dur

    @property
    def hop_size(self):
        if hasattr(self._audio_source, "hop_size"):
            return self._audio_source.hop_size
        return self.block_size

    @property
    def max_read(self):
        try:
            return self._audio_source.max_read
        except AttributeError:
            return None

    def read(self):
        return self._audio_source.read()

    def __getattr__(self, name):
        if name in ("data", "rewind") and not self.rewindable:
            raise AttributeError(
                "'AudioReader' has no attribute '{}'".format(name)
            )
        try:
            return getattr(self._audio_source, name)
        except AttributeError:
            raise AttributeError(
                "'AudioReader' has no attribute '{}'".format(name)
            )


# Keep AudioDataSource for compatibility
# Remove in a future version when ADSFactory is dropped
AudioDataSource = AudioReader


class Recorder(AudioReader):
    def __init__(
        self, input, block_dur=0.01, hop_dur=None, max_read=None, **kwargs
    ):
        super().__init__(
            input,
            block_dur=block_dur,
            hop_dur=hop_dur,
            record=True,
            max_read=max_read,
            **kwargs
        )
