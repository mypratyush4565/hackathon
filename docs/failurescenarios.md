# Failure Scenarios – VeriCourt System
This document explains how the VeriCourt system behaves when something goes wrong during evidence handling.

## Scenario 1: Evidence File Modified After Registration

**What went wrong**  
The evidence file was changed after it was already registered.

**When it happens**  
During verification or when a file is uploaded again later.

**System check**  
The system compares the original hash with the current file hash.

**System response**  
- Evidence is marked as Integrity Failed  
- An alert is generated  
- The change is recorded in the audit log  
- The original evidence is not replaced

## Scenario 2: Late Upload From a Non-Trusted Source

**What went wrong**  
Evidence was recorded earlier but uploaded much later.

**When it happens**  
During pre-entry risk assessment.

**System check**  
The system checks the delay between capture time and upload time.

**System response**  
- Risk score is increased  
- Mandatory disclosure is required  
- Evidence is marked as low or medium trust

## Scenario 3: Insufficient Corroboration Sources

**What went wrong**  
Only one source of evidence is available when more were expected.

**When it happens**  
During multi-source corroboration.

**System check**  
The system checks the number and independence of sources.

**System response**  
- Corroboration strength is reduced  
- The court report shows limited support  
- Evidence is still allowed

## Scenario 4: Expected Evidence Coverage Not Met

**What went wrong**  
Expected evidence for a location or time is missing.

**When it happens**  
During coverage analysis.

**System check**  
Expected sources are compared with actual sources.

**System response**  
- Coverage status is marked as inadequate  
- A warning is added to the court report

## Scenario 5: Attempt to Replace Registered Evidence

**What went wrong**  
Someone tries to overwrite already registered evidence.

**When it happens**  
After evidence registration.

**System check**  
The system checks if the evidence ID already exists.

**System response**  
- The request is rejected  
- Original evidence remains unchanged  
- The attempt is logged

These rules ensure that evidence integrity, transparency, and court trust are always protected.
