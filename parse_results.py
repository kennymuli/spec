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
    os.chdir(spec_output_dir)

    try:
        for csv_result in csv_results:
            for item in spec_tests:
                with open(csv_result, 'rb') as f:
                    csv_handler = csv.reader(f)
                    for row in csv_handler:
                        if item in row:
                            results["%s_base_copies" % item] = row[1] if row[1] is not None else ''
                            results["%s_base_runtime" % item] = row[2] if row[2] is not None else ''
                            results["%s_base_rate" % item] = row[3] if row[3] is not None else ''
                            results["%s_peak_copies" % item] = row[6] if row[6] is not None else ''
                            results["%s_peak_runtime" % item] = row[7] if row[7] is not None else ''
                            results["%s_peak_rate" % item] = row[8] if row[8] is not None else ''
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


# Collect information on the provider and VM environment
project_name = raw_input("\nPlease enter the project name: ")
project_name = project_name.lower()

provider_name = raw_input("\nPlease enter the provider name: ")
provider_name = provider_name.lower()

vm_name = raw_input("\nPlease enter the VM name (if no VM name, just say vCPU/RAM in GB (e.g., 2vCPU/4GB): ")
vm_name = vm_name.lower()

project_id = raw_input("\nPlease enter the project id: ")

spec_tests = ['400.perlbench', '401.bzip2', '403.gcc', '429.mcf', '483.xalancbmk', '450.soplex', '482.sphinx3']
spec_output_dir = '/SPEC/CPU2006/output'

iteration = 1
for x in range(iterations):
    results = {}
    int_result_csv = '%s_%s_INT.csv' % (project_id, iteration)
    fp_result_csv = '%s_%s_FP.csv' % (project_id, iteration)
    csv_results = [int_result_csv, fp_result_csv]
    parse_test_results()
    save_test_results()
    iteration += 1

print "\nSPEC CPU results are parsed and saved to database.\n"
