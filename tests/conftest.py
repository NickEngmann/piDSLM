"""Auto-generated conftest.py -- mocks Raspberry Pi hardware modules.

Provides:
- 15+ RPi hardware modules pre-mocked (RPi.GPIO with realistic constants, guizero, etc.)
- source_module fixture: loads repo .py files with while-True loops stripped via AST
- All other module-level init code runs safely against mocks
"""
import sys
import os
import ast
import types
import glob as _glob
from unittest.mock import MagicMock
import pytest

# --- Mock ALL RPi hardware modules ---
_RPI_MODULES = [
    'RPi', 'RPi.GPIO', 'spidev', 'smbus', 'smbus2',
    'guizero', 'guizero.app', 'guizero.widgets',
    'picamera', 'picamera2',
    'gpiozero', 'gpiozero.pins', 'gpiozero.pins.mock',
    'board', 'digitalio', 'busio', 'adafruit_dht',
    'w1thermsensor', 'Adafruit_DHT',
    'RPIO', 'pigpio', 'wiringpi',
    'sense_hat', 'luma.core', 'luma.oled', 'luma.led_matrix',
    'serial',
]

for _mod in _RPI_MODULES:
    sys.modules[_mod] = MagicMock()

# Import hook: auto-mock ANY unknown hardware module during source file loading
# This catches custom libraries like mp2624, adafruit_* variants, etc.
# Uses find_spec (Python 3.4+) since find_module is deprecated and ignored in Python 3.12
import importlib.abc
import importlib.machinery

class _AutoMockFinder(importlib.abc.MetaPathFinder):
    """Meta-path finder that auto-mocks missing modules instead of raising ImportError."""
    _BUILTIN_SKIP = {
        'os', 'sys', 'json', 'time', 'datetime', 'math', 're', 'pathlib',
        'subprocess', 'shutil', 'collections', 'functools', 'itertools',
        'logging', 'typing', 'dataclasses', 'enum', 'copy', 'io',
        'threading', 'multiprocessing', 'socket', 'http', 'urllib',
        'hashlib', 'base64', 'struct', 'array', 'configparser', 'argparse',
        'unittest', 'pytest', 'glob', 'fnmatch', 'csv', 'string',
    }
    _active = False

    def find_spec(self, name, path, target=None):
        if not self._active:
            return None
        top = name.split('.')[0]
        if top in self._BUILTIN_SKIP:
            return None
        if name in sys.modules:
            return None
        # Create a mock module and register it
        mock = MagicMock()
        mock.__name__ = name
        mock.__spec__ = importlib.machinery.ModuleSpec(name, None)
        sys.modules[name] = mock
        return mock.__spec__

_auto_mocker = _AutoMockFinder()
sys.meta_path.insert(0, _auto_mocker)

# Realistic RPi.GPIO constants
_gpio = sys.modules['RPi.GPIO']
_gpio.BCM = 11
_gpio.BOARD = 10
_gpio.OUT = 0
_gpio.IN = 1
_gpio.HIGH = 1
_gpio.LOW = 0
_gpio.PUD_UP = 22
_gpio.PUD_DOWN = 21
_gpio.RISING = 31
_gpio.FALLING = 32
_gpio.BOTH = 33

# Make guizero App work as context manager
_guizero = sys.modules['guizero']
_guizero.App.return_value.__enter__ = MagicMock(return_value=MagicMock())
_guizero.App.return_value.__exit__ = MagicMock(return_value=False)


def _is_while_true(node):
    """Check if an AST node is a while-True/while-1 loop."""
    if not isinstance(node, ast.While):
        return False
    test = node.test
    if isinstance(test, ast.Constant) and test.value in (True, 1):
        return True
    if hasattr(ast, "NameConstant") and isinstance(test, ast.NameConstant) and test.value is True:
        return True
    return False


def _strip_while_true_from_body(body):
    """Recursively strip while-True loops from AST node bodies."""
    new_body = []
    for node in body:
        if _is_while_true(node):
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            node.body = _strip_while_true_from_body(node.body)
        elif isinstance(node, ast.ClassDef):
            node.body = _strip_while_true_from_body(node.body)
        elif isinstance(node, ast.If):
            node.body = _strip_while_true_from_body(node.body)
            if node.orelse:
                node.orelse = _strip_while_true_from_body(node.orelse)
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            node.body = _strip_while_true_from_body(node.body)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            node.body = _strip_while_true_from_body(node.body)
        elif isinstance(node, ast.Try):
            node.body = _strip_while_true_from_body(node.body)
            for handler in node.handlers:
                handler.body = _strip_while_true_from_body(handler.body)
            if node.orelse:
                node.orelse = _strip_while_true_from_body(node.orelse)
            if node.finalbody:
                node.finalbody = _strip_while_true_from_body(node.finalbody)
        new_body.append(node)
    return new_body


def _strip_while_true(source_path):
    """Recursively strip while-True loops from all nesting levels."""
    with open(source_path) as f:
        source = f.read()
    try:
        tree = ast.parse(source)
        tree.body = _strip_while_true_from_body(tree.body)
        ast.fix_missing_locations(tree)
        return compile(tree, source_path, 'exec')
    except SyntaxError:
        return compile(source, source_path, 'exec')


class _SourceProxy:
    """Proxy that forwards attribute writes back to the originating module."""
    def __init__(self):
        object.__setattr__(self, '_modules', [])
        object.__setattr__(self, '_attr_to_mod', {})

    def _add_module(self, mod):
        self._modules.append(mod)
        for attr in dir(mod):
            if not attr.startswith('_'):
                self._attr_to_mod[attr] = mod

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        for mod in reversed(self._modules):
            try:
                return getattr(mod, name)
            except AttributeError:
                continue
        raise AttributeError(f"source_module has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        if name in self._attr_to_mod:
            setattr(self._attr_to_mod[name], name, value)
        elif self._modules:
            setattr(self._modules[0], name, value)

    def __delattr__(self, name):
        if name.startswith('_'):
            object.__delattr__(self, name)
            return
        if name in self._attr_to_mod:
            try:
                delattr(self._attr_to_mod[name], name)
            except AttributeError:
                pass
        elif self._modules:
            try:
                delattr(self._modules[0], name)
            except AttributeError:
                pass

    def __dir__(self):
        return sorted(self._attr_to_mod.keys())


@pytest.fixture
def source_module():
    """Load .py source files from repo with while-True loops stripped.

    All hardware modules are already mocked. Module-level init code runs safely.
    Returns a _SourceProxy that forwards writes back to the actual module globals.

    Usage:
        def test_capture(source_module):
            source_module.capture_image()
    """
    repo_root = ''
    proxy = _SourceProxy()

    search_dirs = [repo_root]
    for subdir in ['src', 'lib']:
        subpath = os.path.join(repo_root, subdir)
        if os.path.isdir(subpath):
            search_dirs.append(subpath)

    for search_dir in search_dirs:
        pattern = os.path.join(search_dir, '**', '*.py') if search_dir != repo_root else os.path.join(search_dir, '*.py')
        for py_file in sorted(_glob.glob(pattern, recursive=True)):
            basename = os.path.basename(py_file)
            if basename.startswith('test_') or basename in ('conftest.py', 'setup.py'):
                continue

            mod_name = os.path.splitext(basename)[0]
            try:
                code_obj = _strip_while_true(py_file)
                mod = types.ModuleType(mod_name)
                mod.__file__ = py_file
                for rm in _RPI_MODULES:
                    short = rm.split('.')[-1]
                    mod.__dict__[short] = sys.modules[rm]
                _auto_mocker._active = True  # Enable catch-all mock for unknown imports
                try:
                    exec(code_obj, mod.__dict__)
                finally:
                    _auto_mocker._active = False
                sys.modules[mod_name] = mod  # Register so @patch('mod_name.x') works

                proxy._add_module(mod)
            except Exception as e:
                _auto_mocker._active = False
                print(f"[conftest] Warning loading {basename}: {e}")
                continue

    return proxy
