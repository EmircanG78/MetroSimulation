# 🚇 Sürcüsüz Metro Simülasyonu - Rota Optimizasyonu

## 📄 Proje Açıklaması
Bu proje, bir metro ağında iki istasyon arasındaki **en hızlı** ve **en az aktarmalı** rotayı bulan bir simülasyon geliştirmeyi amaçlamaktadır. Graf veri yapısı kullanılarak modellenen metro ağında, **BFS (Breadth-First Search)** algoritması ile en az aktarma yapılan rota, **A* algoritması** ile en hızlı rota bulunur.

Gerçek dünya problemlerini algoritmik düşünce ile çözme becerilerini geliştirmek hedeflenmiştir.

---

## ⚙️ Kullanılan Teknolojiler ve Kütüphaneler

- **Python 3.x**  
  Proje Python programlama dili kullanılarak geliştirilmiştir.

- **collections**  
  - `defaultdict`: Metro ağı grafını oluştururken, her istasyonun komşu listelerini dinamik ve varsayılan olarak yönetmek için kullanılmıştır.  
  - `deque`: BFS algoritmasında kuyruk veri yapısını hızlı ve verimli şekilde oluşturmak için tercih edilmiştir.

- **heapq**  
  A* algoritmasında öncelikli kuyruk (priority queue) işlemlerini yönetmek için kullanılmıştır. Bu, en hızlı rotayı bulmak adına en düşük maliyetli rotayı önceliklendirir.

- **typing**  
  - `Dict`, `List`, `Set`, `Tuple`, `Optional`: Fonksiyonların parametreleri ve dönüş değerleri için tip ipuçları verilerek kodun okunabilirliği ve sürdürülebilirliği artırılmıştır.

---

## 📌 Algoritmaların Çalışma Mantığı

### 1. **Breadth-First Search (BFS) Algoritması**
- **Amaç**: İki istasyon arasındaki **en az aktarma** yapılan rotayı bulur.
- **Nasıl Çalışır?**  
  BFS algoritması graf üzerinde katman katman gezinerek en kısa (aktarma sayısı açısından) yolu bulur. Kuyruk (queue) yapısı kullanılır ve her istasyon sırasıyla işlenir. İlk ulaşılan hedef istasyon, en az aktarma içeren rotayı temsil eder.

- **Neden BFS?**  
  Aktarma sayısına odaklanan durumlarda en kısa yol bulunması için uygun bir algoritmadır.

### 2. **A\* (A-Star) Algoritması**
- **Amaç**: İki istasyon arasındaki **en hızlı** rotayı bulur.
- **Nasıl Çalışır?**  
  A* algoritması, her rotanın toplam süresini dikkate alarak en kısa süreli yolu önceliklendirir. Heuristic fonksiyonlar ve öncelik kuyruğu kullanılarak hedef istasyona en hızlı ulaşımı sağlar.

- **Neden A\*?**  
  En hızlı yolu bulmada performanslıdır. Hem gerçek maliyeti (geçilen yolların süreleri), hem de tahmini maliyeti (hedefe olan uzaklık/süre) dikkate alır.

- **Kodda Kullanılma Şekli**  
  A* algoritmasından en iyi şekilde verim almak için vektörlerle çalışmak daha iyidir. Fakat kod içinde vektörler verilmediği ve vektörleri rastgele atayamayacağım (hata çıkma olasılığı yüksek) için A* algoritmasının heuristik değerini 0'a ayarladım. Heuristik değerinin 0'a ayarlanmasıyla birlikte A* algoritması Dijkstra algoritması gibi davranır. Yani daha yavaş ve güvenli.

---

## 🚀 Projeyi Çalıştırma ve Örnek Kullanım

### Çalıştırma Adımları

1. Proje dosyasını bilgisayarınıza indirin.
2. Terminal veya Komut Satırı'nda bulunduğunuz dizini proje dosyasının olduğu klasöre getirin.
3. Aşağıdaki komut ile çalıştırın:

```bash
python dosya_adi.py
```

> Örneğin dosya adı `metro_simulation.py` ise:
```bash
python metro_simulation.py
```

---

### Kullanım Senaryosu

Kod çalıştırıldığında, sabit olarak belirlenmiş istasyonlar üzerinden rotalar hesaplanır ve sonuçlar ekrana yazdırılır.

Örneğin:

```
Senaryo 1: AŞTİ'den OSB'ye:
En az aktarmalı rota: M1 -> K4
En hızlı rota (15 dakika): M1 -> K4
```

Kod içerisinde başlangıç ve bitiş noktaları şu şekilde sabit olarak verilmiştir:

```python
rota = metro.en_az_aktarma_bul("M1", "K4")
sonuc = metro.en_hizli_rota_bul("M1", "K4")
```

Kendi istasyonlarınızı test etmek için bu değerleri değiştirebilirsiniz.

---

### Testler ve Doğrulamalar

- Farklı başlangıç ve bitiş istasyonları için kod üzerinde değişiklik yaparak test edebilirsiniz.
- Rota mantığının ve sürelerin doğru hesaplandığını kontrol edin.

---

## 💡 Geliştirme Fikirleri

- Metro haritasının görselleştirilmesi (matplotlib, networkx)
- Metroların geliş ve bekleme süre bilgilerinin eklenmesi
- Gerçek zamanlı verilerle sistemin sürekli güncellenmesi
- A* algoritmasından tam verim alınabilmesi için duraklara vektör eklenmesi
- Farklı şehirlerin metro haritalarının eklenmesi (veri seti genişletmek için)

---

## 🔗 Kaynaklar
- [GeeksforGeeks - BFS](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)
- [RedBlobGames - A*](https://www.redblobgames.com/pathfinding/a-star/introduction/)
- [Python Collections Module](https://docs.python.org/3/library/collections.html)
- [Python Heapq Module](https://docs.python.org/3/library/heapq.html)
- [ChatGPT - Algoritmaların çalışma mantığını öğrenme ve kaynak araştırmalarında destek için](https://openai.com/chatgpt)

---