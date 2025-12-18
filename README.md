# The Patient Centre Interview
This repository contains my interview project for the internship role at The Patient Centre.

---

### Project Structure

```
├── analytics_buffer.py
├── mock_api.py
├── tests/
│   ├── test_analytics_buffer.py
│   └── test_mock_api.py
├── requirements.txt
└── README.md
```
___

### Requirements
* Python 3.9+ <br>
* Unix-based system (Linux or macOS) <br>
* pip and venv <br>

___

### Setup Instructions
1. Clone the repository
```
git clone https://github.com/EmilyEsther1311/the-patient-centre-interview.git
cd the-patiente-centre-interview
```

2. Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```
___

### Running the Tests
From the project root directory:
```
python -m pytest
```
___

### Implementation Details
#### AnalyticsBuffer
The `AnalyticsBuffer` class stores events in memory and attempts to flush them to an API.

Constructor arguments:
* `bufferLimit`: maximum number of events before an immediate flush
* `timerLimit`: maximum time (in seconds) allowed between successful flushes
* `api`: a MockApi object
* `failureLimit`: maximum number of consecutive API failures before raising an error

Key attributes:
* `buffer`: list of events stored in memory
* `lastCall`: timestamp of the last successful API call
* `failureCount`: count of consecutive failed API calls

The `track(event)` method triggers a flush when required

#### MockApi
The `MockApi` class simulates a backend API using a configurable success probability.
* `successRate` must be a float between 0 and 1
* `call()` returns:
  * 1 for success
  * 0 for failure

___

### Testing Strategy
#### Tools Used
* pytest for automated unit testing
* Deterministic validation through repeated execution
* MockApi implementations to force success or failure
* Manual manipulation of timestamps to test time-based logic instantly

___

### Edge Case Handling
* API failures do not cause data loss; events remain in the buffer
* Consecutive API failures increment `failureCount`
* Once `failureLimit` is reached, a RuntimeError is raised to prevent infinite memory growth
* All limits are configurable via constructor arguments

___

### Design Decisions
* Configuration values are provided via constructor arguments instead of being hardcoded
* API logic is abstracted for easy testing
* The buffer is cleared only after a successful API call
* Failure handling is explicit and clearly communicated

___

### Possible Improvements
The following improvements could be made:
* Use an async event loop instead of synchronous calls
* Make the timer check continuous, not just when `track()` is called

___

### Author Notes
This project was implemented with a strong emphasis on testability, extensibility, and safety, following the assignment rubric closely. All critical behaviors are covered by automated unit tests, and the system is designed to be easy to evolve as requirements change.
