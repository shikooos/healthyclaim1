# HealthyClaim — Healthcare Billing Intelligence & Research Platform

[![Status: Public Preview](https://img.shields.io/badge/Status-Public%20Preview-blue.svg)](https://healthyclaim.com)
[![License: Research & Evaluation](https://img.shields.io/badge/License-Research%20%26%20Evaluation-green.svg)](#license)

> **HealthyClaim is a healthcare billing intelligence and research platform in public preview, exploring how AI-assisted clinical evidence extraction can work with deterministic verification to produce evidence-backed coding and claim artifacts.**

---

## 🔬 Core Architecture: Evidence-First Adjudication

Traditional AI billing systems often allow Large Language Models (LLMs) to directly select billing codes—leading to hallucinations, unverified add-on codes, and unsupportable audit risk. 

HealthyClaim establishes a strict architectural separation: **AI never decides final billing truth**.

```
Clinical Documentation (SOAP / H&P / Operative Notes)
  │
  ▼
[ 1. Context Retrieval ]
  │   Retrieves relevant coding criteria, policy scopes, and specialty context
  ▼
[ 2. Linguistic Evidence Extraction ]
  │   Extracts documented clinical facts, assertions, anatomy, and laterality
  ▼
[ 3. Candidate Code Mapping ]
  │   Proposes candidate CPT, HCPCS, and ICD-10-CM codes grounded in extracted facts
  ▼
[ 4. Deterministic Rule Adjudication ]
  │   Evaluates candidates against authoritative sources:
  │   ├── CMS NCCI PTP edits (Column 1 / Column 2 & CCMI indicators)
  │   ├── CMS Medically Unlikely Edits (MUE caps & adjudication indicators)
  │   ├── Medicare LCD/NCD medical necessity criteria
  │   └── Deterministic modifier logic (Modifier 25, 59, 50, X{EPSU})
  ▼
[ 5. Draft Claim Artifact Generation ]
      Outputs draft CMS-1500 and ANSI ASC X12 EDI 837P artifacts for testing
```

---

## 🌐 Public Resources & Links

- **Live Website:** [https://healthyclaim.com](https://healthyclaim.com)
- **Public Interactive Demo:** [https://healthyclaim.com/#simulator](https://healthyclaim.com/#simulator)
- **Methodology & Pipeline:** [https://healthyclaim.com/methodology/](https://healthyclaim.com/methodology/)
- **Research & Engineering Papers:** [https://healthyclaim.com/research/](https://healthyclaim.com/research/)

---

## 🧪 What You Can Explore

- **Clinical Evidence Extraction:** How linguistic models extract objective facts from unstructured clinical narratives without hallucinating undocumented procedures.
- **Deterministic Rule Verification:** Real-time evaluation of candidate codes against CMS NCCI unbundling rules, MUE unit ceilings, and modifier hierarchies.
- **Draft Claim Artifacts:** Generation of standard CMS-1500 layout structures and ANSI ASC X12 837P EDI transaction loops for workflow integration testing.
- **Benchmark Methodologies:** Evaluation protocols using synthetic clinical notes to measure coding recall, precision, and unbundling prevention.

---

## 🔒 What Is Intentionally Private & Excluded

To maintain security, patient privacy, and project integrity, this public repository does **NOT** contain:
- **Protected Health Information (PHI):** All demos, test cases, and examples use strictly synthetic or de-identified clinical data.
- **Production Credentials:** No clearinghouse API keys, database credentials, or production server secrets.
- **Proprietary Knowledge Graphs:** Production database snapshots and internal vector embeddings are hosted on secure private infrastructure.
- **Production Clearinghouse Integrations:** This repository provides research and test artifacts; live EDI submission occurs via private enterprise connectors.

---

## 🚫 What HealthyClaim Is NOT

- **NOT an LLM that invents CPT codes:** The system does not allow probabilistic language models to guess or hallucinate billing codes.
- **NOT a chatbot making billing decisions:** All coding and modifier determinations are adjudicated deterministically.
- **NOT a production clearinghouse:** HealthyClaim produces draft claim artifacts for testing, evaluation, and downstream clearinghouse intake.
- **NOT a substitute for professional billing or compliance review:** The platform is designed to assist and provide audit traceability, not to eliminate human oversight.

---

## 📌 Repository Topics

`healthcare` • `medical-billing` • `medical-coding` • `healthcare-ai` • `revenue-cycle-management` • `medical-claims` • `ncci` • `mue` • `cms-1500` • `edi-837` • `clinical-documentation`

---

## 📬 Development Status & Contact

HealthyClaim is under active development. We welcome feedback from healthcare providers, revenue cycle engineers, and medical coding researchers.

- **Follow the Project:** Star and watch this repository for architectural updates and benchmark releases.
- **Test the Public Demo:** Visit [healthyclaim.com](https://healthyclaim.com) to test synthetic clinical notes.
- **Contact:** [info@healthyclaim.com](mailto:info@healthyclaim.com)
