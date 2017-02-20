from abc import abstractmethod, abstractproperty, ABCMeta
from collections import namedtuple

ASCENDING = 1
DESCENDING = -1

OrderSpecifier = namedtuple("OrderSpecifier", ['field', 'direction'])


class Log(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_entry(self, time, loggername, levelname, objname,
                     objpk=None, message="", metadata=None):
        """
        Create a log entry.

        :param time: The time of creation for the entry
        :type time: :class:`datetime.datetime`
        :param loggername: The name of the logger that generated the entry
        :type loggername: basestring
        :param levelname: The log level
        :type levelname: basestring
        :param objname: The object name (if any) that emitted the entry
        :type objname: basestring
        :param objpk: The object id that emitted the entry
        :type objpk: int
        :param message: The message to log
        :type message: basestring
        :param metadata: Any (optional) metadata, should be JSON serializable dictionary
        :type metadata: :class:`dict`
        :return: An object implementing the log entry interface
        :rtype: :class:`aiida.orm.log.LogEntry`
        """
        pass

    @abstractmethod
    def create_entry_from_record(self, record):
        """
        Create a log entry from a record created by the python logging

        :param record: The record created by the logging module
        :type record: :class:`logging.record`
        :return: An object implementing the log entry interface
        :rtype: :class:`aiida.orm.log.LogEntry`
        """
        pass

    @abstractmethod
    def find(self, filter_by=None, order_by=None, limit=None):
        """
        Find all entries in the Log collection that confirm to the filter and
        optionally sort and/or apply a limit.

        :param filter_by: A dictionary of key value pairs where the entries have
            to match all the criteria (i.e. an AND operation)
        :type filter_by: :class:`dict`
        :param order_by: A list of tuples of type :class:`OrderSpecifier`
        :type order_by: list
        :param limit: The number of entries to retrieve
        :return: An iterable of the matching entries
        """
        pass


class LogEntry(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def id(self):
        """
        Get the primary key of the entry

        :return: The entry primary key
        :rtype: int
        """
        pass

    @abstractproperty
    def time(self):
        """
        Get the time corresponding to the entry

        :return: The entry timestamp
        :rtype: :class:`datetime.datetime`
        """
        pass

    @abstractproperty
    def loggername(self):
        """
        The name of the logger that created this entry

        :return: The entry loggername
        :rtype: basestring
        """
        pass

    @abstractproperty
    def levelname(self):
        """
        The name of the log level

        :return: The entry log level name
        :rtype: basestring
        """
        pass

    @abstractproperty
    def objpk(self):
        """
        Get the id of the object that created the log entry

        :return: The entry timestamp
        :rtype: int
        """
        pass

    @abstractproperty
    def objname(self):
        """
        Get the name of the object that created the log entry

        :return: The entry object name
        :rtype: basestring
        """
        pass

    @abstractproperty
    def message(self):
        """
        Get the message corresponding to the entry

        :return: The entry message
        :rtype: basestring
        """
        pass

    @abstractproperty
    def metadata(self):
        """
        Get the metadata corresponding to the entry

        :return: The entry metadata
        :rtype: json
        """
        pass

    @abstractmethod
    def persist(self):
        """
        Persist the log entry to the database

        :return: reference of self
        :rtype: :class: LogEntry
        """
        pass