
import re
import json
import os

def generate_sql_lines(endpoint_dir):
	case_des_list = []
	case_mode_list = []
	order_metadata_list = []
	json_dir = os.path.join(endpoint_dir, "data")

	for file in os.listdir(endpoint_dir):
		if str(file).endswith(".yaml"):
			filename = file.split('.')[0]
			yaml_file = os.path.join(endpoint_dir, file)
			json_file = os.path.join(endpoint_dir+'/data', filename+'.json')
			with open(yaml_file, 'r') as f:
				yaml_lines = f.readlines()
				for ln in yaml_lines:
					found = re.search("case_description", ln.strip())
					if found:
						case_des = ln.split(": ")[1]
						# print(case_des)
						case_des_list.append(case_des.strip())
						break

			with open(json_file, 'r') as jsonf:
				json_content = json.load(jsonf)
				case_mode = json_content['mode']
				# print(case_mode)
				case_mode_list.append(case_mode)
				json_str = json.dumps(json_content)
				order_metadata_list.append(json_str)
				# print(len(case_mode_list))
	return case_des_list, case_mode_list, order_metadata_list


if __name__ == "__main__":
	cases_sql_file = "cases_sql.txt"
	order_detail_sql_file = "order_detail_sql.txt"
	sourceDir = "/Users/.../food_cms/collections"
	# generate_sql_lines(sourceDir)

	des_list, mode_list, metadata_list = generate_sql_lines(sourceDir)
	list_len = len(mode_list)
	# print(des_list)
	# print(mode_list)


	with open(cases_sql_file, 'w') as f:
		for i in range(list_len):
			f.write("(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\'),\n".format('', des_list[i], 'pending', mode_list[i], 'Deliveries', 'OM', 'pre_e2e', 'core_food'))

	with open(order_detail_sql_file, 'w') as detailf:
		for i in metadata_list:
			detailf.write("(\'{}\',\'{}\'),\n".format('', i))
