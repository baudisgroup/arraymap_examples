from pymongo import MongoClient
import json
import click
import os
import shutil

client = MongoClient()
db = client['arraymap']



@click.command()
@click.option('-l', '--list', 'file_idlist', default='./id_list.txt', help='A text file containing a list of biosample IDs')
@click.option('-o', '--out', 'output_folder', default='./examples', help='The output folder')
def cli(file_idlist, output_folder):


	try:
		shutil.rmtree(output_folder)
	except Exception as e:
		print(e)
	# check output folder
	if not os.path.isdir(output_folder):
		os.makedirs(output_folder)


	## Generate biosamples
	list = []
	id_list = []
	collection = db['biosamples']
	fout = os.path.join(output_folder, 'biosamples.json')
	with open(file_idlist, 'r') as fin:
		for line in fin:
			id_list.append('PGX_AM_BS_' + line.strip())

	query = "{'id': {'$in':" + str(id_list) + "}}"

	with open(fout, 'w') as fo:
		for doc in collection.find(eval(query),{'_id': 0, 'updated':0}):
			list.append(doc)
		json.dump(list, fo, sort_keys=True, indent=4)




	## Generate individuals
	list = []
	id_list = []
	collection = db['individuals']
	fout = os.path.join(output_folder, 'individuals.json')
	with open(file_idlist, 'r') as fin:
		for line in fin:
			id_list.append('PGX_IND_' + line.strip())

	query = "{'id': {'$in':" + str(id_list) + "}}"

	with open(fout, 'w') as fo:
		for doc in collection.find(eval(query),{'_id': 0,  'updated':0}):
			list.append(doc)
		json.dump(list, fo, sort_keys=True, indent=4)






	## Generate callsets
	list = []
	id_list = []
	name = 'callsets'
	collection = db[name]
	fout = os.path.join(output_folder, name+'.json')
	with open(file_idlist, 'r') as fin:
		for line in fin:
			id_list.append('PGX_AM_BS_' + line.strip())

	query = "{'biosample_id': {'$in':" + str(id_list) + "}}"

	with open(fout, 'w') as fo:
		for doc in collection.find(eval(query),{'_id': 0, 'updated':0, 'info.statusmaps':0}):
			list.append(doc)
		json.dump(list, fo, sort_keys=True, indent=4)





	## Generate variants

	list = []
	id_list = []
	name = 'variants'
	collection = db[name]
	fout = os.path.join(output_folder, name+'.json')
	with open(file_idlist, 'r') as fin:
		for line in fin:
			id_list.append('PGX_AM_BS_' + line.strip())

	query = "{'biosample_id': {'$in':" + str(id_list) + "}}"

	with open(fout, 'w') as fo:
		for doc in collection.find(eval(query),{'_id': 0, 'created': 0, 'updated':0}):
			if doc not in list:
				list.append(doc)
		json.dump(list, fo, sort_keys=True, indent=4)


# main
if __name__ == '__main__':
    cli()