for collection in biosamples individuals callsets variants
do
 mongoimport --db arraymapexamples --collection $collection --drop --file ./examples/$collection.json --jsonArray
done