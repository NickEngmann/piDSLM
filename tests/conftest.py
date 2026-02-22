"""Auto-generated conftest.py — mocks Raspberry Pi hardware modules.

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

# ─── Mock ALL RPi hardware modules ───
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


def _strip_while_true(source_path):
    """Strip while-True loops from module level, keep everything else."""
    with open(source_path) as f:
        source = f.read()
    try:
        tree = ast.parse(source)
        new_body = []
        for node in tree.body:
            if isinstance(node, ast.While):
                test = node.test
                if isinstance(test, ast.Constant) and test.value in (True, 1):
                    continue
                if isinstance(test, ast.NameConstant) and test.value is True:
                    continue
            new_body.append(node)
        tree.body = new_body
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
    repo_root = '/workspace/repo'
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
                exec(code_obj, mod.__dict__)
                sys.modules[mod_name] = mod  # Register so @patch('mod_name.x') works

                proxy._add_module(mod)
            except Exception as e:
                print(f"[conftest] Warning loading {basename}: {e}")
                continue

    return proxy
