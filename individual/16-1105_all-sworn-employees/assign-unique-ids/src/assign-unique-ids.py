#!usr/bin/env python3
#
# Author(s):    Roman Rivera

'''assign-unique-ids script for 16-1105_all-sworn-employees'''

import pandas as pd
import __main__

from assign_unique_ids_functions import assign_unique_ids, aggregate_data
import setup


def get_setup():
    ''' encapsulates args.
        calls setup.do_setup() which returns constants and logger
        constants contains args and a few often-useful bits in it
        including constants.write_yamlvar()
        logger is used to write logging messages
    '''
    script_path = __main__.__file__
    args = {
        'input_file': 'input/ase-units.csv.gz',
        'output_file': 'output/ase-units.csv.gz',
        'output_demo_file': 'output/ase-units_demographics.csv.gz',
        'id_cols': [
            "first_name", "last_name", "middle_initial",
            'middle_initial2', "suffix_name", 'current_age',
            "appointed_date", "gender", "race",
            'first_name_NS', 'last_name_NS'
            ],
        'max_cols': [
            'star1', 'star2', 'star3', 'star4', 'star5',
            'star6', 'star7', 'star8', 'star9', 'star10'
            ],
        'current_cols': ['unit'],
        'time_col': 'unit_start_date',
        'id': 'ase-units_ID'
        }

    assert (args['input_file'].startswith('input/') and
            args['input_file'].endswith('.csv.gz')),\
        "input_file is malformed: {}".format(args['input_file'])
    assert (args['output_file'].startswith('output/') and
            args['output_file'].endswith('.csv.gz')),\
        "output_file is malformed: {}".format(args['output_file'])

    return setup.do_setup(script_path, args)


cons, log = get_setup()

df = pd.read_csv(cons.input_file)

df, uid_report = assign_unique_ids(df, cons.id, cons.id_cols)
log.info(uid_report)
df.to_csv(cons.output_file, **cons.csv_opts)

agg_df = aggregate_data(df, cons.id, cons.id_cols,
                        max_cols=cons.max_cols,
                        current_cols=cons.current_cols,
                        time_col=cons.time_col)
agg_df.to_csv(cons.output_demo_file, **cons.csv_opts)