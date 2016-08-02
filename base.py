from conf import *
from random import randint
from datetime import datetime
import os
import csv
import time
import shutil
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
    v1 = sub.Popen(['cat', '/proc/cpuinfo'], stdout=sub.PIPE)
    v2 = sub.Popen(['grep', 'processor'], stdin=v1.stdout, stdout=sub.PIPE)
    v3 = sub.Popen(['wc', '-l'], stdin=v2.stdout, stdout=sub.PIPE)
    cpu_count = v3.communicate()[0]
    cpu_count = str(cpu_count)
    spec_cmd = ['runspec', '--config', 'spec_test_config.cfg', '--tune', 'all', '--rate', cpu_count, '--noreportable',
                '--output_format', 'csv', '--iterations', '1']
    spec_cmd.extend(spec_tests)
    sub.call(spec_cmd)


def parse_test_results():
    """
    Parse SPEC CPU test results
    """
    os.chdir(spec_result_dir)

    for csv_result in csv_results:
        with open(csv_result, 'rb') as f:
            csv_handler = csv.reader(f)
            for row in csv_handler:
                for item in spec_tests:
                    if item in row:
                        results["%s_base_copies" % item] = row[1] if row[1] is not None else ''
                        results["%s_base_runtime" % item] = row[2] if row[2] is not None else ''
                        results["%s_base_rate" % item] = row[3] if row[3] is not None else ''
                        results["%s_peak_copies" % item] = row[6] if row[6] is not None else ''
                        results["%s_peak_runtime" % item] = row[7] if row[7] is not None else ''
                        results["%s_peak_rate" % item] = row[8] if row[8] is not None else ''
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
        perlbench_base_copies=results['400.perlbench_base_copies'],
        perlbench_base_runtime=results['400.perlbench_base_runtime'],
        perlbench_base_rate=results['400.perlbench_base_rate'],
        perlbench_peak_copies=results['400.perlbench_peak_copies'],
        perlbench_peak_runtime=results['400.perlbench_peak_runtime'],
        perlbench_peak_rate=results['400.perlbench_peak_rate'],
        bzip2_base_copies=results['401.bzip2_base_copies'],
        bzip2_base_runtime=results['401.bzip2_base_runtime'],
        bzip2_base_rate=results['401.bzip2_base_rate'],
        bzip2_peak_copies=results['401.bzip2_peak_copies'],
        bzip2_peak_runtime=results['401.bzip2_peak_runtime'],
        bzip2_peak_rate=results['401.bzip2_peak_rate'],
        gcc_base_copies=results['403.gcc_base_copies'],
        gcc_base_runtime=results['403.gcc_base_runtime'],
        gcc_base_rate=results['403.gcc_base_rate'],
        gcc_peak_copies=results['403.gcc_peak_copies'],
        gcc_peak_runtime=results['403.gcc_peak_runtime'],
        gcc_peak_rate=results['403.gcc_peak_rate'],
        mcf_base_copies=results['429.mcf_base_copies'],
        mcf_base_runtime=results['429.mcf_base_runtime'],
        mcf_base_rate=results['429.mcf_base_rate'],
        mcf_peak_copies=results['429.mcf_peak_copies'],
        mcf_peak_runtime=results['429.mcf_peak_runtime'],
        mcf_peak_rate=results['429.mcf_peak_rate'],
        xalancbmk_base_copies=results['483.xalancbmk_base_copies'],
        xalancbmk_base_runtime=results['483.xalancbmk_base_runtime'],
        xalancbmk_base_rate=results['483.xalancbmk_base_rate'],
        xalancbmk_peak_copies=results['483.xalancbmk_peak_copies'],
        xalancbmk_peak_runtime=results['483.xalancbmk_peak_runtime'],
        xalancbmk_peak_rate=results['483.xalancbmk_peak_rate'],
        soplex_base_copies=results['450.soplex_base_copies'],
        soplex_base_runtime=results['450.soplex_base_runtime'],
        soplex_base_rate=results['450.soplex_base_rate'],
        soplex_peak_copies=results['450.soplex_peak_copies'],
        soplex_peak_runtime=results['450.soplex_peak_runtime'],
        soplex_peak_rate=results['450.soplex_peak_rate'],
        sphinx3_base_copies=results['482.sphinx3_base_copies'],
        sphinx3_base_runtime=results['482.sphinx3_base_runtime'],
        sphinx3_base_rate=results['482.sphinx3_base_rate'],
        sphinx3_peak_copies=results['482.sphinx3_peak_copies'],
        sphinx3_peak_runtime=results['482.sphinx3_peak_runtime'],
        sphinx3_peak_rate=results['482.sphinx3_peak_rate']
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

vm_name = raw_input("\nPlease enter the VM name (if no VM name, just say vCPU_RAM (e.g., 2vCPU_4GB): ")
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


spec_tests = ['400.perlbench', '401.bzip2', '403.gcc', '429.mcf', '483.xalancbmk', '450.soplex', '482.sphinx3']

spec_result_dir = '/SPEC/CPU2006/result'
spec_output_dir = '/SPEC/CPU2006/output'
int_result_csv = 'CINT2006.001.ref.csv'
fp_result_csv = 'CFP2006.001.ref.csv'
csv_results = [int_result_csv, fp_result_csv]

if os.path.exists(spec_result_dir):
    shutil.rmtree(spec_result_dir)

if not os.path.exists(spec_output_dir):
    os.makedirs(spec_output_dir)

iteration = 1
start = time.time()
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
    run_test_suite()

    # PARSE TEST RESULTS
    print "\nParsing test results...\n"
    os.system('cp %s/%s %s/%s_%s_INT.csv' % (spec_result_dir, int_result_csv, spec_output_dir, project_id, iteration))
    os.system('cp %s/%s %s/%s_%s_FP.csv' % (spec_result_dir, fp_result_csv, spec_output_dir, project_id, iteration))
    parse_test_results()
    shutil.rmtree(spec_result_dir)

    if populate_db:
        # SAVE RESULTS IN DATABASE
        print "\nTransmitting to Database...\n"
        save_test_results()

    iteration += 1

print "\nSPEC CPU tests are completed successfully.\n"
