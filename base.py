from conf import *
from random import randint
from datetime import datetime
import os
import csv
import time
import subprocess as sub


def confirm(prompt):
    """
    Prompt a confirm in raw input
    """
    prompt = '%s [%s or %s]: ' % (prompt, 'yes', 'no')
    while True:
        ans = raw_input(prompt)
        if ans not in ['yes', 'no']:
            print 'Please enter yes or no\n'
            continue
        if ans == 'yes':
            return True
        if ans == 'no':
            return False


def run_test_suite():
    """
    Run SPEC CPU suite
    """
    spec_cmd = ['runspec', '--config', 'spec_test_config.cfg', '--noreportable', '--tune', 'base', '--output_format',
                'csv', '--iterations', '1']
    spec_cmd.extend(spec_tests)
    sub.call(spec_cmd)


def parse_test_results():
    """
    Parse SPEC CPU test results
    """
    os.chdir('/SPEC/CPU2006/result')

    for item in spec_tests:
        with open(int_result_csv, 'rb') as f:
            csv_handler = csv.reader(f)
            for row in csv_handler:
                if item in row:
                    results["%s_base_ref" % item] = row[1]
                    results["%s_base_run" % item] = row[2]
                    results["%s_base_ratio" % item] = row[3]
                    results["%s_peak_ref" % item] = row[6]
                    results["%s_peak_run" % item] = row[7]
                    results["%s_peak_ratio" % item] = row[8]
                    break

    for item in spec_tests:
        with open(fp_result_csv, 'rb') as f:
            csv_handler = csv.reader(f)
            for row in csv_handler:
                if item in row:
                    results["%s_base_ref" % item] = row[1]
                    results["%s_base_run" % item] = row[2]
                    results["%s_base_ratio" % item] = row[3]
                    results["%s_peak_ref" % item] = row[6]
                    results["%s_peak_run" % item] = row[7]
                    results["%s_peak_ratio" % item] = row[8]
                    break

    results['end_time'] = datetime.now()
    results['end_time_formatted'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results['test_duration'] = (results['end_time'] - results['start_time']).seconds
    return


def save_test_results():
    """
    Save results to database
    """
    Open_SpecCpu = SpecCpu(
        project_id=project_id,
        project=project_name,
        provider=provider_name,
        instance_type=vm_name,
        iteration=iteration,
        start_time=results['start_time_formatted'],
        end_time=results['end_time_formatted'],
        test_duration=results['test_duration'],
        perlbench_base_ref=results['400.perlbench_base_ref'],
        perlbench_base_run=results['400.perlbench_base_run'],
        perlbench_base_ratio=results['400.perlbench_base_ratio'],
        perlbench_peak_ref=results['400.perlbench_peak_ref'],
        perlbench_peak_run=results['400.perlbench_peak_run'],
        perlbench_peak_ratio=results['400.perlbench_peak_ratio'],
        bzip2_base_ref=results['401.bzip2_base_ref'],
        bzip2_base_run=results['401.bzip2_base_run'],
        bzip2_base_ratio=results['401.bzip2_base_ratio'],
        bzip2_peak_ref=results['401.bzip2_peak_ref'],
        bzip2_peak_run=results['401.bzip2_peak_run'],
        bzip2_peak_ratio=results['401.bzip2_peak_ratio'],
        gcc_base_ref=results['403.gcc_base_ref'],
        gcc_base_run=results['403.gcc_base_run'],
        gcc_base_ratio=results['403.gcc_base_ratio'],
        gcc_peak_ref=results['403.gcc_peak_ref'],
        gcc_peak_run=results['403.gcc_peak_run'],
        gcc_peak_ratio=results['403.gcc_peak_ratio'],
        mcf_base_ref=results['429.mcf_base_ref'],
        mcf_base_run=results['429.mcf_base_run'],
        mcf_base_ratio=results['429.mcf_base_ratio'],
        mcf_peak_ref=results['429.mcf_peak_ref'],
        mcf_peak_run=results['429.mcf_peak_run'],
        mcf_peak_ratio=results['429.mcf_peak_ratio'],
        xalancbmk_base_ref=results['483.xalancbmk_base_ref'],
        xalancbmk_base_run=results['483.xalancbmk_base_run'],
        xalancbmk_base_ratio=results['483.xalancbmk_base_ratio'],
        xalancbmk_peak_ref=results['483.xalancbmk_peak_ref'],
        xalancbmk_peak_run=results['483.xalancbmk_peak_run'],
        xalancbmk_peak_ratio=results['483.xalancbmk_peak_ratio'],
        soplex_base_ref=results['450.soplex_base_ref'],
        soplex_base_run=results['450.soplex_base_run'],
        soplex_base_ratio=results['450.soplex_base_ratio'],
        soplex_peak_ref=results['450.soplex_peak_ref'],
        soplex_peak_run=results['450.soplex_peak_run'],
        soplex_peak_ratio=results['450.soplex_peak_ratio'],
        sphinx3_base_ref=results['482.sphinx3_base_ref'],
        sphinx3_base_run=results['482.sphinx3_base_run'],
        sphinx3_base_ratio=results['482.sphinx3_base_ratio'],
        sphinx3_peak_ref=results['482.sphinx3_peak_ref'],
        sphinx3_peak_run=results['482.sphinx3_peak_run'],
        sphinx3_peak_ratio=results['482.sphinx3_peak_ratio']
    )
    session.add(Open_SpecCpu)
    session.commit()


if duration_value.lower() == "seconds":
    duration = duration
elif duration_value.lower() == "minutes":
    duration = duration * 60
elif duration_value.lower() == "hours":
    duration = duration * 3600
elif duration_value.lower() == "days":
    duration = duration * 86400

# Collect information on the provider and VM environment
project_name = raw_input("\nPlease enter the project name: ")
project_name = project_name.lower()

provider_name = raw_input("\nPlease enter the provider name: ")
provider_name = provider_name.lower()

vm_name = raw_input("\nPlease enter the VM name (if no VM name, just say vCPU/RAM in GB (e.g., 2vCPU/4GB): ")
vm_name = vm_name.lower()

start_time = datetime.now().strftime('%Y%m%d-%H%M')
random_uid = randint(0, 1000000)
project_id = provider_name + vm_name + start_time + str(random_uid)

populate_db = confirm(prompt='\nSave test results in database?')

if populate_db:
    from db import Base, SpecCpu
    from db import Ignition
    from sqlalchemy.orm import sessionmaker

    # Bind Ignition to the metadata of the Base class
    Base.metadata.bind = Ignition
    DBSession = sessionmaker(bind=Ignition)
    session = DBSession()

iteration = 1
start = time.time()
os.system('mkdir /SPEC/CPU2006/output')
for x in range(iterations):
    stop = time.time() - start
    if stop >= duration:
        break
    # INTRODUCTION
    os.system('clear')
    results = {}
    print "|------------------------|"
    print "|     SPEC CPU 2006      |"
    print "|   Performance Tests    |"
    print "|------------------------|"
    print ""

    print "\nIteration: %s\n" % iteration

    results['start_time'] = datetime.now()
    results['start_time_formatted'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # RUN TEST SUITE
    print "\nExecuting SPEC CPU tests...\n"
    spec_tests = ['400.perlbench', '401.bzip2', '403.gcc', '429.mcf', '483.xalancbmk', '450.soplex', '482.sphinx3']
    run_test_suite()

    # PARSE TEST RESULTS
    print "\nParsing test results...\n"
    int_result_csv = 'CINT2006.001.ref.csv'
    fp_result_csv = 'CFP2006.001.ref.csv'

    os.system('cp /SPEC/CPU2006/result/%s /SPEC/CPU2006/output/%s_%s_INT.csv' % (int_result_csv, project_id, iteration))
    os.system('cp /SPEC/CPU2006/result/%s /SPEC/CPU2006/output/%s_%s_FP.csv' % (fp_result_csv, project_id, iteration))
    parse_test_results()
    os.system('rm -rf /SPEC/CPU2006/result')

    if populate_db:
        # SAVE RESULTS IN DATABASE
        print "\nTransmitting to Database...\n"
        save_test_results()

    iteration += 1

print "\nSPEC CPU tests are completed successfully.\n"
