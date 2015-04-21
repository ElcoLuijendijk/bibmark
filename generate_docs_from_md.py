"""
call script to crop bibtex files to include only references contained
in any markdown files in the work directory and then run pandoc to
generate pdf, docx and odt output

standard input:
python generate_docs_from_md.py markdown_dir bibtex_dir

where markdown dir is the location of the directory containing one or more


To run the script from the present working directory:
>>> python generate_docs_from_md.py

Run from a different directory
>>> python generate_docs_from_md.py 'home/user/example_dir'

Run from a different directory and specify directory containing bibtex file(s)
>>> python generate_docs_from_md.py 'home/user/example_dir' 'home/user/bibtext_dir'

"""

import sys
import os
import subprocess


def parse_arguments(args):

    """
    parse file arguments
    separates arguments in main arguments starting with - and additional
    options that follow each main argument

    :param args:
    :return:

    """

    args_ind = [i for i, s in enumerate(args) if s[0] == '-']
    arg_names = [args[i] for i in args_ind]
    arg_opts = [args[a+1:b] for a, b in zip(args_ind[:-1], args_ind[1:])]
    arg_opts.append(args[args_ind[-1]+1:])

    final_args = [[a, b] for a, b in zip(arg_names, arg_opts)]

    return final_args

# default options
ref_dir = None
output_formats = ['docx', 'pdf']
pandoc_args = []

# 
scriptdir = os.path.dirname(os.path.realpath(__file__))
current_dir = os.getcwd()

args = sys.argv[1:]

# find out if user specified work dir
if len(args) > 0:
    work_dir = args[-1]
    args = args[:-1]
elif 'last_directory.txt' in os.listdir(scriptdir):
    work_dir =\
        open(os.path.join(scriptdir, 'last_directory.txt'), 'r').read().strip()
    print 'trying to look for markdown files in last-used directory: %s' \
          % work_dir
    print 'press enter to continue or enter an alternative directory path:'
    a = raw_input()
    if len(a) > 0:
        work_dir = a
else:
    print 'please enter the full path to the directory where I should ' \
          'look for markdown files'
    work_dir = raw_input()

# find args
final_args = parse_arguments(args)
for arg, arg_opts in final_args:
    if arg == '-bibtex':
        # user-specified bibtex dir:
        print 'user-specified bibtex directory'
        ref_dir = arg_opts[0]
    if arg == '-o':
        # user specified output formats
        output_formats = arg_opts
    else:
        # pass args on to pandoc
        pandoc_arg = arg
        pandoc_arg += ' '.join(arg_opts)
        pandoc_args.append(pandoc_arg)

if ref_dir is None:
    if 'darwin' in sys.platform:
        default_bibtex_folder = 'default_bibtex_folder_mac.txt'
    else:
        default_bibtex_folder = 'default_bibtex_folder.txt'

    if os.path.exists(default_bibtex_folder):
        print 'reading default bibtex file location from ' \
              '%s' % default_bibtex_folder

        fin = open(default_bibtex_folder, 'r')
        ref_dir = fin.readlines()[0].rstrip()
        fin.close()
    else:
        ref_dir = os.path.join(work_dir, 'refs')
        if os.path.exists(ref_dir) is False:
            ref_dir = work_dir

home = os.path.expanduser("~")
if work_dir[0] == '~':
    work_dir = os.path.join(home, work_dir[2:])
if ref_dir[0] == '~':
    ref_dir = os.path.join(home, ref_dir[2:])

print 'looking for markdown files in %s' % work_dir
print 'and looking for bibtex files in %s' % ref_dir

# crop bibtex file
subprocess.call(['python',
                 os.path.join(scriptdir, 'crop_bibtex_file.py'),
                 work_dir, ref_dir])

fns = os.listdir(work_dir)
fns_ref = os.listdir(work_dir)
fns_script = os.listdir(scriptdir)

markdown_files = [fn for fn in fns if ('.md' in fn and '~' not in fn)]

# find bibliography style file (.csl),
# assume there is only one in work directory
csl_folder = work_dir
csl_files = [fn for fn in fns if '.csl' in fn]

if len(csl_files) == 0:
    print 'cannot find a csl file in working dir, ' \
          'trying to find .csl file in the bibmark directory instead'
    csl_files = [fn for fn in fns_script if '.csl' in fn]
    csl_folder = scriptdir
    if len(csl_files) == 0:
        msg = 'could not find a .csl file in the working directory %s or ' \
              'the script directory %s' \
              % (work_dir, scriptdir)
        raise IndexError(msg)

csl_files.sort()
csl_file = csl_files[0]


for markdown_file in markdown_files:
    
    md_short = markdown_file.split('.')[-2]

    bib_files = [fn for fn in fns_ref if 'for_%s.bib' % md_short in fn]

    # go through all bibtex files
    # there should be only one, but just in case
    for bib_file in bib_files:

        bib_file_with_path = os.path.join(work_dir, bib_file)

        for output_format in output_formats:

            output_file = os.path.join('%s.%s' % (md_short, output_format))

            #md_file_loc = os.path.join(work_dir, markdown_file)
            csl_fn = os.path.join(csl_folder, csl_file)

            pdc = ['pandoc', markdown_file, '-o',  output_file,
                   '-V', 'geometry:margin=1in',
                   '--bibliography=%s' % bib_file_with_path,
                   '--csl=%s' % csl_fn]

            if pandoc_args != []:
                pdc.append(pandoc_args[0].strip('"'))

            print '\n\ncalling pandoc:\n'
            print '-> ', ' '.join(pdc)

            # using os.chdir to change to directory where markdown file is
            # located. Not so elegant, but only way to keep figure references
            # in markdown file intact
            os.chdir(work_dir)
            subprocess.call(pdc)
            os.chdir(current_dir)

# saving directory path
fout = open(os.path.join(scriptdir, 'last_directory.txt'), 'w')
fout.write('%s' % work_dir)
fout.close()

print 'done'
