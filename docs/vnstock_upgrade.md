# Nguồn dữ liệu thị trường cho giao diện

## Cài đặt

```powershell
py -3.13 -m pip install -r requirements.txt
```

File requirements đã chứa `--extra-index-url https://vnstocks.com/api/simple`. Nếu chỉ nâng hai gói trong môi trường hiện có, dùng:

```powershell
py -3.13 -m pip install --upgrade --extra-index-url https://vnstocks.com/api/simple vnstock==4.0.9 vnai==2.6.2
```

Ứng dụng đọc OHLCV từ VCI hoặc KBS. Giá cổ phiếu có đơn vị nghìn đồng, còn VN-Index có đơn vị điểm. Snapshot dùng trong nghiên cứu giữ phiên bản nguồn và ngày lấy dữ liệu đã ghi trong manifest.
