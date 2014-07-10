# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""
Tests for :module:`flocker.node.script`.
"""

from twisted.trial.unittest import SynchronousTestCase
from twisted.python.usage import UsageError
from yaml import safe_dump
from ...testtools import FlockerScriptTestsMixin, StandardOptionsTestsMixin
from ..script import ChangeStateOptions, ChangeStateScript


class ChangeStateScriptTests(FlockerScriptTestsMixin, SynchronousTestCase):
    """
    Tests for L{ChangeStateScript}.
    """
    script = ChangeStateScript
    options = ChangeStateOptions
    command_name = u'flocker-changestate'


class ChangeStateScriptMainTests(SynchronousTestCase):
    """
    Tests for ``ChangeStateScript.main``.
    """
    script = ChangeStateScript()
    options = ChangeStateOptions()

    def test_deferred_result(self):
        """
        ``ChangeStateScript.main`` returns a ``Deferred`` on success.
        """
        dummy_reactor = object()
        options = self.options
        expected_deployment = {'version': 1, 'nodes': {}}
        expected_application = {'version': 1, 'applications': {}}
        options["deployment_config"] = expected_deployment
        options["app_config"] = expected_application

        d = self.script.main(dummy_reactor, options)

        self.assertEqual(
            {'start': [], 'stop': []},
            self.successResultOf(d)
        )


class ChangeStateOptionsTests(StandardOptionsTestsMixin, SynchronousTestCase):
    """
    Tests for :class:`ChangeStateOptions`.
    """
    options = ChangeStateOptions

    def test_custom_configs(self):
        """
        The supplied configuration strings are saved as ``dict``\ s on the
        options instance.
        """
        options = self.options()
        expected_deployment = {"foo": "bar", "spam": "eggs", "anumber": 14}
        expected_application = {"appfoo": "appbar",
                                "appspam": "appeggs",
                                "appnumber": 17}
        options.parseOptions(
            [safe_dump(expected_deployment), safe_dump(expected_application)])

        self.assertDictContainsSubset(
            {'deployment_config': expected_deployment,
             'app_config': expected_application},
            options
        )

    def test_invalid_deployment_configs(self):
        """
        If the supplied deployment_config is not valid `YAML`, a
        ``UsageError`` is raised.
        """
        options = self.options()
        deployment_bad_yaml = "{'foo':'bar', 'x':y, '':'"
        e = self.assertRaises(
            UsageError, options.parseOptions, [deployment_bad_yaml, b''])

        self.assertTrue(
            str(e).startswith('Deployment config could not be parsed as YAML')
        )

    def test_invalid_application_configs(self):
        """
        If the supplied application_config is not valid `YAML`, a
        ``UsageError`` is raised.
        """
        options = self.options()
        application_bad_yaml = "{'foo':'bar', 'x':y, '':'"
        e = self.assertRaises(
            UsageError, options.parseOptions, [b'', application_bad_yaml])

        self.assertTrue(
            str(e).startswith('Application config could not be parsed as YAML')
        )
