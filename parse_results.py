from conf import *
import os
import csv
from db import Base, SpecCpu
from db import Ignition
from sqlalchemy.orm import sessionmaker

# Bind Ignition to the metadata of the Base class
Base.metadata.bind = Ignition
DBSession = sessionmaker(bind=Ignition)
session = DBSession()


def parse_test_results():
    """
    Parse SPEC CPU test results
    """
    os.chdir('/SPEC/CPU2006/output')

    try:
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
        return
    except Exception as e:
        raise e


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
        start_time='-',
        end_time='-',
        test_duration='-',
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


# Collect information on the provider and VM environment
project_name = raw_input("\nPlease enter the project name: ")
project_name = project_name.lower()

provider_name = raw_input("\nPlease enter the provider name: ")
provider_name = provider_name.lower()

vm_name = raw_input("\nPlease enter the VM name (if no VM name, just say vCPU/RAM in GB (e.g., 2vCPU/4GB): ")
vm_name = vm_name.lower()

project_id = raw_input("\nPlease enter the project id: ")

spec_tests = ['400.perlbench', '401.bzip2', '403.gcc', '429.mcf', '483.xalancbmk', '450.soplex', '482.sphinx3']
iteration = 1
for x in range(iterations):
    results = {}
    int_result_csv = '%s_%s_INT.csv' % (project_id, iteration)
    fp_result_csv = '%s_%s_FP.csv' % (project_id, iteration)
    parse_test_results()
    save_test_results()
    iteration += 1

print "\nSPEC CPU results are parsed and saved to database.\n"
