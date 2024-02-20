0.4.0 (2023-10-18)
------------------

- Move root-level $ref in schemas to an allOf combiner. [#87]
- Fix URI fragment format in transform-1.2 schema. [#88]
- Update schemas for ASDF standard 1.6.0 [#110]

0.3.0 (2022-08-22)
------------------

- Add schemas to properly support bounding_box and compound_bounding_box. [#31]
- Add fixed and bounds to base transform schema to properly document them. [#34]
- Add input_units_equivalencies to base transform schema to properly document it. [#36]
- Update spline1d schema. [#46]
- Add Schechter1D schema. [#54]
- Fix fix_inputs tag bug. [#57]
- Create docs for package. [#59]
- Move packaging configuration to ``pyproject.toml``. [#62]
- Remove unnecessary ``tag:`` entry from all schemas. [#65]

0.2.2 (2022-02-24)
------------------

- Add inputs and outputs to base transform schema to properly document them. [#33]
- Add spline1d schema. [#41]
- Add cosine, tangent, arcsine, arccosine, and arctangent schemas. [#40]
- Fix circular build dependencies for asdf. [#38]

0.2.0 (2021-12-13)
------------------

- Remove generic-1.x.0 schemas and examples. [#30]

0.1.0 (2021-11-24)
------------------

- Initial release
