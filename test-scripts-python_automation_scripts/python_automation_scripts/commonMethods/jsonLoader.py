import json


class jsonLoader:
	
	def json_read(path):
		filename = path
		jsonContent = json.loads(open(filename).read())
		return jsonContent

	def json_write(data):
		with open('D://test_scripts_python_2//config//data.json', 'w') as outfile:
			outfile.write(json.dumps(data, sort_keys=True, indent=4))
			outfile.close()

	def write_vouchers(data):
		with open('D://test_scripts_python_2//config//usedVouchers.json', 'w') as outfile:
			outfile.write(json.dumps(data, sort_keys=True, indent=4))
			outfile.close()