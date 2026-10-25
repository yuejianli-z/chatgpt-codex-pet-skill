# Stage-by-stage learning ledger

Record an increment for each stage actually experienced. Do not invent a failure to fill the form: “none found” must include the inspected scope. Use project-local labels and sanitized public summaries. Keep original failed logs and executed inputs intact.

## Entry (duplicate for each finding)
- Entry label / case label / stage / date:
- Input evidence: reference/version/hash; actually inspected image/frame/time range; observation method and limits:
- Failure or improvement opportunity: observed result versus expected criterion; or none found and scope:
- Cause hypothesis: supporting evidence, uncertainty and alternative explanations:
- Bounded fix: exact change, preserved approved layers/cells, authorized scope, attempt count/budget and stop/change-route condition:
- Verification: actual execution and result below; new version and preserved failed-run reference:
- Outcome: verified / unresolved; unresolved defect or blocking evidence:
- Generalizable rule: precise wording, applicable conditions, exclusions, and location of implemented rule/template/check:
- Generalization status: supported_within_case / proposed_transfer / cross_case_verified:
- Evidence status: observed / untested / inconclusive:
- Regression test/scenario references and actual execution results:

Required chain: stage evidence → failure/opportunity → hypothesis → bounded fix → verified or unresolved outcome → scoped rule → regression test. Record uncertainty instead of filling a missing link with a success claim.

## Verification evidence
| Kind: machine / visual / user_feedback | Artifact/version/hash and inspected scope | Method / reviewer or tool / date | Result: pass / warning / fail / not_run / blocked | Concrete evidence and limits |
| --- | --- | --- | --- | --- |
| | | | | |

For visual evidence, state native/enlarged dimensions, comparable reference/view, exact images/frames/time ranges and findings. For timed playback, record actual watch duration and timestamps. Generation, decoding and watching are different events. A validator reporting pass cannot substitute for a visual pass.

## Regression and implementation
| Kind: machine / manual | Test or scenario reference | Protected invariant / failure condition | Actual status: passed / failed / not_run | Evidence / affected rule or template |
| --- | --- | --- | --- | --- |
| | | | | |

- Machine-checkable quantities and actual check evidence:
- Human-only identity/aesthetic/brush-intent scenario and reviewer evidence, or not_run:
- Cross-case transfer: cases actually tested, versions, evidence and counterexamples; otherwise proposed_transfer:
- Unresolved follow-up, responsible decision and next evidence needed:

## Integrity checks
- [ ] Every actual stage is represented; absent stages are not invented.
- [ ] Hypotheses are distinguished from observations; fixes have bounded scope.
- [ ] Failed reports and original prompts remain preserved; corrections are new annotations/runs.
- [ ] Verification outcomes cite actual evidence; blocked and untested work stays explicit.
- [ ] No manual visual scenario is reported as an automated pass.
- [ ] A within-case finding is not labeled cross_case_verified without cross-case evidence.
- [ ] Every retained learning maps to a concrete rule/template/check and regression scenario.
- [ ] Public copies exclude private inputs, identifiers, paths and case artwork without clearance.

A ledger/schema validator can check structure, evidence-chain fields and status consistency only. It cannot certify that evidence prose is true or judge artistic quality. Record the validator actually available, invocation/version, inspected ledger version, result and limitations here:
