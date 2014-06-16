# Bibmark

Bibmark contains two python scripts to simplify working with markdown files, pandoc and bibtex references for academic writing. 

`crop_bibtex_file.py` is used to crop bibtex files to contain only the references that are cited in a markdown file.

`generate_docs_from_md.py` scans the current working dir and a subdir /refs for markdown and bibtex files, crops the bibtex files and calls pandoc to generate .pdf .odt and .docx documents from the markdown files.

These scripts are useful if you have a large several MB bibtex library like me and wish to generate smaller bibtex files to distribute with a markdown document. Cropping bibtex files also avoid problems with duplicate references in bibtex files (hello Mendeley) and speeds up processing markdown files with bibliographies. `crop_bibtex_file.py` also removes abstract and annotate items from bibtex references, which sometimes cause problems with pandoc.


# Requirements

* python: https://www.python.org/
* pandoc: http://johnmacfarlane.net/pandoc/


# Example usage

For example, we would like to include Einstein's relativity papers [@Einstein1905tragheit;@Einstein1916grundlage] in our bibliography, but not his other papers that are located in the /ref/Einsteins_refs.bib bibtex file.

Now run:

    >>> python crop_bibtex_file.py -s

or manually specify the location of this readme file and the bibtex file using

    >>> python crop_bibtex_file.py readme.md refs/Einsteins_refs.bib

To use pandoc to create pdf or docx document including a nice bibliography run:

    >>> pandoc readme.md -o readme.pdf --bibliography=refs/Einstein_refs_cropped_for_readme.bib --csl nature.csl

Citation style files can be found in many places, for example in Zotero's style repository: www.zotero.org/styles

You can also automate the entire process by running:

    >>> python generate_docs_from_md.py
    
This will automatically search for markdown files in the current working directory and bibtex files in the directory `refs`, crop all bibtex files and generate pdf, odt and docx output. 

# References