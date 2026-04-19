# Test Cases — Restful-Booker API

## Legend

| Priority | Meaning |
|----------|---------|
| P0 | Critical — must pass for release |
| P1 | High — important functional coverage |
| P2 | Medium — edge/boundary/security cases |

---

## TC-01: Generate Auth Token with Valid Credentials

| Field | Value |
|-------|-------|
| **ID** | TC-01 |
| **Priority** | P0 |
| **Type** | Positive |
| **Endpoint** | `POST /auth` |
| **Preconditions** | None |
| **Input** | `{ "username": "admin", "password": "password123" }` |
| **Expected Result** | Status `200`; response body contains `token` (non-empty string) |

---

## TC-02: Auth Token Rejected for Invalid Credentials

| Field | Value |
|-------|-------|
| **ID** | TC-02 |
| **Priority** | P0 |
| **Type** | Negative |
| **Endpoint** | `POST /auth` |
| **Preconditions** | None |
| **Input** | `{ "username": "admin", "password": "wrong" }` |
| **Expected Result** | Status `200`; response body contains `reason: "Bad credentials"` (no token issued) |

---

## TC-03: Auth with Missing Fields

| Field | Value |
|-------|-------|
| **ID** | TC-03 |
| **Priority** | P1 |
| **Type** | Negative |
| **Endpoint** | `POST /auth` |
| **Preconditions** | None |
| **Input** | `{}` (empty body) |
| **Expected Result** | No token issued; response contains `reason: "Bad credentials"` |

---

## TC-04: Create Booking with Valid Data

| Field | Value |
|-------|-------|
| **ID** | TC-04 |
| **Priority** | P0 |
| **Type** | Positive |
| **Endpoint** | `POST /booking` |
| **Preconditions** | None |
| **Input** | Valid booking JSON with all required fields |
| **Expected Result** | Status `200`; response contains `bookingid` (integer) and `booking` object matching input |

---

## TC-05: Create Booking — Missing Required Fields

| Field | Value |
|-------|-------|
| **ID** | TC-05 |
| **Priority** | P1 |
| **Type** | Negative |
| **Endpoint** | `POST /booking` |
| **Preconditions** | None |
| **Input** | Booking JSON with `firstname` omitted |
| **Expected Result** | Status `500` or `400`; booking is not created |

---

## TC-06: Create Booking — Invalid Data Types

| Field | Value |
|-------|-------|
| **ID** | TC-06 |
| **Priority** | P1 |
| **Type** | Negative |
| **Endpoint** | `POST /booking` |
| **Preconditions** | None |
| **Input** | `totalprice` as string `"abc"`, `depositpaid` as string `"yes"` |
| **Expected Result** | Status `500` or `400`; booking is not created or values are rejected |

---

## TC-07: Create Booking — Boundary Values (Zero / Negative Price)

| Field | Value |
|-------|-------|
| **ID** | TC-07 |
| **Priority** | P2 |
| **Type** | Boundary |
| **Endpoint** | `POST /booking` |
| **Preconditions** | None |
| **Input** | `totalprice: 0` and separately `totalprice: -1` |
| **Expected Result** | Zero price booking may succeed; negative price should be rejected or handled gracefully |

---

## TC-08: Get All Booking IDs

| Field | Value |
|-------|-------|
| **ID** | TC-08 |
| **Priority** | P0 |
| **Type** | Positive |
| **Endpoint** | `GET /booking` |
| **Preconditions** | At least one booking exists |
| **Input** | None |
| **Expected Result** | Status `200`; response is a JSON array of objects each containing `bookingid` |

---

## TC-09: Get Booking by Valid ID

| Field | Value |
|-------|-------|
| **ID** | TC-09 |
| **Priority** | P0 |
| **Type** | Positive |
| **Endpoint** | `GET /booking/{id}` |
| **Preconditions** | Create a booking first |
| **Input** | Valid booking ID from precondition |
| **Expected Result** | Status `200`; response body matches the created booking data |

---

## TC-10: Get Booking by Non-existent ID

| Field | Value |
|-------|-------|
| **ID** | TC-10 |
| **Priority** | P1 |
| **Type** | Negative |
| **Endpoint** | `GET /booking/{id}` |
| **Preconditions** | None |
| **Input** | ID `9999999` (unlikely to exist) |
| **Expected Result** | Status `404`; appropriate error response |

---

## TC-11: Filter Bookings by Name

| Field | Value |
|-------|-------|
| **ID** | TC-11 |
| **Priority** | P1 |
| **Type** | Positive |
| **Endpoint** | `GET /booking?firstname=X&lastname=Y` |
| **Preconditions** | Create a booking with known name |
| **Input** | Query params matching the created booking |
| **Expected Result** | Status `200`; returned list includes the created booking ID |

---

## TC-12: Full Update Booking with Auth

| Field | Value |
|-------|-------|
| **ID** | TC-12 |
| **Priority** | P0 |
| **Type** | Positive |
| **Endpoint** | `PUT /booking/{id}` |
| **Preconditions** | Valid auth token; existing booking |
| **Input** | Complete updated booking JSON |
| **Expected Result** | Status `200`; response body reflects all updated fields |

---

## TC-13: Full Update Booking Without Auth (Unauthorized)

| Field | Value |
|-------|-------|
| **ID** | TC-13 |
| **Priority** | P0 |
| **Type** | Security |
| **Endpoint** | `PUT /booking/{id}` |
| **Preconditions** | Existing booking; no auth token |
| **Input** | Updated booking JSON, no Cookie/Authorization header |
| **Expected Result** | Status `403`; booking is NOT updated |

---

## TC-14: Partial Update Booking (PATCH)

| Field | Value |
|-------|-------|
| **ID** | TC-14 |
| **Priority** | P1 |
| **Type** | Positive |
| **Endpoint** | `PATCH /booking/{id}` |
| **Preconditions** | Valid auth token; existing booking |
| **Input** | `{ "firstname": "UpdatedName" }` |
| **Expected Result** | Status `200`; `firstname` updated, other fields unchanged |

---

## TC-15: Partial Update Without Auth

| Field | Value |
|-------|-------|
| **ID** | TC-15 |
| **Priority** | P1 |
| **Type** | Security |
| **Endpoint** | `PATCH /booking/{id}` |
| **Preconditions** | Existing booking; no auth token |
| **Input** | `{ "firstname": "Hacker" }` |
| **Expected Result** | Status `403`; booking is NOT modified |

---

## TC-16: Delete Booking with Auth

| Field | Value |
|-------|-------|
| **ID** | TC-16 |
| **Priority** | P0 |
| **Type** | Positive |
| **Endpoint** | `DELETE /booking/{id}` |
| **Preconditions** | Valid auth token; existing booking |
| **Input** | Booking ID |
| **Expected Result** | Status `201`; subsequent GET returns `404` |

---

## TC-17: Delete Booking Without Auth

| Field | Value |
|-------|-------|
| **ID** | TC-17 |
| **Priority** | P0 |
| **Type** | Security |
| **Endpoint** | `DELETE /booking/{id}` |
| **Preconditions** | Existing booking; no auth token |
| **Input** | Booking ID |
| **Expected Result** | Status `403`; booking still exists |

---

## TC-18: Delete Non-existent Booking

| Field | Value |
|-------|-------|
| **ID** | TC-18 |
| **Priority** | P2 |
| **Type** | Negative |
| **Endpoint** | `DELETE /booking/{id}` |
| **Preconditions** | Valid auth token |
| **Input** | ID `9999999` |
| **Expected Result** | Status `405` or `404`; graceful error handling |

---

## TC-19: Create Booking — Checkout Before Checkin Date

| Field | Value |
|-------|-------|
| **ID** | TC-19 |
| **Priority** | P2 |
| **Type** | Edge |
| **Endpoint** | `POST /booking` |
| **Preconditions** | None |
| **Input** | `checkin: "2025-12-01"`, `checkout: "2025-11-01"` |
| **Expected Result** | API should reject or handle gracefully (may still accept — document observed behaviour) |

---

## TC-20: Create Booking — Very Large Total Price

| Field | Value |
|-------|-------|
| **ID** | TC-20 |
| **Priority** | P2 |
| **Type** | Boundary |
| **Endpoint** | `POST /booking` |
| **Preconditions** | None |
| **Input** | `totalprice: 999999999` |
| **Expected Result** | Booking is created or gracefully rejected; no server crash |
