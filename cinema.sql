-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 23 Apr 2024 pada 16.20
-- Versi server: 10.4.24-MariaDB
-- Versi PHP: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cinema`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `booking`
--

CREATE TABLE `booking` (
  `id_booking` varchar(15) NOT NULL,
  `id_user` varchar(11) NOT NULL,
  `id_schedule` varchar(10) NOT NULL,
  `id_drink` varchar(20) NOT NULL,
  `tanggal_booking` date NOT NULL,
  `jml_seat` tinyint(4) DEFAULT NULL,
  `total` int(25) NOT NULL,
  `qrcode` varchar(40) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(30) NOT NULL DEFAULT 'proses'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `carousel`
--

CREATE TABLE `carousel` (
  `id_carousel` int(11) NOT NULL,
  `nama_carousel` varchar(50) NOT NULL,
  `image_carousel` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `carousel`
--

INSERT INTO `carousel` (`id_carousel`, `nama_carousel`, `image_carousel`) VALUES
(1, 'Siksa Kubur', '171160633149812_925x527.jpg'),
(2, 'Banner Dua Hati Biru', 'BN202404151036241816.jpg'),
(3, 'Aespa World Tour', 'BN202404081021026400.jpg'),
(4, 'Banner Godzilla x Kong The New Empire', '171160641816969_925x527.jpg'),
(5, 'Banner Badrawuhi Di Desa Penari', '171194224929857_925x527.jpg');

-- --------------------------------------------------------

--
-- Struktur dari tabel `detail_booking`
--

CREATE TABLE `detail_booking` (
  `id_detail` int(11) NOT NULL,
  `id_booking` varchar(15) DEFAULT NULL,
  `no_seat` varchar(5) DEFAULT NULL,
  `id_seat` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `drink`
--

CREATE TABLE `drink` (
  `id_drink` varchar(20) NOT NULL,
  `drink_name` varchar(30) NOT NULL,
  `image_drink` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `drink`
--

INSERT INTO `drink` (`id_drink`, `drink_name`, `image_drink`) VALUES
('7 798062 545470', 'Club Air Mineral 600ml', 'club 600.png'),
('996006 856532', 'Frut Tea Blackcurrant 250ml', 'fruit tea 250.jpg'),
('996006 856869', 'Teh Botol Sosro 250ml', 'teh botol sosro 250.jpg');

-- --------------------------------------------------------

--
-- Struktur dari tabel `movies`
--

CREATE TABLE `movies` (
  `id_movie` varchar(10) NOT NULL,
  `title` varchar(255) NOT NULL,
  `sinopsis` longtext NOT NULL,
  `sutradara` varchar(100) NOT NULL,
  `penulis` varchar(75) NOT NULL,
  `produser` varchar(75) NOT NULL,
  `produksi` varchar(75) NOT NULL,
  `cast` varchar(150) NOT NULL,
  `genre` varchar(20) NOT NULL,
  `durasi` tinyint(11) NOT NULL,
  `rating` enum('SU','13+','17+') NOT NULL,
  `tanggal_rilis` date DEFAULT NULL,
  `tahun` varchar(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `movies`
--

INSERT INTO `movies` (`id_movie`, `title`, `sinopsis`, `sutradara`, `penulis`, `produser`, `produksi`, `cast`, `genre`, `durasi`, `rating`, `tanggal_rilis`, `tahun`) VALUES
('MV001', 'Godzilla x Kong: The New Empire', 'Godzilla dan Kong akan melawan kekuatan baru yang sangat berbahaya. Kedua raksasa kuno itu akan menghadapi ancaman besar dari dasar bumi. Ancaman yang bisa membuat Godzilla maupun Kong punah.', 'Adam Wingard', 'Terry Rossio, Simon Barrett, Jeremy Slater', 'Alex Garcia, Jon Jashni, Eric McLeod', 'Warner Bros. Pictures', 'Rebecca Hall, Dan Stevens, Kaylee Hottle, Fala Chen, Rachel House, Brian Tyree Henry, Alex Ferns, Mercy Cornwall, Nicola Crisa, Jordy Campbell', 'Action, Sci-Fi', 115, 'SU', '2024-03-07', '2024'),
('MV002', 'Exhuma', 'Sebuah keluarga kaya Korea yang bermukim di Los Angeles memanggil sepasang dukun muda (diperankan oleh Kim Go-eun dan Lee Do-hyun) untuk menyelamatkan bayi mereka yang baru lahir setelah mengalami sejumlah kejadian mistis. Dua dukun ini merasakan adanya bayangan gelap leluhur yang terikat di keluarga itu, dengan sebutan “Panggilan dari Kubur”. Untuk melakukan pembongkaran kubur dan melepaskan sang leluhur, mereka meminta bantuan pada peramal fengsui (diperankan oleh Choi Min-sik) dan petugas pemakaman (diperankan Yoo Hae-jin). Tanpa diduga, keempat orang ini menemukan kuburan tersebut berada di lokasi mencurigakan dekat sebuah desa terpencil di Korea. Pembongkaran kubur pun dilakukan, namun di saat bersamaan sesuatu yang jahat dari bawah kubur juga turut terlepas.\r\n\r\n', 'Jang Jae-hyun', 'Jang Jae-hyun', '-', 'Showbox', 'Lee Do-hyun, Kim Go-eun, Choi Min Sik, Yoo Hai-Jin, Jeon Jin-ki', 'Horror', 12, '13+', '2024-02-28', '2024'),
('MV003', 'Ghostbusters: Frozen Empire\r\n', 'Saat penemuan artefak kuno membuat kekuatan jahat muncul, para anggota Ghostbusters baik yang baru dan lama harus bekerja sama untuk melindungi rumah mereka dan menyelamakan dunia dari Zaman Es kedua.\r\n\r\n', 'Gil Kenan', 'Gil Kenan, Jason Reitman', 'Ivan Reitman, Jason Reitman, Jason Blumenfeld', 'Columbia Pictures', 'Mckenna Grace, Annie Potts, Carrie Coon, Paul Rudd, Finn Wolfhard, Bill Murray, Celeste O\'Connor, Patton Oswalt, Dan Aykroyd, Ernie Hudson, Kumail Nan', 'Adventure, Fantasy', 115, 'SU', '2024-03-20', '2024'),
('MV004', 'The Ministry of Ungentlemanly Warfare\r\n', 'Dari kisah nyata tentang unit Militer Inggris merekrut sekelompok kecil tentara berkemampuan khusus yang memiliki misi untuk menyerang pasukan Jerman di belakang garis musuh selama Perang Dunia II dengan cara-cara yang tidak biasa.\r\n\r\n', 'Guy Ritchie', 'Paul Tamasy, Eric Johnson, Arash Amel, Guy Ritchie', 'Ivan Atkinson, Jerry Bruckheimer, John Friedberg, Chad Oman', 'Lionsgate', 'Henry Cavill, Alan Ritchson, Alex Pettyfer, Eiza Gonzalez, Babs Olusanmokun, Cary Elwes, Hero Fiennes Tiffin, Henry Golding, Rory Kinnear, Til Schweig', 'Action, War', 120, '13+', '2024-04-19', '2024'),
('MV005', 'The First Omen', 'Seorang wanita muda Amerika dikirim ke Roma untuk memulai kehidupan pelayanan kepada gereja. Namun, ia menghadapi kegelapan dan konspirasi mengerikan yang menyebabkan dia mempertanyakan keimanannya.', 'Arkasha Stevenson', 'Tim Smith, Arkasha Stevenson, Keith Thomas', 'David S. Goyer, Keith Levine', '20th Century Studios', 'Bill Nighy, Nell Tiger Free, Sonia Braga, Maria Caballero, Charles Dance, Ralph Ineson, Andrea Arcangeli, Anton Alexander', 'Horror', 119, '17+', '2024-04-04', '2024'),
('MV006', 'SUGA | Agust D TOUR \'D-DAY\' THE MOVIE', 'Film konser penutupan SUGA BTS yang ditunggu-tunggu, SUGA│Agust D TOUR ‘D-DAY’ THE MOVIE memenuhi layar lebar di seluruh dunia! Sebagai akhir yang megah dari tur dunia, “SUGA | Agust D TOUR ‘D-DAY’ THE FINAL” menandai puncak dari 25 konser yang diadakan di 10 kota, yang membawa total penonton sebanyak 290,000 orang sepanjang turnya. Rasakan energi yang menyala-nyala dan kegemparan “D-DAY’ THE FINAL” di layar, Mulai dari suara indah yang melintasi batasan antara sebagai anggota “21st Century Pop Icon” BTS dan sebagai artis solo Agust D, penampilan yang menggetarkan, energi yang luar biasa, hingga penampilan duet spesial yang menampilkan anggota BTS lainnya, seperti RM, Jimin, dan Jung Kook.', 'Jun-Soo Park', '-', '-', 'HYBE', 'SUGA', 'Music', 84, '13+', '2024-04-05', '2024'),
('MV007', 'Badarawuhi di Desa Penari', 'Desa itu masih menyimpan misteri. Kepingan demi kepingan misteri terungkap, termasuk teror dari entitas paling ditakuti yaitu, BADARAWUHI.', 'Kimo Stamboel', 'Lele Leila', 'Manoj Punjabi', 'MD Pictures', 'Aulia Sarah, Maudy Effrosina, Jourdy Pranata, Claresta Taufan, Moh. Iqbal Sulaiman, Ardit Erwandha, Diding Boneng, Aming Sugandhi, Dinda Kanya Dewi, B', 'Horror', 122, '13+', '2024-04-11', '2024'),
('MV008', 'Dua Hati Biru', 'Kelanjutan kisah Dua Garis Biru, tentang Bima (Angga Yunanda) dan Dara (Aisha Nurra Datau) yang berusaha membangun rumah tangga dan jadi orangtua terbaik untuk Adam (Farrell Rafisqy) di antara perbedaan mereka kini.', 'Gina S Noer, Dinna Jasanti', 'Gina S Noer', 'Chand Parwez Servia, Gina S Noer, Riza, Sigit Pratama', 'Starvision, Wahana Kreator', 'Angga Yunanda, Aisha Nurra Datau, Farrell Rafisqy, Cut Mini, Arswendi Bening Swara, Lulu Tobing, Keanu Angelo, Maisha Kanna, Rachel Amanda, Shakira Ja', 'Drama', 106, '13+', '2024-04-17', '2024'),
('MV009', 'Kung Fu Panda 4\r\n', 'Setelah Po (Jack Black) ditunjuk untuk menjadi Pemimpin Spiritual Lembah Damai dia memiliki misi baru. Bersama Zhen (Awkwafina), seekor rubah cerdik, Po mengumpulkan pasukan baru untuk melawan Chameleon (Viola Davis), penyihir jahat yang mampu menyerap semua kekuatan dari penjahat yang ia panggil dan memungkinkannya untuk berubah wujud menjadi makhluk yang ia serap.', 'Mike Mitchell', 'Jonathan Aibel, Glenn Berger', 'Rebecca Huntley', 'Universal Pictures', 'Jack Black, Awkwafina, Viola Davis, Dustin Hoffman, James Hong, Bryan Cranston, Ian McShane, Ke Huy Quan', 'Animation, Adventure', 94, 'SU', '2024-03-03', '2024'),
('MV010', 'Siksa Kubur', 'Setelah kedua orang tuanya jadi korban bom bunuh diri, Sita (Faradina Mufti) jadi tidak percaya agama. Sejak saat itu, tujuan hidup Sita hanya satu: mencari orang yang paling berdosa dan ketika orang itu meninggal, Sita ingin ikut masuk ke dalam kuburannya untuk membuktikan bahwa siksa kubur tidak ada dan agama tidak nyata. Namun, tentunya ada konsekuensi yang mengerikan bagi mereka yang tak percaya.\r\n\r\n', 'Joko Anwar', 'Joko Anwar', 'Tia Hasibuan', 'Come And See Pictures', 'Faradina Mufti, Reza Rahadian, Widuri Puteri, Muzakki Ramdhan, Fachri Albar, Happy Salma, Slamet Rahardjo, Christine Hakim, Arswendy Bening Swara, Nin', 'Horor, Religi', 117, '17+', '2024-04-11', '2024'),
('MV011', 'Civil War', 'Berkisah tentang tim jurnalis yang melakukan perjalanan melintasi Amerika saat perang saudara melanda dunia. Tim jurnalis yang bertugas di militer berpacu dengan waktu untuk mencapai ibukota sebelum pemberontak menyerbu Gedung Putih.\r\n\r\n', 'Alex Garland', 'Alex Garland', 'Danny Cohen, Gregory Goodman', 'A24', 'Kirsten Dunst, Wagner Moura, Cailee Spaeny, Stephen McKinley Henderson, Sonoya Mizuno, Jefferson White, Nelson Lee, Karl Glusman', 'Action', 109, '17+', '2024-04-12', '2024'),
('MV012', 'Cash Out', 'Mason (John Travolta) adalah pencuri profesional yang melakuan perampokan bank terbesar bersama kelompoknya. Saat terjadi kesalahan, mereka terjebak di dalam bank yang dikelilingi oleh penegak hukum. Ketegangan semakin meningkat saat Mason harus bernegosiasi dengan Amelia (Kristin Davis) yang juga adalah mantan kekasihnya.\r\n\r\n', 'Ives', 'Dipo Oseni, Doug Richardson', 'Cecil Chambers, Joel Cohen', 'Convergence Entertainment Group', 'John Travolta, Kristin Davis, Lukas Haas, Quavo, Victorya Brandart, oel Cohen, Matt Gerald, Jake Ellenz, Luis Da Silva Jr.', 'Action', 90, '13+', '2024-04-26', '2924'),
('MV626', 'THE FALL GUY', 'Colt Seavers (Ryan Gosling) adalah seorang stuntman yang selalu ingin terlihat bagus di depan kamera. Sampai akhirnya ia terlibat sebuah masalah saat sang bintang utama hilang dari lokasi syuting film yang sedang disutradarai oleh mantan kekasihnya, Jody Moreno (Emily Blunt).', ' David Leitch', 'Drew Pearce, Glen A. Larson', '-', 'Universal Pictures', 'Ryan Gosling, Emily Blunt, Hannah Waddingham', 'Action', 126, '13+', '2024-05-03', '2024');

-- --------------------------------------------------------

--
-- Struktur dari tabel `poster_image`
--

CREATE TABLE `poster_image` (
  `id_poster` int(11) NOT NULL,
  `id_movie` varchar(10) NOT NULL,
  `poster_name` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `poster_image`
--

INSERT INTO `poster_image` (`id_poster`, `id_movie`, `poster_name`) VALUES
(1, 'MV001', '170980638065259_287x421.jpg'),
(2, 'MV002', '170952883924109_287x421.jpg'),
(3, 'MV003', '170989317187253_287x421.jpg'),
(4, 'MV004', '171212554991891_287x421.jpg'),
(5, 'MV005', '171082526078534_287x421.jpg'),
(6, 'MV006', '171143761960946_287x421.jpg'),
(7, 'MV007', '171196601780400_287x421.jpg'),
(8, 'MV008', '17109994074491_287x421.jpg'),
(9, 'MV009', '170833695317395_287x421.jpg'),
(10, 'MV010', '170989335367119_290x426.jpg'),
(11, 'MV011', '171074852832328_287x421.jpg'),
(12, 'MV012', '171231691019411_287x421.jpg'),
(18, 'MV626', '24009900.jpg');

-- --------------------------------------------------------

--
-- Struktur dari tabel `schedule`
--

CREATE TABLE `schedule` (
  `id_schedule` varchar(10) NOT NULL,
  `id_movie` varchar(10) NOT NULL,
  `id_theaters` varchar(10) NOT NULL,
  `tanggal_schedule` date NOT NULL,
  `jam` varchar(5) NOT NULL,
  `studio` enum('1','2','3') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `theaters`
--

CREATE TABLE `theaters` (
  `id_theaters` varchar(10) NOT NULL,
  `nama_theaters` varchar(45) NOT NULL,
  `alamat_theaters` varchar(120) NOT NULL,
  `no_telp` varchar(15) DEFAULT NULL,
  `price1` enum('25000','30000') NOT NULL,
  `price2` enum('30000','35000') NOT NULL,
  `price3` enum('35000','40000') NOT NULL,
  `region` enum('36','32','33','35','60','19') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `theaters`
--

INSERT INTO `theaters` (`id_theaters`, `nama_theaters`, `alamat_theaters`, `no_telp`, `price1`, `price2`, `price3`, `region`) VALUES
('BDWKLS', 'NSC Bondowoso', 'Jl. KIS Mangun Sarkoro No.78 Bondowoso Jawa Timur 68216', '0332-5553714', '25000', '30000', '35000', '35'),
('BJGODF', 'NSC Bojonegoro', 'Jl. Hayam Wuruk No. 74 Karangpacar – Bojonegoro Jawa Timur 62117', '0353-3412701', '25000', '30000', '35000', '35'),
('BJROIG', 'NSC Banjar', 'Baninza Mall Lantai 2, Jl. R.Hamara Efendi, Hegarsari – Pataruman, Banjar, Jawa Barat 46322', '0265-7549124', '25000', '30000', '35000', '32'),
('BLTVGD', 'NSC Belitung', 'Jl. Pilang Desa Dukong Kec. Tanjung Pandan, Kab. Belitung, Kepulauan Bangka Belitung 33417 (Perum Meirobieland)', '-', '25000', '30000', '35000', '19'),
('BYGKJF', 'NSC Banyuwangi', 'Jl. Nusantara 9 Kampung Mandar Arah Pantai Boom Banyuwangi Jawa Timur 68413 ', '0333-416192', '25000', '30000', '35000', '35'),
('CMSJDF', 'NSC Ciamis', 'Ciamis Mall Lantai 2, Jl. Jend. Ahmad Yani 15 Ciamis\r\nJawa Barat 46211', '0265-771351', '25000', '30000', '35000', '32'),
('GTGXDV', 'NSC Genteng', 'Jl. Diponegoro No.11 Genteng – Banyuwangi Jawa Timur 68411 ', '0333-8502397', '25000', '30000', '35000', '35'),
('JBGXJI', 'NSC Jombang', 'Jl. KH. Wahid Hasyim 3C Candi Mulyo Jombang Jawa Timur 61411', '0353-3412701', '25000', '30000', '35000', '35'),
('KDLIO', 'NSC Kendal', 'Aneka Jaya Swalayan, Jl. Soekarno Hatta 362\r\nManggisan, Langenharjo, Kendal,\r\nJawa Tengah 51314', '-', '25000', '30000', '35000', '33'),
('KDSJAS', 'NSC Kudus', 'Jl. AKBP Agil Kusumadya, Tanggulangin, Jati Wetan, Kec. Jati, Kabupaten Kudus, Jawa Tengah 59346', '0291-424768', '25000', '30000', '35000', '33'),
('KPJCNV', 'NSC Kepanjen', 'Jl. Raya Talang Agung 78, Rekesan Kepanjen Malang, Jawa Timur 65163', '0341-3901212', '25000', '30000', '35000', '35'),
('KTBNDT', 'NSC Kotabaru', 'Jl. Raya Stagen – Sei Taib Kotabaru 72113 Pulau Laut – Kalimantan Selatan ', '0518-2611369', '25000', '30000', '35000', '60'),
('LMNDFN', 'NSC Lamongan', 'Lamongan Plaza Lt.3\r\nJl. Panglima Sudirman 27, Sidokumpul Lamongan Jawa Timur 62213', '0322-3101648', '25000', '30000', '35000', '35'),
('NGAISH', 'NSC Ngawi', 'Jl. Dr. Radjiman No.33, Dadapan, Klitik, Ngawi Jawa Timur 63271', '0351-400032', '25000', '30000', '35000', '35'),
('NGJBVN', 'NSC Nganjuk', 'Jl. Raya Nganjuk Kediri No.234 Loceret Jawa Timur 64471 ', '0358-3510845', '25000', '30000', '35000', '35'),
('NSC05', 'NSC Demak', 'Tanubayan, Bintoro, Kec. Demak, Kabupaten Demak, Jawa Tengah 59511', '0291-6913922', '25000', '30000', '35000', '33'),
('NSC06', 'NSC Pati ', 'Jl. Raya Pati - Kudus No.KM 4, Margorejo, Kec. Margorejo, Kabupaten Pati, Jawa Tengah 59163', '0295-4103426', '25000', '30000', '35000', '33'),
('PRGIDB', 'NSC Purbalingga', 'Jl. Ahmad Yani No. 31 Purbalingga Jawa Tengah 53312', '0281-6580727', '25000', '30000', '35000', '33'),
('PSRNRD', 'NSC Pasuruan', 'Jl. Soekarno Hatta No.1 Komplek BCA Pasuruan, Jawa Timur 67134', '0343-420024', '25000', '30000', '35000', '35'),
('PWJHSO', 'NSC Purworejo', 'Jl. KH. Ahmad Dahlan 150, Tegalmalang, Purworejo, Jawa Tengah 54151', '-', '25000', '30000', '35000', '33'),
('RKBJDF', 'NSC Rangkasbitung', 'Jl. R.T. Hardiwinangun Plaza Rabinza\r\nBanten 42314', '0252-5555276', '30000', '35000', '40000', '36'),
('SBGLAI', 'NSC Subang', 'Jl. Brigjen Katamso 18A, Dangdeur-Ciereng\r\nPlanet Waterboom Lt. 2 Jawa Barat 41212', '-', '25000', '30000', '35000', '32'),
('SLTSFP', 'NSC Salatiga', 'Jl. Imam Bonjol No.34, Sidorejo Lor (Aneka Jaya Dept. Store) Sidorejo, Salatiga – Jawa Tengah 50714', '0821-3864-2050', '25000', '30000', '35000', '33'),
('SMPJSF', 'NSC Sumenep', 'Jl. Raya Gapura No.6 (Kompleks Pertokoan An Nur) Sumenep – Madura 69412', '0328-6774559', '25000', '30000', '35000', '35'),
('TBNBFD', 'NSC Tuban', 'Jl. Basuki Rachmad No. 215-217 Ronggomulyo Tuban Jawa Timur 62315', '0356-8830379', '25000', '30000', '35000', '35'),
('TMGOSD', 'NSC Temanggung', 'Jl. MT. Haryono No.68 Temanggung Jawa Tengah 56213', '0293-4962534', '25000', '30000', '35000', '33'),
('TRGSJF', 'NSC Trenggalek', 'Gedung Serba Guna Kelutan Jl. Soekarno Hatta No. 91 Ngasinan, Kelutan, Trenggalek Jawa Timur 66313', '-', '25000', '30000', '35000', '35'),
('WSBIJF', 'NSC Wonosobo', 'Jl. Seruni No.3 Kampung Karangkajen, Wonosobo Timur Jawa Tengah 56314 (Depan Bima Music)', '-', '25000', '30000', '35000', '33');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id_user` varchar(11) NOT NULL,
  `nama` varchar(75) NOT NULL,
  `username` varchar(75) NOT NULL,
  `email` varchar(75) NOT NULL,
  `tanggal_lahir` date NOT NULL,
  `no_telp` varchar(15) DEFAULT NULL,
  `gender` enum('Pria','Wanita') DEFAULT NULL,
  `provinsi` int(11) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `pin` int(6) DEFAULT NULL,
  `alamat` varchar(100) DEFAULT NULL,
  `level_user` enum('1','2','3') DEFAULT '3'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id_user`, `nama`, `username`, `email`, `tanggal_lahir`, `no_telp`, `gender`, `provinsi`, `password`, `pin`, `alamat`, `level_user`) VALUES
('1', 'admin', 'admin', 'admin@xyz.com', '1996-04-09', '0', 'Pria', 1, '$2b$12$0uHvtBLhr42VBC9xLSrc2ujwvRx/lhVp1gL3pPS9ii3vv0YPF85j6', 123456, 'admin', '1'),
('11997611216', 'Ahmad', 'ahmad', 'ahmad@xyz.com', '1997-01-01', '2147483647', 'Pria', NULL, '$2b$12$m8DW.wUawd6vfm4/383Hk.Hqt1MGt5Wt9rYAkurf82ZiK2nFxSgcC', 123456, 'bantul', '2'),
('120014976', 'Aryanto', 'yanto', 'arya@xyz.com', '2001-01-01', '083245930235', 'Pria', NULL, '$2b$12$sjQYW8TUjMPiELNfrdHKpuN2MMJam3Z4cyiI/8zBMKwIb1YV4S3nG', NULL, 'Jl. Jenderal Sudirman, Yogyakarta', '3'),
('420040098', 'Daffa Ferdinan', 'Daffa', 'daffa@xyz.com', '2004-04-16', '085323532356', 'Pria', NULL, '$2b$12$htr61NrIj.ZvPij1gEBagu3p.nCGoJNEFAsgamvdcTMj0elvNC3X.', NULL, 'Cirebon Kota', '1'),
('619961819', 'Mamat', 'Mat', 'mamat@xyz.com', '1996-06-14', '0852123456789', 'Pria', NULL, '$2b$12$pZ3pD24iAv4/OoFJDrlPuuiN1ywO4PaxIpjKYZlH//YONZ3R8vxIO', NULL, 'Sleman', '2');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`id_booking`),
  ADD KEY `id_user` (`id_user`) USING BTREE,
  ADD KEY `id_schedule` (`id_schedule`),
  ADD KEY `id_drink` (`id_drink`);

--
-- Indeks untuk tabel `carousel`
--
ALTER TABLE `carousel`
  ADD PRIMARY KEY (`id_carousel`);

--
-- Indeks untuk tabel `detail_booking`
--
ALTER TABLE `detail_booking`
  ADD PRIMARY KEY (`id_detail`),
  ADD KEY `id_booking` (`id_booking`) USING BTREE;

--
-- Indeks untuk tabel `drink`
--
ALTER TABLE `drink`
  ADD PRIMARY KEY (`id_drink`);

--
-- Indeks untuk tabel `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`id_movie`);

--
-- Indeks untuk tabel `poster_image`
--
ALTER TABLE `poster_image`
  ADD PRIMARY KEY (`id_poster`),
  ADD UNIQUE KEY `id_movie` (`id_movie`);

--
-- Indeks untuk tabel `schedule`
--
ALTER TABLE `schedule`
  ADD PRIMARY KEY (`id_schedule`),
  ADD KEY `id_film` (`id_movie`) USING BTREE,
  ADD KEY `id_theaters` (`id_theaters`) USING BTREE;

--
-- Indeks untuk tabel `theaters`
--
ALTER TABLE `theaters`
  ADD PRIMARY KEY (`id_theaters`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `carousel`
--
ALTER TABLE `carousel`
  MODIFY `id_carousel` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `detail_booking`
--
ALTER TABLE `detail_booking`
  MODIFY `id_detail` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `poster_image`
--
ALTER TABLE `poster_image`
  MODIFY `id_poster` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`id_drink`) REFERENCES `drink` (`id_drink`),
  ADD CONSTRAINT `booking_ibfk_3` FOREIGN KEY (`id_schedule`) REFERENCES `schedule` (`id_schedule`);

--
-- Ketidakleluasaan untuk tabel `detail_booking`
--
ALTER TABLE `detail_booking`
  ADD CONSTRAINT `detail_booking_ibfk_1` FOREIGN KEY (`id_booking`) REFERENCES `booking` (`id_booking`);

--
-- Ketidakleluasaan untuk tabel `poster_image`
--
ALTER TABLE `poster_image`
  ADD CONSTRAINT `poster_image_ibfk_1` FOREIGN KEY (`id_movie`) REFERENCES `movies` (`id_movie`);

--
-- Ketidakleluasaan untuk tabel `schedule`
--
ALTER TABLE `schedule`
  ADD CONSTRAINT `schedule_ibfk_1` FOREIGN KEY (`id_movie`) REFERENCES `movies` (`id_movie`),
  ADD CONSTRAINT `schedule_ibfk_2` FOREIGN KEY (`id_theaters`) REFERENCES `theaters` (`id_theaters`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
