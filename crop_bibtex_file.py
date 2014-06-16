"""
create a new bibtex reference file with only those references that
are cited in a markdown file

Elco Luijendijk, march-april 2014

Examples:

>>> python crop_bibtex_file.py -s

search mode, script will try to find markdown and bibtex files in current
directory

>>> python crop_bibtex_file.py -s /home/user/example_dir

search mode, script will try to find markdown and bibtex files in directory
/home/user/example_dir

>>> python crop_bibtex_file.py md_file_1.md md_file_2.md bibtex_file.bib

will create two copies of bibtex_file.bib, named
bibtex_cropped_for_md_file_1.bib and bibtex_cropped_for_md_file_2.bib

"""

import os
import sys
import itertools


def remove_item(bib_list, item_name):

    """
    Remove item from bibtex entries

    Parameters
    ----------
    bib_list : list
        list of bibtex items
    item_name : string
        name of item to be removed from bibtex item, for instance
        'abstract' or 'annote'

    Returns
    -------
    modified_bib : list
        list of bibtex items

    """

    modified_bib = []

    for bib_item in bib_list:
        if ('%s =' % item_name) in bib_item:
            start_item = bib_item.find(item_name)-2
            end_item = start_item + bib_item[start_item:].find('}') + 1
            bib_item_cleaned = bib_item[:start_item] + bib_item[end_item:]
            modified_bib.append(bib_item_cleaned)
        else:
            modified_bib.append(bib_item)

    return modified_bib


if '-s' in sys.argv:

    print '-' * 20
    print 'searching for input markdown and bibtex files'
    print 'markdown file assumed to have extension .md and located in ' \
          'working directory'
    print 'bibtex file searched in subdirectory /refs'
    print 'if this directory does not exist the bibtex file is assumed to be '
    print 'located in the current working directory'

    # find out if user specified working directory:
    if sys.argv[-1] != '-s':
        workdir = sys.argv[sys.argv.index('-s')+1]
    else:
        # if not use current dir
        workdir = os.getcwd()

    # find ref folder, which contains bibtex file(s)
    refdir = os.path.join(workdir, 'refs')

    if os.path.isdir(refdir) is False:
        refdir = workdir

    cwd_files = os.listdir(workdir)
    ref_files = os.listdir(refdir)

    md_files = [fn for fn in cwd_files if '.md' in fn]

    if os.path.isdir(refdir) is True:
        bib_files = [os.path.join(refdir, fn) for fn in ref_files
                     if '.bib' in fn and 'cropped' not in fn]
    else:
        bib_files = [fn for fn in ref_files if '.bib' in fn]

    print 'found markdown files %s' % ', '.join(md_files)
    print 'found bibtex files %s' % ', '.join(bib_files)


elif len(sys.argv) > 2:
    # user specified markdown and bibtex file
    md_fn = [arg for arg in sys.argv if '.md' in arg]
    bib_fn = [arg for arg in sys.argv if '.bib' in arg]

else:
    print 'please specify input & output files, for example:'
    print '``python parse_bibtext.py markdown_file.md bibtex_library.bib '
    print 'or use ``python parse_bibtext.py -s`` to automatically search '\
          'for markdown and bibtex files and parse all combinations'
    exit()

# items to remove from bibtex entries
# for some reason pandoc citeproc cannot handle abstract or annote items
items_to_remove = ['abstract', 'annote']


for md_file, bib_file in itertools.product(md_files, bib_files):

    print '-' * 20
    print 'reading md file %s' % md_file

    md_f = open(md_file, 'r')
    md = md_f.read()
    md_f.close()

    print 'reading bib file %s' % bib_file

    bib_f = open(bib_file, 'r')
    bib = bib_f.read()
    bib_f.close()

    print 'extracting references found in %s from %s' % (md_file, bib_file)

    bibs = bib.split('@')[1:]

    keys = [b[b.find('{')+1:b.find(',')] for b in bibs]

    keys_in_md = ['@%s' % key in md for key in keys]

    updated_bibs = ['@'+b for b, key_in_md in
                    zip(bibs, keys_in_md) if key_in_md is True]

    # remove abstracts, somehow pandoc cannot handle these
    print 'removing items %s from new bibtex file' \
          % ', '.join(items_to_remove)
    for item_to_remove in items_to_remove:
        cleaned_bib = remove_item(updated_bibs, item_to_remove)

    # convert new bibtex file from list to string
    new_bib = ''.join(cleaned_bib)

    # construct output fn
    md_file_short = md_file.split('.')[-2]
    bib_file_short = '.'.join(bib_file.split('.')[:-1])
    output_fn = '%s_cropped_for_%s.bib' % (bib_file_short, md_file_short)

    # save new bibtex file
    print 'saving cropped bib file %s' % output_fn

    fout = open(output_fn, 'w')
    fout.write(new_bib)
    fout.close()

print 'done'