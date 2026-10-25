# Contributing

[中文](CONTRIBUTING.zh-CN.md)

Keep English SKILL.md normative and Chinese guidance semantically equivalent. For every behavior change, cite a rule ID and a real failure or clearly labeled hypothesis. Add machine tests only for machine-checkable properties; visual checks remain manual evidence.

Run `python -m unittest discover -s tests -v`, the manifest example and ledger checker. Preserve failed fixtures/reports when relevant, without private data. Do not rewrite executed prompt histories. Avoid new network/provider dependencies without an explicit capability and privacy review.

Do not submit private photos, unlicensed character art, credentials, signed URLs or owner identifiers. Use original geometric fixtures. A pull request must list changed approval scope, runtime assumptions, bilingual changes and untested behavior. Do not create a public issue containing sensitive evidence.

## Full validation commands

Run the README developer checks and [runnable examples](../skills/create-desktop-companion/docs/en/examples.md), including both bilingual ledger examples. Review [validation evidence](../skills/create-desktop-companion/docs/validation.md) for test scope; browser and native-host acceptance must not be inferred from mocked controller tests. Verify relative links, anchors, asset notices, and English/Chinese parity before proposing a release.

Run diagnostic commands from `skills/create-desktop-companion/`; keep character media in `examples/characters/`, outside the installable skill.
