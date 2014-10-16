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

import pdb
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


# find out if user specified work dir
if len(sys.argv) > 1:
    work_dir = sys.argv[1]
else:
    work_dir = os.getcwd()

if len(sys.argv) > 2:
    ref_dir = sys.argv[2]
else:
    ref_dir = os.path.join(work_dir, 'refs')
    if os.path.exists(ref_dir) is False:
        ref_dir = work_dir

print 'looking for markdown files in %s' % work_dir
print 'and looking for bibtex files in %s' % ref_dir

cwd_files = os.listdir(work_dir)
ref_files = os.listdir(ref_dir)

md_files = [fn for fn in cwd_files if '.md' in fn and '.md~' not in fn]

md_files_full = [os.path.join(work_dir, md_file) for md_file in md_files]

if os.path.isdir(ref_dir) is True:
    bib_files = [os.path.join(ref_dir, fn) for fn in ref_files
                 if '.bib' in fn and 'cropped' not in fn]
else:
    bib_files = [fn for fn in ref_files if '.bib' in fn]

print 'found markdown files %s' % ', '.join(md_files_full)
print 'found bibtex files %s' % ', '.join(bib_files)

# items to remove from bibtex entries
# for some reason pandoc citeproc cannot handle abstract or annote items
items_to_remove = ['abstract', 'annote']


for md_file, md_filename, bib_file in \
        itertools.product(md_files_full, md_files, bib_files):

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
    md_file_short = (os.path.split(md_file)[-1]).split('.')[-2]
    bib_file_short = os.path.split(bib_file)[-1].split('.')[-2]
    output_fn = '%s_cropped_for_%s.bib' % (bib_file_short, md_file_short)
    output_fn_full = os.path.join(work_dir, output_fn)

    # save new bibtex file
    print 'saving cropped bib file %s' % output_fn_full

    fout = open(output_fn_full, 'w')
    fout.write(new_bib)
    fout.close()

print 'done'
