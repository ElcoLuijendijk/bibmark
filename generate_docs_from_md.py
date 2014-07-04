"""
call script to crop bibtex files to include only references contained
in any markdown files in the work directory and then run pandoc to
generate pdf, docx and odt output

To run the script from the present working directory:
>>> python generate_docs_from_md.py

Run from a different directory
>>> python generate_docs_from_md.py -d 'home/user/example_dir'


"""


import sys
import os
import subprocess

# 
scriptdir = os.path.dirname(os.path.realpath(__file__))
current_dir = os.getcwd()

# find out if user specified work dir
if '-d' in sys.argv:
    work_dir = sys.argv[sys.argv.index('-d')+1]
else:
    work_dir = os.getcwd()

ref_dir = os.path.join(work_dir, 'refs')
if os.path.exists(ref_dir) is False:
    ref_dir = work_dir

print 'looking for markdown files in %s' % work_dir
print 'and looking for bibtex files in %s' % ref_dir

# crop bibtex file
subprocess.call(['python',
                 os.path.join(scriptdir, 'crop_bibtex_file.py'),
                 '-s', work_dir])

fns = os.listdir(work_dir)
fns_ref = os.listdir(ref_dir)

markdown_files = [fn for fn in fns if ('.md' in fn and '~' not in fn)]

# find bibliography style file (.csl),
# assume there is only one in work directory
csl_file = [fn for fn in fns if '.csl' in fn][0]

# user specified output formats
if '-o' in sys.argv:
    output_formats = sys.argv[sys.argv.index('-o')+1:]
# default = pdf, docx and odt output
else:
    output_formats = ['pdf', 'docx', 'odt']

for markdown_file in markdown_files:
    
    md_short = markdown_file.split('.')[-2]

    bib_files = [fn for fn in fns_ref if 'for_%s.bib' % md_short in fn]

    # go through all bibtex files
    # there should be only one, but in just in case
    for bib_file in bib_files:

        bib_file_with_path = os.path.join(ref_dir, bib_file)

        for output_format in output_formats:

            output_file = os.path.join('%s.%s' % (md_short, output_format))


            #md_file_loc = os.path.join(work_dir, markdown_file)
            #csl_file_loc = os.path.join(work_dir, csl_file)

            pdc = ['pandoc', markdown_file, '-o',  output_file,
                   '-V', 'geometry:margin=1in',
                   '--bibliography=%s' % bib_file_with_path,
                   '--csl=%s' % csl_file]
            print '\n\ncalling pandoc:\n'
            print '-> ', ' '.join(pdc)

            # using os.chdir to change to directory where markdown file is
            # located. Not so elegant, but only way to keep figure references
            # in markdown file intact
            os.chdir(work_dir)
            subprocess.call(pdc)
            os.chdir(current_dir)

print 'done'
