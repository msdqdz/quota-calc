from datetime import datetime, timedelta
import time

def format_size(size_in_mb):
    """Format ukuran dalam MB, GB, atau KB"""
    if size_in_mb >= 1024:
        size_in_gb = size_in_mb / 1024
        return f"{size_in_gb:.2f}GB"
    elif size_in_mb >= 1:
        return f"{size_in_mb:.2f}MB"
    else:
        size_in_kb = size_in_mb * 1024
        return f"{size_in_kb:.2f}KB"

def countdown_and_quota(target_datetime, total_quota):
    start_time = datetime.now()
    duration = target_datetime - start_time
    total_seconds = duration.total_seconds()
    quota_per_second = total_quota / total_seconds
    quota_per_minute = quota_per_second * 60
    quota_per_hour = quota_per_minute * 60

    while True:
        now = datetime.now()
        remaining_time = target_datetime - now
        
        if remaining_time <= timedelta(0):
            print("Waktu habis!")
            break
        
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        elapsed_seconds = (now - start_time).total_seconds()
        used_quota = elapsed_seconds * quota_per_second
        
        if used_quota > total_quota:
            used_quota = total_quota
        
        remaining_quota = total_quota - used_quota
        
        # Menentukan format output berdasarkan waktu sisa
        if remaining_time.total_seconds() >= 3600:  # Lebih dari 1 jam
            formatted_usage = f"{format_size(quota_per_minute)}/mnt ({format_size(quota_per_hour)}/jam)"
        elif remaining_time.total_seconds() >= 60:  # Lebih dari 1 menit
            formatted_usage = f"{format_size(quota_per_second)}/s ({format_size(quota_per_minute)}/mnt)"
        else:  # Kurang dari 1 menit
            formatted_usage = f"{format_size(quota_per_second)}/s"
        
        formatted_used_quota = format_size(used_quota)
        formatted_total_quota = format_size(total_quota)
        
        # Menampilkan output
        print(f"Wkt mundur: {days:02}:{hours:02}:{minutes:02}:{seconds:02} | "
              f"Kuota: {formatted_used_quota}/{formatted_total_quota} | "
              f"{formatted_usage}", end='\r')
        time.sleep(1)

def show_tutorial():
    """Menampilkan tutorial penggunaan program"""
    print("\nTutorial Penggunaan Program")
    print("1. Jalankan program.")
    print("2. Pilih opsi 1 untuk menghitung penggunaan kuota atau opsi 2 untuk membaca tutorial ini.")
    print("3. Jika memilih opsi 1:")
    print("   - Masukkan tanggal dan waktu target dalam format YYYY-MM-DD HH:MM:SS.")
    print("   - Masukkan total kuota internet dalam MB.")
    print("   - Program akan menghitung dan menampilkan waktu mundur serta penggunaan kuota.")
    print("4. Output program akan menampilkan:")
    print("   - Waktu mundur dalam format: day:hour:minute:second.")
    print("   - Kuota yang digunakan dan total kuota dalam format yang sesuai (MB, GB, atau KB).")
    print("   - Penggunaan kuota per detik, per menit, atau per jam tergantung pada sisa waktu.")
    print("5. Setelah waktu habis, program akan menampilkan 'Waktu habis!' dan berhenti.")

def main():
    while True:
        print("\nSelamat datang!")
        print("Pilih menu:")
        print("1. Hitung penggunaan kuota")
        print("2. Tutorial")
        print("3. Keluar")
        
        choice = input("Masukkan pilihan (1/2/3): ")
        
        if choice == '1':
            target_input = input("Masukkan tanggal dan jam (format: YYYY-MM-DD HH:MM:SS): ")
            
            try:
                target_datetime = datetime.strptime(target_input, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print("Format tanggal dan jam salah. Harap gunakan format: YYYY-MM-DD HH:MM:SS")
                continue
            
            total_quota = float(input("Masukkan total kuota internet (dalam MB): "))
            
            countdown_and_quota(target_datetime, total_quota)
        
        elif choice == '2':
            show_tutorial()
        
        elif choice == '3':
            print("Terima kasih telah menggunakan program ini.")
            break
        
        else:
            print("Pilihan tidak valid. Harap pilih 1, 2, atau 3.")

if __name__ == "__main__":
    main()
