# this file can be used to concat the files when the conversion is done/
# this is useful to avoid the memory issues when reading large files
#! bash
output_path="../data/foursquare.csv"
cat "../data/converted/places/places-00000.csv" >$output_path
for i in $(seq 1 99); do
    csv_path="../data/converted/places/places-$(printf "%05d" $i).csv"
    echo "Processing $csv_path"
    sed -n '2,$p' $csv_path >>$output_path
done
