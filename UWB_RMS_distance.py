import math
from demo_to_python import main

def func():
	data_blocks = main()[0]
	#print(data_blocks, type(data_blocks))

	# Provided list of data blocks
	#data_blocks = test1
		#[
	    #{'nLos': 0, 'distance': 7, 'aoa_azimuth': -12.89, 'aoa_elevation': 7.88},
	    #{'nLos': 1, 'distance': 6, 'aoa_azimuth': -10.81, 'aoa_elevation': 7.48},
	    #{'nLos': 0, 'distance': 14, 'aoa_azimuth': -12.89, 'aoa_elevation': 6.9},
	    #{'nLos': 0, 'distance': 12, 'aoa_azimuth': -12.109, 'aoa_elevation': 8.92},
	    #{'nLos': 1, 'distance': 11, 'aoa_azimuth': -13.79, 'aoa_elevation': 8.21},
	    #{'nLos': 0, 'distance': 12, 'aoa_azimuth': -11.56, 'aoa_elevation': 8.75}
	#

	#([{'nLos': 0, 'distance': 11, 'aoa_azimuth': 26.47, 'aoa_elevation': -15.102}, {'nLos': 0, 'distance': 18, 'aoa_azimuth': 24.118, 'aoa_elevation': -15.8}, {'nLos': 0, 'distance': 13, 'aoa_azimuth': 26.117, 'aoa_elevation': -18.97}, {'nLos': 0, 'distance': 13, 'aoa_azimuth': 25.11, 'aoa_elevation': -16.26}, {'nLos': 0, 'distance': 14, 'aoa_azimuth': 26.21, 'aoa_elevation': -15.111}, {'nLos': 0, 'distance': 12, 'aoa_azimuth': 25.104, 'aoa_elevation': -15.123}, {'nLos': 0, 'distance': 18, 'aoa_azimuth': 26.31, 'aoa_elevation': -15.11}, {'nLos': 0, 'distance': 16, 'aoa_azimuth': 26.43, 'aoa_elevation': -16.27}, {'nLos': 0, 'distance': 17, 'aoa_azimuth': 26.92, 'aoa_elevation': -15.26}, {'nLos': 0, 'distance': 19, 'aoa_azimuth': 25.25, 'aoa_elevation': -16.62}, {'nLos': 0, 'distance': 13, 'aoa_azimuth': 26.114, 'aoa_elevation': -15.12}, {'nLos': 0, 'distance': 14, 'aoa_azimuth': 26.9, 'aoa_elevation': -17.75}, {'nLos': 0, 'distance': 15, 'aoa_azimuth': 27.56, 'aoa_elevation': -16.47}, {'nLos': 0, 'distance': 15, 'aoa_azimuth': 24.115, 'aoa_elevation': -18.83}], 14)
	def compute_rms(values):
	    """Compute the root mean square of a list of numbers."""
	    n = len(values)
	    if n == 0:
	        return 0
	    return math.sqrt(sum(x**2 for x in values) / n)

	# Extract each parameter across all blocks
	try:
			distances = [block['distance'] for block in data_blocks]
			aoa_azimuths = [block['aoa_azimuth'] for block in data_blocks]
			aoa_elevations = [block['aoa_elevation'] for block in data_blocks]
	except:
		print("Not working")
		exit()

	# Compute RMS for each parameter

	rms_distance = compute_rms(distances)
	rms_azimuth = compute_rms(aoa_azimuths)
	rms_elevation = compute_rms(aoa_elevations)

	# Create a single list with the three RMS values
	rms_results = [rms_distance, rms_azimuth, rms_elevation]

	#print("RMS values:")
	#print("Distance RMS:", rms_distance)
	#print("AOA Azimuth RMS:", rms_azimuth)
	#print("AOA Elevation RMS:", rms_elevation)
	print(rms_results)
	return rms_results

func()
