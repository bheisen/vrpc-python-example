import unittest
from vrpc import VrpcLocal
import vrpc_example_ext


class MainTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._vrpc = VrpcLocal(vrpc_example_ext)
        cls._bar = cls._vrpc.create('Bar')
        cls._event = None

    def _onEvent(self, event, *args):
        if (event == 'empty'):
            self._event = args[0]

    def test_functions(self):
        msg = self._vrpc.call_static('Bar', 'philosophy')
        self.assertEqual(msg, 'I have mixed drinks about feelings.')
        self.assertFalse(self._bar.hasDrink('rum'))
        self.assertEqual(self._bar.getAssortment(), {})
        bottle = {'brand': 'a', 'country': 'a', 'age': 1}
        self._bar.addBottle('rum', bottle)
        self.assertDictEqual(self._bar.getAssortment(), {'rum': [bottle]})
        self.assertTrue(self._bar.hasDrink('rum'))
        self._bar.onEmptyDrink((self._onEvent, 'empty'))
        self.assertEqual(self._event, None)
        self._bar.removeBottle('rum')
        self.assertEqual(self._event, 'rum')


if __name__ == '__main__':
    unittest.main()
