# Test Strategy — Restful-Booker API

## Objective

Validate the Restful-Booker API's core functionality, reliability, and security across authentication, booking CRUD operations, and error handling.

## Scope — What We Chose to Test and Why

### In Scope (High Priority)

| Area | Rationale |
|------|-----------|
| **Authentication (POST /auth)** | Gatekeeper for all write operations; a failure here blocks updates and deletes |
| **Create Booking (POST /booking)** | Core business operation — revenue depends on bookings being created correctly |
| **Read Booking (GET /booking, GET /booking/{id})** | Most frequently called endpoints; must return accurate, consistent data |
| **Update Booking (PUT /booking/{id})** | Full update path — validates auth enforcement and data integrity |
| **Partial Update (PATCH /booking/{id})** | Common real-world pattern; partial updates are prone to field-level bugs |
| **Delete Booking (DELETE /booking/{id})** | Destructive operation — must enforce auth and handle edge cases |
| **Input Validation** | Invalid/missing fields, wrong data types, boundary values — common source of production bugs |
| **Auth Enforcement** | Unauthenticated requests to protected endpoints must be rejected |

### De-prioritised

| Area | Rationale |
|------|-----------|
| **Performance / Load Testing** | Out of scope for functional assessment; live shared environment |
| **Concurrent Booking Conflicts** | Race conditions are infrastructure-level; not testable reliably against shared API |
| **UI / Frontend** | API-only assessment |
| **Exhaustive Field Combinations** | Diminishing returns; covered via representative boundary + negative cases |

## Risks and Assumptions

### Risks

- **Shared environment instability**: The API is publicly hosted — data may be modified by other users between test steps. Mitigation: tests create their own data and clean up; assertions reference self-created resources.
- **No schema contract**: No OpenAPI/Swagger spec is provided. Observed behaviour may differ from intended behaviour. Mitigation: document assumptions; validate response structure in tests.
- **Auth token expiry**: Token lifetime is undocumented. Mitigation: generate a fresh token per test session.

### Assumptions

- The API follows RESTful conventions (appropriate HTTP status codes, JSON request/response bodies).
- `admin` / `password123` are the default credentials (per API docs).
- Booking IDs are integers, auto-incremented.
- Dates are expected in `YYYY-MM-DD` format.
- The `depositpaid` field is boolean.

## Test Data Approach

- **Dynamic generation**: Test data is generated at runtime using a data factory (`utils/data_factory.py`) with randomised names, dates and prices. This avoids collisions in the shared environment.
- **Self-contained tests**: Each test creates its own booking, operates on it, and cleans up where appropriate. No reliance on pre-existing data.
- **Configuration-driven**: Base URL and credentials are stored in `config/settings.py` and can be overridden via environment variables for different environments.

## Test Execution Approach

- **Framework**: Python + pytest + requests
- **Reporting**: pytest-html for HTML reports; JUnit XML for CI integration
- **Parallelisation**: Not used — avoids overwhelming the shared public API
- **CI/CD**: GitHub Actions workflow runs tests on push and PR
