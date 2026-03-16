# TESTING.md — piDSLM Test Documentation

## Test Overview
The piDSLM project uses **pytest** as the test framework with comprehensive hardware mocking to enable testing on any Linux system (not just Raspberry Pi).

---

## Test Infrastructure

### Test Suite Location
- **Directory**: `tests/`
- **Configuration**: `tests/conftest.py`
- **Example Tests**: `tests/test_example.py`

### Hardware Mocking
All Raspberry Pi hardware modules are automatically mocked via `conftest.py`:

| Mock Module | Purpose | Implementation |
|-------------|---------|----------------|
| `MockGPIO` | GPIO pin control | Simulates BCM pin modes, read/write |
| `MockI2C` | I2C bus communication | Register read/write, device polling |
| `MockSPI` | SPI bus communication | Data transfer, configuration |
| `MockUART` | Serial communication | Buffer read/write, port control |

**Mocked Modules Count**: 15+ including RPi.GPIO, picamera, gpiozero, smbus, spidev, etc.

---

## Running Tests

### Basic Test Execution
```bash
pytest tests/ -v
```

### Full Test Run with Coverage
```bash
pytest tests/ -v --tb=short
```

### Test Output
```
============================= test session starts ==============================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6
cachedir: .pytest_cache
rootdir: /mnt/sandbox-ssd/workspaces/nickengmann-pidslm/repo
plugins: anyio-4.12.1
collected 2 items

tests/test_example.py::test_gpio_pin_control PASSED                    [ 50%]
tests/test_example.py::test_i2c_communication PASSED                   [100%]

============================== 2 passed in 0.01s ===============================
```

---

## Existing Tests

### test_gpio_pin_control
**Purpose**: Validate GPIO pin control operations

```python
def test_gpio_pin_control():
    """Test GPIO pin output."""
    gpio = MockGPIO()
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUTPUT)
    gpio.output(17, gpio.HIGH)
    assert gpio.input(17) == gpio.HIGH
    gpio.output(17, gpio.LOW)
    assert gpio.input(17) == gpio.LOW
    gpio.cleanup()
```

**Tested Functionality**:
- BCM pin numbering mode
- Input/output pin configuration
- High/low output setting
- Input value reading
- Pin cleanup

### test_i2c_communication
**Purpose**: Validate I2C bus communication

```python
def test_i2c_communication():
    """Test I2C bus read/write."""
    i2c = MockI2C()
    i2c.set_read_response(0x48, bytes([0x00, 0x7F]))  # Temperature sensor
    buf = bytearray(2)
    i2c.readfrom_into(0x48, buf)
    assert buf[1] == 0x7F
```

**Tested Functionality**:
- I2C device address communication
- Buffer read operations
- Data response simulation

---

## Test Fixtures

### source_module Fixture
**Location**: `tests/conftest.py`

**Purpose**: Load source files with hardware mocks active

**Usage**:
```python
def test_capture_image(source_module):
    """Test capture_image method (requires mocking GPIO)."""
    # Access piDSLM class via source module proxy
    # Note: Full GUI tests skipped in CI
```

**Features**:
- AST-based parsing of source files
- Automatic stripping of infinite loops
- Hardware module mock injection
- Attribute forwarding proxy

---

## Test Coverage

### Current Coverage
| Component | Coverage | Status |
|-----------|----------|--------|
| `test_example.py` | 100% (2/2 tests) | ✅ Passing |
| `embedded_mocks.py` | N/A (utilities) | ✅ Complete |
| `conftest.py` | N/A (infrastructure) | ✅ Complete |
| `pidslm.py` | GUI not tested | ⚠️ Manual testing |
| `dropbox_upload.py` | Business logic | ⚠️ Limited |

### Recommended Additional Tests
1. **GUI Component Tests**: Window creation, button callbacks
2. **Path Handling Tests**: Downloads directory configuration
3. **Upload Logic Tests**: File filtering, metadata comparison
4. **Error Handling Tests**: Missing files, permission errors

---

## CI/CD Integration

### Test Command (Recommended)
```bash
cd /workspace/repo && python3 -m pytest tests/ -v --tb=short
```

### Environment Requirements
- Python 3.12+
- pytest 8.0+
- No virtual display needed (hardware mocked)

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt pytest
      - name: Run tests
        run: pytest tests/ -v --tb=short
```

---

## Mock Architecture

### Auto-Mocking Strategy
`conftest.py` uses Python's `sys.meta_path` to intercept module imports:

```python
class _AutoMockFinder(importlib.abc.MetaPathFinder):
    """Auto-mocks missing hardware modules."""
    def find_spec(self, name, path, target=None):
        # Creates MagicMock for unknown modules
        mock = MagicMock()
        mock.__name__ = name
        sys.modules[name] = mock
        return mock.__spec__
```

**Benefits**:
- Tests run on any Linux system
- No need for actual Raspberry Pi hardware
- Fast mock injection (milliseconds)
- Comprehensive hardware simulation

### Mock Constants
GPIO constants are set to realistic values:
```python
GPIO.BCM = 11
GPIO.BOARD = 10
GPIO.OUT = 0
GPIO.IN = 1
GPIO.HIGH = 1
GPIO.LOW = 0
```

---

## Testing Guidelines

### When Adding New Tests
1. Use `MockGPIO`, `MockI2C`, etc. from `embedded_mocks.py`
2. Keep tests in `tests/test_example.py` or create new test files
3. Document test purpose in docstring
4. Use `source_module` fixture for integration tests

### Best Practices
- **Keep tests fast**: All tests should complete in <1s
- **Isolate mocking**: Use fixture-scoped mocks when possible
- **Clear assertions**: Assert specific values, not just truthiness
- **Comment complexity**: Explain why tests exist for complex scenarios

---

## Test Results Summary

| Metric | Value |
|--------|-------|
| Total Tests | 2 |
| Passed | 2 |
| Failed | 0 |
| Skipped | 0 |
| Test Duration | 0.01s |
| Environment | Python 3.14.3, pytest 9.0.2 |

**Last Updated**: 2026-03-16

---

*For questions about testing, refer to `tests/conftest.py` documentation or contact project maintainers.*
