# BOM notes

ReadyKit is software. The bill of materials lists the kit's modules and free dependencies so the numbering matches the exploded view in `media/exploded.png` and drawing RDK-DWG-001. Items 1 to 7 and 12 each have their own object in the view; the tray numbered 10 stands for all the bought open-source parts (items 8, 10, 11 and 13). Item 9, CI hosting, is not shown.

Items 12 (repository reader) and 13 (3D viewer script) were added on 2026-10-01 to make the design constructable (RDK-DDR-003). Lines 2, 5, 7, 8 and 10 were reworded for the same record: the identity file is read through the reader, the gate writes the README badge, each repository carries a small stub instead of the whole kit, the fonts ship inside the package, and the dependencies split into a small core and optional extras.

Changes carried out on 2026-10-02 from the decisions of that day: the reader's identity record gained a sixth value, the still-open phrase (line 12); the tray (line 10) now has five bays, one for the core libraries and one for each extra, with the release gate and archive helper in the release extra; line 7 names the CI platforms (Linux, macOS, Windows through WSL2) and the Python versions (3.11 and the newest release). No line changed price and no line was added or removed. Mass: not applicable, ReadyKit is software and the massing is illustrative.

Every line is priced. All costs are USD 0.00: every module is written in-house under MIT, and every dependency is free and open source (licenses in RDK-CAL-001, section F; the viewer script is Apache-2.0). Value-engineering target: USD 0 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 0 (USD 0 over the target). Contributor time is not costed here.

The only paid option is private-repository CI time beyond GitHub's included minutes, which the tool does not need.
