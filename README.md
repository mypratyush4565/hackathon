1.ER DIAGRAM:-
![1. ER DIAGRAM](images/er_diagram.png)

2.FLOWCHART:-
![2. FLOWCHART](images/flowchart.png)

3.DATA FLOW DIAGRAM(DFD):-
![3. DFD](images/dfd.png) 

4.EVIDENCE CAPTURE AND VERIFICATION FLOW
![4. EVIDENCE CAPTURE AND VERIFICATION FLOW](images/evidence_capture_and_verification_flow.png)

 VeriCourt:-A Court-Aware Digital Evidence Integrity & Trust Assessment Framework

1. Overview 

Digital media has become a critical form of legal evidence, yet most systems focus only on preserving files after submission. They fail to assess how much an evidence item should be trusted, especially when manipulation, delay, or loss of context may occur before it enters an official system. 

VeriCourt shifts the focus from claiming authenticity to structured, transparent credibility assessment, aligned with judicial reasoning rather than technological absolutism. 

2. Problem Statement 

Modern courts increasingly rely on videos, images, and audio recordings, but existing evidence systems suffer from three systemic failures: 

(i)Pre-Entry Blindness – Evidence may be altered or selectively presented before submission, with no structured way to reason about this uncertainty. 

(ii)Unequal Sources, Equal Treatment – Informal public recordings and official surveillance footage are often processed similarly despite vastly different reliability. 

(iii)False Certainty – Deepfake detection, blockchain storage, and metadata checks often imply authenticity, which is legally unsafe and technically unreliable. 

Courts do not require technological truth; they require explainability, transparency, and clearly stated uncertainty. 

3. Key Insight 

Evidence preservation is not the same as evidence trust evaluation. 

4. VeriCourt Philosophy 

VeriCourt does not determine what is true. 

It structures: 

(a)why evidence should be trusted 

(b)to what extent it should be trusted 

(c)where uncertainty explicitly exists 

(d)The framework supports judicial judgment rather than replacing it. 

5. Trust Boundary Shift 

Evidence is assigned legal weight based on its source: 

(i)Official CCTV / Bodycam — High 

(ii)Vehicle Dashcam — Medium 

(iii)Public Mobile Recording — Low 

(iv)Forwarded / Re-shared Media — Very Low 

This prevents over-reliance on edited or viral content and mirrors real-world judicial intuition. 

6. Pre-Entry Risk Scoring 

Instead of claiming authenticity, VeriCourt evaluates pre-entry risk using factors such as: 

(a)Capture-to-submission delay 

(b)Source category 

(c)Metadata consistency 

(d)Availability of capture context 

(e)Declared transfer history 

Output: Low / Medium / High Pre-Entry Risk 

Uncertainty is disclosed rather than concealed. 

7. Mandatory Disclosure Protocol 

Each uploader must formally declare: 

(i)Recorder identity 

(ii)Time and location of capture 

(iii)Transfer path prior to submission 

These declarations are immutably recorded. If later contradicted, the credibility of the evidence collapses, similar to a false affidavit. 

8. Post-Registration Integrity Protection 

Once registered: 

A cryptographic hash is generated 
         ↓        
A timestamp is sealed 
         ↓
A unique Evidence ID is assigned 
         ↓
This ensures post-entry integrity without making retroactive authenticity claims. 
         
9. Multi-Source Corroboration Logic 

When multiple evidences exist, VeriCourt evaluates: 

(i)Temporal alignment 

(ii)Spatial consistency 

(iii)Event sequencing 

(iv)Source independence 

The system flags agreement, conflict, or dependency but issues no probabilistic verdicts. 

10. Expectation-Based Evidence Coverage 

The system assesses whether additional evidence should reasonably exist given the context. 

Examples: 

(i)Busy public location → high expectation 

(ii)Private or restricted space → low expectation 

(iii)Missing expected evidence results in a coverage warning, not an accusation. 

11. Judicial Output & Scope 

VeriCourt generates a neutral analytical report including: 

-> Integrity status 

1. Source reliability classification 

2. Pre-entry risk level 

3. Corroboration strength 

4. Evidence coverage adequacy 

All final determinations remain entirely human. VeriCourt does not reconstruct events, claim certainty, or replace judicial reasoning. 

## **Improvements in Round 2:-**

1. Multi-Evidence Corroboration:

-> Cross-verify multiple related evidence files (e.g., CCTV + dashcam + mobile video of the same event).

-> Show a consistency report highlighting mismatches or confirmed matches.

2. Chain-of-Custody Tracking

-> Maintain a timeline of every action on each evidence (uploaded, verified, accessed, shared).

-> Use timestamps + user IDs to show audit trail.

-> Can be stored in a small database like SQLite.

3. Secure User Authentication

-> Allow judges, police, or admin roles to log in.

-> Only registered users can upload/verify.

-> Can integrate JWT or session-based authentication.

4. Enhanced Pre-Entry Risk Assessment

-> Include more factors for risk:

->  File source reliability

-> Upload time (recent or delayed)

-> File format and metadata

-> Assign dynamic risk score (Low / Medium / High / Critical).

5. File Metadata Extraction

-> Extract metadata like: Camera type, timestamp, GPS coordinates (if available)

6. Download / Print Evidence Report

-> Allow users to download a PDF certificate of evidence integrity, including hash, risk, source, and timestamp.