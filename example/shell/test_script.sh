mkdir -p user_io/test_output/book
mkdir -p user_io/test_output/review

echo 'TESTING COLLECT BOOK METADATA:'
echo '==========================\n'
python main.py -s book --book_ids_path example/data/goodreads_classics_sample.txt --output_directory_path user_io/test_output/book -f csv

echo 'TESTING GENERATE BOOK ID TITLES:'
echo '================================\n'
python main.py -s book_id -f csv

echo 'TESTING COLLECT BOOK REVIEWS:'
echo '=========================\n'
python main.py -s review --book_ids_path example/data/goodreads_classics_sample.txt --output_directory_path user_io/test_output/review --browser firefox --sort_order default  --format csv
