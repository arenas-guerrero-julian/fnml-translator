# RML-FNML Translator

RML-FNML translator unfolds data transformation defined in RML-FNML to RML Views.

## Install

```
pip install git+https://github.com/arenas-guerrero-julian/rml_fnml_translator.git
```

## Usage

```
usage: python3 -m rml_fnml_translator [-h] [-i INPUT] [-o OUTPUT] [-m MAPPING_LANGUAGE] [-v]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to the input [R2]RML-FNML mappings
  -o OUTPUT, --output OUTPUT
                        path to the output [R2]RML mappings
  -m MAPPING_LANGUAGE, --mapping_language MAPPING_LANGUAGE
                        whether to generate R2RML or RML (valid options: `R2RML` or `RML`)
  -v, --version         show program's version number and exit
```

## Citing 💬

Cite the associated [ICWE paper](https://oa.upm.es/82205/1/2024_ICWE_RML_FNML_to_RML_Views.pdf):

```bib
@inproceedings{arenas2024handling,
  title = {{Handling Data Transformations in Virtual Knowledge Graphs with RML View Unfolding}},
  author = {Arenas-Guerrero, Julián},
  booktitle = {Proceedings of the 24th International Conference on Web Engineering},
  publisher = {Springer Nature Switzerland},
  pages = {424-427},
  year = {2024},
  isbn = {978-3-031-62362-2},
  doi = {10.1007/978-3-031-62362-2_38},
}
```
