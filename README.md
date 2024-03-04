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
