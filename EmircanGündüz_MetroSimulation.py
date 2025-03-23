from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx  # İstasyon kimliği (kırmızı hat, mavi hat gibi)
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}  # idx: Istasyon kimliği
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)  # hangi hatta hangi istasyonlar var

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur
        Parametreler:
            baslangic_id: Başlangıç istasyonunun kimliği
            hedef_id: Hedef istasyonunun kimliği
        Dönüş:
            Eğer rota bulunursa, istasyon listesi döndürülür, aksi halde None döndürülür
        """
        baslangic_istasyon = self.istasyonlar[baslangic_id]
        
        queue = deque()
        queue.append((baslangic_id, baslangic_istasyon.hat, 0, [baslangic_istasyon])) # istasyon, mevcut hat, aktarma sayısı, rota
        # ziyaret edilen istasyonları en az kaç aktarmayla ziyaret edildiğini tutar 
        # istasyon id : aktarma sayısı
        ziyaret_edilen = {}

        while queue:
            istasyon_id, hat, aktarma_sayisi, rota = queue.popleft()
            # daha az ya da eşit veya daha önce ziyaret ettiysek devam ediyoruz  
            if istasyon_id in ziyaret_edilen and aktarma_sayisi >= ziyaret_edilen[istasyon_id]:
                continue
            ziyaret_edilen[istasyon_id] = aktarma_sayisi # mevcut istasyonun aktarma sayısı
            # eğer hedefe ulaştıysak rotayı döndürüyoruz
            if istasyon_id == hedef_id:
                return rota 
            
            for komsu, _ in self.istasyonlar[istasyon_id].komsular: # şuanki istasyonun bütün komşularını geziyoruz
                # daha önce ziyaret edilmediyse ya da şuanki versiyonunda daha az aktarma sayısı varsa bu rota kuyruğa eklenir
                if komsu.idx not in ziyaret_edilen or aktarma_sayisi < ziyaret_edilen[komsu.idx]:
                    yeni_aktarma_sayisi = aktarma_sayisi
                    # hat değişikliği varsa hat sayısını arttırıyoruz
                    if komsu.hat != hat:
                        yeni_aktarma_sayisi += 1
                    queue.append((komsu.idx, komsu.hat, yeni_aktarma_sayisi, rota + [komsu]))
        return None #kuyruk tamamen bitmiş fakat hedefe ulaşamamışsak None döndürüyoruz
 


    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur
        
        Parametreler:
            baslangic_id: Başlangıç istasyonunun kimliği
            hedef_id: Hedef istasyonunun kimliği
        Dönüş:
            Eğer rota bulunursa, istasyon listesi ve toplam sürenin tuple'ı döndürülür, aksi halde None döndürülür
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar: #istasyonları kontrol edip eğer yoksa none döndürüyoruz
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # öncelik kuyruğu: (f_değeri, toplam_sure, id, istasyon, rota)
        öncelik = []
        heapq.heappush(öncelik, (0, 0, id(baslangic), baslangic, [baslangic]))

        # ziyaret edilen istasyonları o istasyona ulaşmak için geçen süre ile tutar
        ziyaret_edilen = {}
        
        while öncelik:
            # kuyruktan en düşük f değer elemanını çıkarıyoruz
            _, toplam_sure, _, şuanki_istasyon, rota = heapq.heappop(öncelik) # en düşük toplam süre + heuristik değerli rota
            
            # daha önce ziyaret ettiysek ve ziyaret süresi daha önceki ziyaretten daha kısa veya eşitse bu istasyonu atlıyoruz
            if şuanki_istasyon.idx in ziyaret_edilen and toplam_sure >= ziyaret_edilen[şuanki_istasyon.idx]:
                continue
            
            # mevcut istasyona ulaşmamız için gereken süreyi tutar 
            ziyaret_edilen[şuanki_istasyon.idx] = toplam_sure
            
            # eğer hedef istasyona ulaştıysak rotayı ve toplam süreyi döndürüyoruz
            if şuanki_istasyon.idx == hedef_id:
                return rota, toplam_sure
            
            for komsu, sure in şuanki_istasyon.komsular: #şuanki istasyonun komşularını geziyoruz
                yeni_toplam_sure = toplam_sure + sure #komşuya giderken geçen süreyi hesaplıyoruz

                heuristik = 0 # 0 olarak almamızın sebebi, 
                # Dijkstra gibi çalışmasını ve daha garanti olması amacıyla hepsine bakmasını istememiz.
                f_degeri = yeni_toplam_sure + heuristik

                yeni_rota = rota + [komsu] #mevcut rotaya komşu rotayı da ekliyoruz 

                heapq.heappush(öncelik, (f_degeri, yeni_toplam_sure, komsu.idx, komsu,  yeni_rota))
        
        return None # eğer yolları tamamladık fakat hedefe ulaşamadıysak none döndürüyoruz
                
# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 