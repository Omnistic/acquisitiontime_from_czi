import os
import re
import pickle
import dateutil.parser
import time

CHUNK_SIZE_IN_BYTES = 1000000000
CHUNK_OVERLAP_SIZE = 44

def get_acquisition_times_from_large_file(czi_filepath, acquisition_times_filepath):
    binary_acquisition_times = []
    ii = 1

    with open(czi_filepath, 'rb') as f:
        chunk = f.read(CHUNK_SIZE_IN_BYTES)
        chunk_overlap = f.read(CHUNK_OVERLAP_SIZE)

        while True:
            start_time = time.time()

            if chunk == b'':
                break

            binary_acquisition_times.extend(re.findall(b'<AcquisitionTime>(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+Z)', chunk))

            chunk = chunk_overlap + f.read(CHUNK_SIZE_IN_BYTES)
            chunk_overlap = f.read(CHUNK_OVERLAP_SIZE)
            chunk += chunk_overlap
            
            ii += 1
            print('{0} GB done (interval: {1:.2f}s)'.format(ii, time.time() - start_time))
            
    adcquisition_times = [dateutil.parser.isoparse(dt.decode()) for dt in binary_acquisition_times]
    
    with open(acquisition_times_filepath, 'wb') as f:
        pickle.dump(adcquisition_times, f)

if __name__ == '__main__':
    czi_filepath = r'your_file.czi'

    acquisition_times_filepath = czi_filepath.replace('.czi', '.pkl')

    if not os.path.isfile(acquisition_times_filepath):
        get_acquisition_times_from_large_file(czi_filepath, acquisition_times_filepath)

    with open(acquisition_times_filepath, 'rb') as file:
        acquisition_times = pickle.load(file)
