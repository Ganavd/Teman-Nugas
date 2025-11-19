import os
import sys
import time
import datetime
import winsound
import tkinter as tk
from tkinter import messagebox
import threading

DATA = "data"
if not os.path.exists(DATA):
    os.makedirs(DATA)

FILE_SELESAI = os.path.join(DATA, "tugas_selesai.txt")
FILE_BELUM = os.path.join(DATA, "tugas_belum.txt")

tugas_list = []
stop_thread = False

def typewriter(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def garis():
    print("=" * 50)


def header():
    clear_screen()
    garis()
    print("📘  SELAMAT DATANG DI TEMAN NUGAS")
    print("💡  Semangat menyelesaikan tugasmu!")
    garis()


def simpan_status(nama_tugas, status, waktu=None):
    nama_file = FILE_SELESAI if status == "selesai" else FILE_BELUM
    if waktu is None:
        waktu = datetime.datetime.now()
    with open(nama_file, "a", encoding="utf-8") as file:
        waktu = waktu.strftime("%d-%m-%Y %H:%M")
        file.write(f"{waktu} | {nama_tugas}\n")


def hatihati():
    for _ in range(1):
        winsound.Beep(1500, 1000)
    for _ in range(2):
        winsound.Beep(1500, 500)


def gawat():
    for _ in range(3):
        winsound.Beep(2000, 1200)


def habis():
    for _ in range(5):
        winsound.Beep(2000, 500)


def notifikasi_deadline_loop():
    global stop_thread

    while not stop_thread:
        now = datetime.datetime.now()

        for tugas in list(tugas_list):
            if tugas.get("handled", False):
                continue

            nama = tugas["nama"]
            deadline = tugas["deadline"]
            s2 = tugas["s2"]
            s1 = tugas["s1"]
            popup_shown = tugas.get("popup_shown", False)
            selisih = (deadline - now).total_seconds()

            if 300 < selisih <= 3600 and not s2:
                print(f"\n⚠️  [Peringatan] Tugas '{nama}' tinggal kurang dari 1 jam lagi!")
                try:
                    hatihati()
                    hatihati()
                except:
                    pass
                time.sleep(1)
                tugas["s2"] = True

            elif 0 < selisih <= 300 and not s1:
                print(f"\n⏰  [NOTIF] Tugas '{nama}' tinggal kurang dari 5 menit lagi!")
                try:
                    gawat()
                except:
                    pass
                time.sleep(1)
                tugas["s1"] = True

            if selisih <= 0 and not popup_shown and not tugas.get("handled", False):
                tugas["overdue"] = True
                tugas["popup_shown"] = True

                try:
                    habis()
                except:
                    pass

                def show_popup(t):

                    clear_screen()
                    garis()
                    print(f"⏰ TUGAS '{t['nama'].upper()}' WAKTUNYA KONFIRMASI!")
                    print("⚠️  Harap segera konfirmasi melalui popup yang muncul.")
                    garis()
                    print("\n(Mohon maaf, layar di-clear untuk mencegah duplikasi data.)\n")

                    time.sleep(1)

                    root = tk.Tk()
                    root.title("⏰ Waktu Tugas Habis")

                    w, h = 420, 220
                    sw = root.winfo_screenwidth()
                    sh = root.winfo_screenheight()
                    x = int((sw - w) / 2)
                    y = int((sh - h) / 2)
                    root.geometry(f"{w}x{h}+{x}+{y}")
                    root.configure(bg="#fff5e1")

                    label = tk.Label(
                        root,
                        text=f"⏰ Waktu untuk tugas:\n\n{t['nama'].upper()}\n\nApakah sudah selesai?",
                        bg="#fff5e1",
                        font=("Segoe UI", 12, "bold")
                    )
                    label.pack(pady=20)

                    def selesai():
                        simpan_status(t["nama"], "selesai")
                        t["handled"] = True
                        try:
                            tugas_list.remove(t)
                        except:
                            pass

                        msg_root = tk.Tk()
                        msg_root.title("🎉 Selamat!")

                        w, h = 400, 200
                        sw = msg_root.winfo_screenwidth()
                        sh = msg_root.winfo_screenheight()
                        x = int((sw - w) / 2)
                        y = int((sh - h) / 2)
                        msg_root.geometry(f"{w}x{h}+{x}+{y}")
                        msg_root.configure(bg="#e6f7ff")

                        label = tk.Label(
                            msg_root,
                            text="🎉 Selamat!\nKamu telah menyelesaikan tugas tepat waktu!",
                            bg="#e6f7ff",
                            font=("Segoe UI", 12, "bold"),
                            justify="center",
                            wraplength=350
                        )
                        label.pack(pady=20)

                        btn = tk.Button(
                            msg_root,
                            text="OK",
                            bg="#b6d7a8",
                            width=10,
                            command=lambda: [msg_root.destroy(), root.destroy()]
                        )
                        btn.pack(pady=10)

                        msg_root.mainloop()


                    def belum():
                        simpan_status(t["nama"], "belum")
                        t["handled"] = True
                        try:
                            tugas_list.remove(t)
                        except:
                            pass

                        msg_root = tk.Tk()
                        msg_root.title("⚠️ Belum Selesai")

                        w, h = 400, 200
                        sw = msg_root.winfo_screenwidth()
                        sh = msg_root.winfo_screenheight()
                        x = int((sw - w) / 2)
                        y = int((sh - h) / 2)
                        msg_root.geometry(f"{w}x{h}+{x}+{y}")
                        msg_root.configure(bg="#fff5e1")

                        label = tk.Label(
                            msg_root,
                            text="⚠️ Kamu belum menyelesaikan tugas ini.\nJangan menyerah! Segera selesaikan ya!",
                            bg="#fff5e1",
                            font=("Segoe UI", 12, "bold"),
                            justify="center",
                            wraplength=350
                        )
                        label.pack(pady=20)

                        btn = tk.Button(
                            msg_root,
                            text="OK",
                            bg="#f4cccc",
                            width=10,
                            command=lambda: [msg_root.destroy(), root.destroy()]
                        )
                        btn.pack(pady=10)

                        msg_root.mainloop()

                    frame = tk.Frame(root, bg="#fff5e1")
                    frame.pack()
                    tk.Button(frame, text="Sudah", bg="#b6d7a8", width=10, command=selesai).grid(row=0, column=0, padx=10)
                    tk.Button(frame, text="Belum", bg="#f4cccc", width=10, command=belum).grid(row=0, column=1, padx=10)

                    root.mainloop()

                show_popup(tugas)

        time.sleep(1)


def tambah_tugas():
    print("\n📝 TAMBAH TUGAS BARU")
    garis()

    nama = input("📘 Nama Tugas: ")

    while True:
        try:
            jenis = input("🧩 Jenis Tugas (Normatif/Produktif): ").lower()
            if jenis in ["normatif", "produktif"]:
                break
        except:
            pass
        print("Masukkan jenis sesuai contoh!")

    while True:
        print("\nFormat waktu: DD-MM-YYYY HH:MM")
        deadline_str = input("⏰  Masukkan deadline (DD-MM-YYYY HH:MM): ").strip()
        try:
            deadline = datetime.datetime.strptime(deadline_str, "%d-%m-%Y %H:%M")
            if deadline < datetime.datetime.now():
                print("⚠️  Deadline tidak valid.")
            else:
                break
        except ValueError:
            print("⚠️  Format tanggal salah.")

    tugas_list.append({
        "nama": nama,
        "jenis": jenis,
        "deadline": deadline,
        "s2": False,
        "s1": False,
        "popup_shown": False,
        "overdue": False,
        "handled": False
    })

    print("\n✅ Tugas ditambahkan! Notifikasi akan berjalan otomatis.")
    time.sleep(3)


def simpan_tugas_ke_file(tugas_list, file_nama):
    with open(file_nama, "w", encoding="utf-8") as f:
        for tugas in tugas_list:
            f.write(f"{tugas['deadline']} | {tugas['nama']} \n")


def tampilkan_tugas(tugas_list):
    if not tugas_list:
        print("  (tidak ada)")
    else:
        for idx, tugas in enumerate(tugas_list, 1):
            print(f"  {idx}. {tugas['nama']} | Deadline: {tugas['deadline'].strftime('%d-%m-%Y %H:%M')}")


def lihat_daftar_tugas():
    while True:
        clear_screen()
        garis()
        print("📋  DAFTAR TUGAS")
        garis()
        print("1. ✅ Tugas Sudah Selesai")
        print("2. ❌ Tugas Belum Selesai")
        print("3. 📚 Tugas Aktif")
        print("4. 🔙 Kembali")
        garis()
        pilihan = input("Pilih opsi (1-4): ")

        if pilihan == "1":
            clear_screen()
            garis()
            print("✅ DAFTAR TUGAS SELESAI")
            garis()
            if os.path.exists(FILE_SELESAI):
                with open(FILE_SELESAI, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]

                if lines:
                    for line in lines:
                        print("✅", line)
                else:
                    print("(Kosong)")
            else:
                print("(Belum ada data tugas yang sudah selesai.)")
            input("\nTekan Enter untuk kembali...")

        elif pilihan == "2":
            clear_screen()
            garis()
            print("❌ DAFTAR TUGAS BELUM SELESAI")
            garis()

            tugas_belum_selesai = []
            if os.path.exists(FILE_BELUM):
                with open(FILE_BELUM, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                deadline, nama = line.split(" | ", 1)
                                tugas_belum_selesai.append({"nama": nama, "deadline": deadline})
                            except:
                                print(f"⚠️  Baris tidak valid: {line}")

            if not tugas_belum_selesai:
                print("KAMU TIDAK ADA DATA TUGAS BELUM SELESAI")
                input("\nTekan Enter untuk kembali...")
                continue

            for idx, t in enumerate(tugas_belum_selesai, 1):
                print(f"  {idx}. {t['nama']} | Deadline: {t['deadline']}")

            while True:
                if not tugas_belum_selesai:
                    print("\nKamu tidak ada tugas yang belum selesai.")
                    input("\nTekan Enter untuk kembali...")
                    break
                jawab = input("\nApakah ada tugas yang sudah selesai? (y/n): ").strip().lower()
                if jawab == "y":
                    nama_tugas = input("Nama tugas yang sudah selesai: ").strip()
                    for tugas in tugas_belum_selesai[:]:
                        if tugas["nama"].lower() == nama_tugas.lower():
                            tugas_belum_selesai.remove(tugas)
                            simpan_tugas_ke_file(tugas_belum_selesai, FILE_BELUM)
                            simpan_status(tugas["nama"], "selesai")
                            print(f"\n✅ Tugas '{nama_tugas}' telah dipindahkan ke tugas selesai.")
                            break
                    else:
                        print(f"\n⚠️  Tugas '{nama_tugas}' tidak ditemukan.")

                elif jawab == "n":
                    input("\nTekan Enter untuk kembali...")
                    break
                else :
                    print("Input tidak valid!")
                
        elif pilihan == "3":
            clear_screen()
            garis()
            print("📚 DAFTAR TUGAS AKTIF")
            garis()

            if not tugas_list:
                print("KAMU TIDAK ADA DATA TUGAS AKTIF")
                input("\nTekan Enter untuk kembali...")
                continue

            tampilkan_tugas(tugas_list)
            
            while True:
                if not tugas_list:
                    print("\nKamu tidak ada tugas yang aktif.")
                    input("\nTekan Enter untuk kembali...")
                    break
                jawab = input("\nApakah ada tugas yang sudah selesai? (y/n): ").strip().lower()
                if jawab == "y":
                    nama_tugas = input("Nama tugas mana yang sudah selesai: ").strip()
                    for tugas in tugas_list[:]:
                        if tugas["nama"].lower() == nama_tugas.lower():
                            now = datetime.datetime.now()
                            selisih = (tugas["deadline"] - now).total_seconds()

                            if selisih <= 0:
                                print(f"\n⏰ Deadline untuk '{nama_tugas}' sudah lewat.")
                                print("   Silakan konfirmasi melalui popup atau lanjutkan manual.")
                                tugas_list.remove(tugas)
                                simpan_status(tugas["nama"], "selesai")
                                tugas["handled"] = True
                                print(f"\n✅ Tugas '{nama_tugas}' telah dipindahkan ke tugas selesai.")
                                input("\nTekan Enter untuk kembali...")
                                break

                            elif selisih < 15:
                                print(f"\n⚠️  Waktumu sudah sangat dekat dengan deadline!")
                                print(f"   Tugas '{nama_tugas}' akan segera muncul di popup otomatis.")
                                print("   Harap tunggu notifikasi muncul, lalu konfirmasi di sana ya!")
                                input("\nTekan Enter untuk kembali...")
                                break

                            else:
                                tugas_list.remove(tugas)
                                simpan_status(tugas["nama"], "selesai")
                                tugas["handled"] = True
                                print(f"\n✅ Tugas '{nama_tugas}' telah dipindahkan ke tugas selesai.")
                                input("\nTekan Enter untuk kembali...")
                                break
                    else:
                        print(f"\n⚠️  Tugas '{nama_tugas}' tidak ditemukan.")
                        
                elif jawab == "n" :
                    input("\nTekan Enter untuk kembali...")
                    break
                else :
                    print("Input tidak valid!")

        elif pilihan == "4":
            break

        else:
            print("Masukkan pilihan yang benar (1-4).")
            time.sleep(1)


def parse_history_file(filepath):
    items = []
    if not os.path.exists(filepath):
        return items
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 2:
                waktu = parts[0].strip()
                nama = "|".join(parts[1:]).strip()
                try:
                    date = datetime.datetime.strptime(waktu, "%d-%m-%Y %H:%M")
                except:
                    continue
                items.append((date, nama))
    return items


def statistik_range(awal_date, akhir_date):
    selesai_items = parse_history_file(FILE_SELESAI)
    belum_items = parse_history_file(FILE_BELUM)
    selesai_count = sum(1 for dt, _ in selesai_items if awal_date <= dt.date() <= akhir_date)
    belum_count = sum(1 for dt, _ in belum_items if awal_date <= dt.date() <= akhir_date)
    total = selesai_count + belum_count
    return selesai_count, belum_count, total


def analisa_tugas():
    now = datetime.datetime.now()
    today = now.date()
    yesterday = (now - datetime.timedelta(days=1)).date()

    while True:
        clear_screen()
        header()
        print("📊 STATISTIK PRODUKTIVITAS")
        print(f"📅 Hari ini : {today.strftime('%d-%m-%Y')}")
        print("------------------------------------------")
        print("1. Lihat Statistik Hari Ini")
        print("2. Lihat Statistik Hari Kemarin")
        print("3. Pilih Rentang Tanggal")
        print("ENTER untuk kembali")
        pilihan = input("Pilih (1-3) atau ENTER: ").strip()

        if pilihan == "":
            break

        if pilihan == "1":
            selesai, belum, total = statistik_range(today, today)
            persentase = int((selesai / total) * 100) if total != 0 else 0
            panjang_bar = 10
            jumlah = int(round((persentase / 100) * panjang_bar))
            progress_bar = "[" + "#" * jumlah + " " * (panjang_bar - jumlah) + "]"

            clear_screen()
            header()
            print(f"📅 Statistik Hari Ini : {today.strftime('%d-%m-%Y')}")
            print("==================================")
            print(f"✅ Jumlah tugas selesai       : {progress_bar} {selesai}/{total}")
            print(f"❌ Jumlah tugas belum selesai : {belum}")
            print(f"📅 Total tugas tercatat       : {total}")
            print(f"🔥 Persentase produktivitas   : {persentase}%")

            if persentase >= 80:
                tips_ai = "🎉 Hebat! Disiplinmu luar biasa, pertahankan semangat ini!"
            elif persentase >= 50:
                tips_ai = "⚡ Cukup baik! Tapi masih bisa lebih teratur dan konsisten!"
            else:
                tips_ai = "💡 Masih banyak ruang berkembang. Yuk, mulai disiplin dari tugas kecil dulu!"

            print("\n💡 Tips AI:")
            print(tips_ai)
            input("\nTekan Enter untuk kembali...")

        elif pilihan == "2":
            selesai, belum, total = statistik_range(yesterday, yesterday)
            persentase = int((selesai / total) * 100) if total != 0 else 0
            panjang_bar = 10
            jumlah = int(round((persentase / 100) * panjang_bar))
            progress_bar = "[" + "#" * jumlah + " " * (panjang_bar - jumlah) + "]"

            clear_screen()
            header()
            print(f"📅 Statistik Hari Kemarin : {yesterday.strftime('%d-%m-%Y')}")
            print("==================================")
            print(f"✅ Jumlah tugas selesai       : {progress_bar} {selesai}/{total}")
            print(f"❌ Jumlah tugas belum selesai : {belum}")
            print(f"📅 Total tugas tercatat       : {total}")
            print(f"🔥 Persentase produktivitas   : {persentase}%")

            if persentase >= 80:
                tips_ai = "🎉 Hebat! Disiplinmu luar biasa, pertahankan semangat ini!"
            elif persentase >= 50:
                tips_ai = "⚡ Cukup baik! Tapi masih bisa lebih teratur dan konsisten!"
            else:
                tips_ai = "💡 Masih banyak ruang berkembang. Yuk, mulai disiplin dari tugas kecil dulu!"

            print("\n💡 Tips AI:")
            print(tips_ai)
            input("\nTekan Enter untuk kembali...")

        elif pilihan == "3":
            clear_screen()
            header()
            print("📆 Pilih rentang tanggal (format DD-MM-YYYY)")
            awal = input("Tanggal mulai (DD-MM-YYYY): ").strip()
            akhir = input("Tanggal akhir  (DD-MM-YYYY): ").strip()

            try:
                awal_date = datetime.datetime.strptime(awal, "%d-%m-%Y").date()
                akhir_date = datetime.datetime.strptime(akhir, "%d-%m-%Y").date()
            except:
                print("Format tanggal salah!")
                time.sleep(1)
                continue

            if akhir_date < awal_date:
                print("Tanggal akhir harus sama atau setelah tanggal mulai.")
                time.sleep(1)
                continue

            selesai, belum, total = statistik_range(awal_date, akhir_date)
            persentase = int((selesai / total) * 100) if total != 0 else 0
            panjang_bar = 10
            jumlah = int(round((persentase / 100) * panjang_bar))
            progress_bar = "[" + "#" * jumlah + " " * (panjang_bar - jumlah) + "]"

            clear_screen()
            header()
            hari_span = (akhir_date - awal_date).days + 1
            print(f"📅 Statistik {awal_date.strftime('%d-%m-%Y')} s/d {akhir_date.strftime('%d-%m-%Y')}  ({hari_span} hari)")
            print("==================================")
            print(f"✅ Jumlah tugas selesai       : {progress_bar} {selesai}/{total}")
            print(f"❌ Jumlah tugas belum selesai : {belum}")
            print(f"📅 Total tugas tercatat       : {total}")
            print(f"🔥 Persentase produktivitas   : {persentase}%")

            if persentase >= 80:
                tips_ai = "🎉 Hebat! Disiplinmu luar biasa, pertahankan semangat ini!"
            elif persentase >= 50:
                tips_ai = "⚡ Cukup baik! Tapi masih bisa lebih teratur dan konsisten!"
            else:
                tips_ai = "💡 Masih banyak ruang berkembang. Yuk, mulai disiplin dari tugas kecil dulu!"

            print("\n💡 Tips AI:")
            print(tips_ai)
            input("\nTekan Enter untuk kembali...")

        else:
            print("Pilihan salah.")
            time.sleep(1)


def main_menu():
    while True:
        header()
        print("1️⃣  Tambah & Monitor Tugas")
        print("2️⃣  Lihat Daftar Tugas")
        print("3️⃣  Analisis Produktivitas")
        print("4️⃣  Keluar")
        garis()
        pilih = input("Pilih menu (1-4): ")

        if pilih == "1":
            tambah_tugas()
        elif pilih == "2":
            lihat_daftar_tugas()
        elif pilih == "3":
            analisa_tugas()
        elif pilih == "4":
            garis()
            typewriter("🙏  TERIMA KASIH TELAH MENGGUNAKAN TEMAN NUGAS!", 0.02)
            typewriter("✨  Tetap produktif dan semangat selalu.", 0.02)
            global stop_thread
            stop_thread = True
            break
        else:
            print("Masukkan angka 1-4!")
            time.sleep(1)


if __name__ == "__main__":
    threading.Thread(target=notifikasi_deadline_loop, daemon=True).start()
    main_menu()