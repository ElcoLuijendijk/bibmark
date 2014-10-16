# Bibmark

Bibmark contains two python scripts to simplify working with markdown files, pandoc and bibtex references for academic writing. 

`crop_bibtex_file.py` is used to crop bibtex files to contain only the references that are cited in a markdown file.

`generate_docs_from_md.py` scans the current working dir and a subdir /refs for markdown and bibtex files, crops the bibtex files and calls pandoc to generate .pdf .odt and .docx documents from the markdown files.

These scripts are useful if you have a large several MB bibtex library like me and wish to generate smaller bibtex files to distribute with a markdown document. Cropping bibtex files also avoid problems with duplicate references in bibtex files (hello Mendeley) and speeds up processing markdown files with bibliographies. `crop_bibtex_file.py` also removes abstract and annotate items from bibtex references, which sometimes cause problems with pandoc.


# Requirements

* python: https://www.python.org/
* pandoc: http://johnmacfarlane.net/pandoc/


# Example usage

For example, we would like to include Einstein's relativity papers [@Einstein1905tragheit;@Einstein1916grundlage] in our bibliography, but not his other papers that are located in the `/refs/Einsteins_refs.bib` bibtex file.

To crop the bibtex file, run:

    >>> python crop_bibtex_file.py

This will automatically crop the bibtex file located in a folder specified in `default_bibtex_file.txt` located in the bibmark folder. If this file does not exist the script searches for bibtex files in the folder `refs`.

To use pandoc to create a pdf document including a nice bibliography run:

    >>> pandoc readme.md -o readme.pdf --bibliography=refs/Einstein_refs_cropped_for_readme.bib --csl rvmp.csl

The --csl command specifies a citation style. Citation style files can be found in many places, for example in Zotero's style repository: www.zotero.org/styles

You can also automate the entire process by running:

    >>> python generate_docs_from_md.py
    
This will automatically search for markdown files in the current working directory and bibtex files in the directory `refs`, crop all bibtex files and generate pdf, odt and docx output.

See the included readme.pdf, readme.odt or readme.docx files to check how this readme file looks with a bibliography.


# License

GPL v3 (http://www.gnu.org/copyleft/gpl.html)



Elco Luijendijk, 2014


# References