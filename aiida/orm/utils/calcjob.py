# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""Utilities to operate on `CalcJobNode` instances."""

from aiida.common import exceptions

__all__ = ('CalcJobResultManager',)


class CalcJobResultManager:
    """
    Utility class to easily access the contents of the 'default output' node of a `CalcJobNode`.

    A `CalcJob` process can mark one of its outputs as the 'default output'. The default output node will always be
    returned by the `CalcJob` and will always be a `Dict` node.

    If a `CalcJob` defines such a default output node, this utility class will simplify retrieving the result of said
    node through the `CalcJobNode` instance produced by the execution of the `CalcJob`.

    The default results are only defined if the `CalcJobNode` has a `process_type` that can be successfully used
    to load the corresponding `CalcJob` process class *and* if its process spec defines a `default_output_node`.
    If both these conditions are met, the results are defined as the dictionary contained within the default
    output node.
    """

    def __init__(self, node):
        """Construct an instance of the `CalcJobResultManager`.

        :param calc: the `CalcJobNode` instance.
        """
        self._node = node
        self._result_node = None
        self._results = None

    @property
    def node(self):
        """Return the `CalcJobNode` associated with this result manager instance."""
        return self._node

    def _load_results(self):
        """Try to load the results for the `CalcJobNode` of this result manager.

        :raises ValueError: if no default output node could be loaded
        """
        try:
            process_class = self._node.process_class
        except ValueError as exception:
            raise ValueError(f'cannot load results because process class cannot be loaded: {exception}')

        process_spec = process_class.spec()
        default_output_node_label = process_spec.default_output_node

        if default_output_node_label is None:
            raise ValueError(f'cannot load results as {process_class} does not specify a default output node')

        try:
            default_output_node = self.node.base.links.get_outgoing().get_node_by_label(default_output_node_label)
        except exceptions.NotExistent as exception:
            raise ValueError(f'cannot load results as the default node could not be retrieved: {exception}')

        self._result_node = default_output_node
        self._results = default_output_node.get_dict()

    def get_results(self):
        """Return the results dictionary of the default results node of the calculation node.

        This property will lazily load the dictionary.

        :return: the dictionary of the default result node
        """
        if self._results is None:
            self._load_results()
        return self._results

    def __dir__(self):
        """Add the keys of the results dictionary such that they can be autocompleted."""
        return sorted(list(self.get_results().keys()))

    def __iter__(self):
        """Return an iterator over the keys of the result dictionary."""
        for key in self.get_results().keys():
            yield key

    def __getattr__(self, name):
        """Return an attribute from the results dictionary.

        :param name: name of the result return
        :return: value of the attribute
        :raises AttributeError: if the results node cannot be retrieved or it does not contain the `name` attribute
        """
        try:
            return self.get_results()[name]
        except ValueError as exception:
            raise AttributeError from exception
        except KeyError:
            raise AttributeError(f"Default result node<{self._result_node.pk}> does not contain key '{name}'")

    def __getitem__(self, name):
        """Return an attribute from the results dictionary.

        :param name: name of the result return
        :return: value of the attribute
        :raises KeyError: if the results node cannot be retrieved or it does not contain the `name` attribute
        """
        try:
            return self.get_results()[name]
        except ValueError as exception:
            raise KeyError from exception
        except KeyError:
            raise KeyError(f"Default result node<{self._result_node.pk}> does not contain key '{name}'")
