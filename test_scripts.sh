mkdir -p test-output
mkdir -p test-output/test-books
mkdir -p test-output/test-reviews
mkdir -p test-output/test-bookshelf

python get_books.py --book_ids_path test_book_ids.txt --output_directory_path test-output/test-books

python get_reviews.py --book_ids_path test_book_ids.txt --output_directory_path test-output/test-reviews --sort_order 0 --browser firefox

python get_books.py --l --user_id 7362767 --shelf_name goats --output_directory_path test-output/test-bookshelf