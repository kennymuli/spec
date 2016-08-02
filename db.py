from sqlalchemy import Column, Integer, String, Float, create_engine, __version__
from sqlalchemy.ext.declarative import declarative_base

# Check which version of SQLAlchemy is currently being used.
print "SQLAlchemy Version: " + __version__
Base = declarative_base()


class SpecCpu(Base):
    __tablename__ = 'spec_cpu'
    id = Column(Integer, primary_key=True)
    project_id = Column(String(30), nullable=True)
    project = Column(String(30), nullable=True)
    provider = Column(String(30), nullable=True)
    instance_type = Column(String(30), nullable=True)
    iteration = Column(Integer, nullable=False)
    start_time = Column(String(20), nullable=False)
    end_time = Column(String(20), nullable=False)
    test_duration = Column(String(20), nullable=False)
    perlbench_base_copies = Column(String(20), nullable=False)
    perlbench_base_runtime = Column(String(20), nullable=False)
    perlbench_base_rate = Column(String(20), nullable=False)
    perlbench_peak_copies = Column(String(20), nullable=False)
    perlbench_peak_runtime = Column(String(20), nullable=False)
    perlbench_peak_rate = Column(String(20), nullable=False)
    bzip2_base_copies = Column(String(20), nullable=False)
    bzip2_base_runtime = Column(String(20), nullable=False)
    bzip2_base_rate = Column(String(20), nullable=False)
    bzip2_peak_copies = Column(String(20), nullable=False)
    bzip2_peak_runtime = Column(String(20), nullable=False)
    bzip2_peak_rate = Column(String(20), nullable=False)
    gcc_base_copies = Column(String(20), nullable=False)
    gcc_base_runtime = Column(String(20), nullable=False)
    gcc_base_rate = Column(String(20), nullable=False)
    gcc_peak_copies = Column(String(20), nullable=False)
    gcc_peak_runtime = Column(String(20), nullable=False)
    gcc_peak_rate = Column(String(20), nullable=False)
    mcf_base_copies = Column(String(20), nullable=False)
    mcf_base_runtime = Column(String(20), nullable=False)
    mcf_base_rate = Column(String(20), nullable=False)
    mcf_peak_copies = Column(String(20), nullable=False)
    mcf_peak_runtime = Column(String(20), nullable=False)
    mcf_peak_rate = Column(String(20), nullable=False)
    xalancbmk_base_copies = Column(String(20), nullable=False)
    xalancbmk_base_runtime = Column(String(20), nullable=False)
    xalancbmk_base_rate = Column(String(20), nullable=False)
    xalancbmk_peak_copies = Column(String(20), nullable=False)
    xalancbmk_peak_runtime = Column(String(20), nullable=False)
    xalancbmk_peak_rate = Column(String(20), nullable=False)
    soplex_base_copies = Column(String(20), nullable=False)
    soplex_base_runtime = Column(String(20), nullable=False)
    soplex_base_rate = Column(String(20), nullable=False)
    soplex_peak_copies = Column(String(20), nullable=False)
    soplex_peak_runtime = Column(String(20), nullable=False)
    soplex_peak_rate = Column(String(20), nullable=False)
    sphinx3_base_copies = Column(String(20), nullable=False)
    sphinx3_base_runtime = Column(String(20), nullable=False)
    sphinx3_base_rate = Column(String(20), nullable=False)
    sphinx3_peak_copies = Column(String(20), nullable=False)
    sphinx3_peak_runtime = Column(String(20), nullable=False)
    sphinx3_peak_rate = Column(String(20), nullable=False)


# Create an object, db, to act as the connect to the database.
# The SQLEngine object is used to open the connection, which is what is being used in the db variable.
# Format for create_engine is "engine://user:password@host:port/database"
Ignition = create_engine("mysql://root:inapp@localhost:3306/performance_tests")

# Holds all the database metadata.
Base.metadata.create_all(Ignition)
