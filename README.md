Nama : Zoya

NPM : 2506620293

Kelas : PBP D 

pertanyaan reflektif tugas individu 1

1. Saya menggunakan beberapa elemen semantik seperti <header>, <main>, <section>, dan <footer>. Elemen-elemen ini membantu saya membagi website menjadi bagian-bagian yang lebih jelas. Misalnya, <header> untuk bagian atas dan navigasi, <main> untuk isi utama, dan <footer> untuk bagian bawah website.

2. Tantangan yang saya temukan adalah mengatur tata letak grid agar tetap rapi di berbagai ukuran layar. Tampilan yang terlihat bagus di desktop belum tentu terlihat sama di layar mobile. Karena itu, saya perlu mempertimbangkan ukuran gambar, teks, dan posisi setiap elemen agar informasi penting tetap mudah dilihat.

3. Karena website ini masih berupa static web, isi website belum bisa berubah atau memiliki banyak interaksi dengan pengguna. Jika dikembangkan lagi, saya ingin menambahkan fitur yang interaktif seperti slideshow agar pengunjung bisa berinteraksi langsung melalui website.

Dalam proses pembuatan website, saya menggunakan bantuan AI untuk membantu memahami cara membuat tampilan grid sesuai dengan desain yang saya inginkan, terutama dalam mengatur posisi gambar dan teks, serta cara untuk menambahkan font untuk memperbagus website. Saya juga menggunakan AI untuk membantu memahami cara menautkan link atau dokumen agar ketika diklik dapat mengarah ke halaman atau dokumen tujuan.

pertanyaan reflektif tugas individu 2

1. Ketika pengguna membuka halaman portofolio, urls.py proyek menerima URL lalu meneruskannya ke urls.py aplikasi main. Selanjutnya, view mengambil data dari model, memasukkannya ke context, lalu mengirimkannya ke template untuk ditampilkan sebagai halaman HTML di browser.

2. Data sebaiknya disimpan dalam model agar tidak perlu menulis setiap data secara langsung di HTML. Dengan begitu, data lebih mudah ditambah, diubah, atau dihapus tanpa harus mengubah struktur template, sehingga aplikasi lebih mudah dikembangkan.

3. makemigrations membuat file migrasi berdasarkan perubahan yang dilakukan pada model, sedangkan migrate menerapkan perubahan tersebut ke database. Contohnya, saat saya membuat model Project atau menambahkan field baru pada model, saya perlu menjalankan kedua perintah tersebut.

Saya menggunakan bantuan AI melalui platform ChatGPT untuk membantu memahami konsep Django, seperti model, view, template, routing, migration, dan unit testing. AI juga membantu memberikan panduan saat memperbaiki error, memahami struktur kode, serta memberikan saran dalam pembuatan dan pengembangan halaman portofolio.

pertanyaan reflektif tugas individu 3

1. Kita menggunakan ModelForm karena form ini otomatis terhubung dengan model Django, jadi kita tidak perlu membuat semua input dan validasinya dari awal secara manual. ModelForm juga membantu memastikan data yang dimasukkan sesuai dengan aturan yang sudah dibuat di model. Sementara itu, {% csrf_token %} digunakan untuk melindungi form dari serangan CSRF (Cross-Site Request Forgery), sehingga Django bisa memastikan bahwa request benar-benar berasal dari website kita.

2. JSON lebih sering digunakan dalam aplikasi web modern karena formatnya lebih sederhana, ringan, dan mudah dibaca dibandingkan XML. JSON juga lebih mudah diproses oleh JavaScript dan cocok untuk pertukaran data antara frontend dan backend, sehingga banyak digunakan dalam API.

3. Saat view mengembalikan data portofolio dalam bentuk JSON, Django mengambil data dari model terlebih dahulu, kemudian data tersebut diserialize menjadi format yang bisa direpresentasikan sebagai JSON. Serialization diperlukan karena object atau query dari model Django tidak bisa langsung dikirim sebagai JSON. Setelah diserialize, data dapat dikirim melalui response dan dibaca oleh aplikasi atau frontend yang membutuhkan data tersebut.

Saya menggunakan bantuan AI melalui ChatGPT untuk membantu memahami konsep dan proses pengerjaan tugas, seperti pemahaman penggunaan ModelForm dan {% csrf_token %}, konsep JSON dan XML, serta proses serialization data Django menjadi JSON.
Selain itu, AI juga membantu dalam proses implementasi fitur pada website portofolio, seperti membuat halaman Education dengan fitur tambah, edit, dan hapus, mengatur URL, view, form, serta CSS.