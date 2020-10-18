cần cài các package python:

	pip install pandas
	pip install numpy


run: 
	python splitAddress.py


đợi khi nào chạy hết mới ra kết quả.


cần xóa file output.csv trước, chạy mới được






dòng 389




2670/8093 = 0.33

33% ở thành phố hồ chí minh thiếu phường

dùng open street map còn được 260
URL = "https://nominatim.openstreetmap.org/reverse?format=json&lat=" + lat + "&lon=" + lon  + "&zoom=18&addressdetails=1"


#cấu trúc openstreet map không ổn định, nên một vài trường hợp chưa cover hết
https://nominatim.openstreetmap.org/reverse?format=json&lat=10.74408436&lon=106.62205505&zoom=18&addressdetails=1
https://nominatim.openstreetmap.org/reverse?format=json&lat=10.69777298&lon=106.60936737&zoom=18&addressdetails=1
https://nominatim.openstreetmap.org/reverse?format=json&lat=10.72649097&lon=106.72059631&zoom=18&addressdetails=1
