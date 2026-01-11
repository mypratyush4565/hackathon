# Event Flow – VeriCourt System

This document explains the sequence of events that occur from evidence submission to court report generation.

## Event 1: EvidenceRegistered

**Triggered when**  
A user submits evidence and it is accepted for registration.

**What it means**  
The evidence is now stored and assigned an evidence ID.

**Next actions**  
- Hash generation begins  
- Risk evaluation is triggered

## Event 2: RiskScoreCalculated

**Triggered when**  
Pre-entry risk assessment is completed.

**What it means**  
The system has evaluated trust, delay, and source reliability.

**Next actions**  
- Risk score is stored  
- Disclosure requirements are determined

## Event 3: IntegrityVerified

**Triggered when**  
Evidence hash verification is performed.

**What it means**  
The system confirms whether the evidence was modified.

**Next actions**  
- Integrity status is updated  
- Any mismatch is flagged

## Event 4: CorroborationCompleted

**Triggered when**  
Multiple evidence sources are analyzed together.

**What it means**  
The system evaluates consistency across sources.

**Next actions**  
- Corroboration strength is recorded  
- Coverage analysis proceeds

## Event 5: CourtReportGenerated

**Triggered when**  
All checks are completed successfully.

**What it means**  
The evidence is ready for legal review.

**Next actions**  
- Final report is stored  
- Report is made available to judges

This event-driven flow allows VeriCourt to remain modular, scalable, and easy to extend in the future.
