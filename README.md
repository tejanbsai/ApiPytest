# Restful-Booker API Test Suite

Automated API tests for the [Restful-Booker](https://restful-booker.herokuapp.com) hotel booking API, covering authentication, CRUD operations, input validation, and security checks.

## Project Structure

```
restful-booker-api-tests/
├── api/                        # API client layer
│   ├── base_client.py          #   Generic REST client (extend for any API)
│   ├── auth_client.py          #   Authentication endpoint client
│   └── booking_client.py       #   Booking CRUD endpoint client
├── config/
│   └── settings.py             # Configuration (URL, credentials, timeouts)
├── models/
│   └── booking.py              # Booking data model (dataclass)
├── tests/
│   ├── conftest.py             # Shared fixtures (clients, tokens, test data)
│   ├── test_auth.py            # Authentication tests (TC-01 to TC-03)
│   ├── test_booking_create.py  # Create booking tests (TC-04 to TC-07, TC-19, TC-20)
│   ├── test_booking_read.py    # Read booking tests (TC-08 to TC-11)
│   ├── test_booking_update.py  # Update booking tests (TC-12 to TC-15)
│   └── test_booking_delete.py  # Delete booking tests (TC-16 to TC-18)
├── utils/
│   └── data_factory.py         # Randomised test data generation
├── docs/
│   ├── TEST_STRATEGY.md        # Phase 1 — Test strategy document
│   └── TEST_CASES.md           # Phase 2 — Documented test cases
├── .github/workflows/
│   └── api-tests.yml           # CI/CD — GitHub Actions pipeline
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Prerequisites

- Python 3.10+
- pip

## Setup and Run

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd restful-booker-api-tests

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run all tests
pytest

# 5. Run with verbose output
pytest -v

# 6. Run a specific test file
pytest tests/test_auth.py

# 7. Run by marker
pytest -m smoke
```

## Configuration

Settings are in `config/settings.py` and can be overridden via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `API_BASE_URL` | `https://restful-booker.herokuapp.com` | API base URL |
| `API_USERNAME` | `admin` | Auth username |
| `API_PASSWORD` | `password123` | Auth password |
| `API_TIMEOUT` | `30` | Request timeout in seconds |

Example:

```bash
API_BASE_URL=https://your-staging-api.com pytest
```

## Test Reports

After running tests, reports are generated in the `reports/` directory:

- **`reports/report.html`** — HTML report (open in browser)
- **`reports/results.xml`** — JUnit XML (for CI integration)

## Extending the Framework

### Adding a new API resource

1. Create a new client in `api/` extending `BaseClient`
2. Add a data model in `models/`
3. Add a factory method in `utils/data_factory.py`
4. Create test file in `tests/`
5. Add shared fixtures in `tests/conftest.py`

### Pointing at a different environment

Set the `API_BASE_URL` environment variable — no code changes needed.

## CI/CD

A GitHub Actions workflow is included at `.github/workflows/api-tests.yml`. It runs automatically on push and PR to `main`, and uploads test reports as artifacts.
