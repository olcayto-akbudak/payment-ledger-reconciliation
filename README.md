# Ödeme ve Fatura Mutabakatı

**Depo adı:** `payment-ledger-reconciliation` · Python 3.12+ · bağımsız çalışır · dış paket gerekmez.

Belirsiz ödemeyi rastgele faturaya kapatmadan, ücret ve iade sonrası net tutarı izlemek.

## Teknik kapsam

Kısmi tahsis, çoklu referans, kuruş bazlı korunum. Bu depo çalıştırılabilir bir mühendislik laboratuvarıdır. Ağ erişimi, özel hesap veya gerçek müşteri verisi gerektirmez. Örneklerde kasıtlı hatalar da bulunur; BLOCK, REVIEW veya false sonucu bazı senaryolarda beklenen davranıştır.

## Hızlı başlangıç

Depo kökünde:

```bash
python -m unittest -v
python app.py demo
python app.py demo --input scenario.json --output custom-report.json
```

`sample-report.json` gerçekten çalıştırılmış örnek çıktıdır. Yeniden çalıştırma sonucu `report.json` olur. Zamanlama ölçümleri hariç sabit seed ve girdiyle tekrarlanabilir. Kurulum için `pip install` gerekmez.

## Mimari ve kararlar

İşlem hattı: Payment netting → eligible invoices → explicit allocation → currency controls.

Temel varsayım: Tutarlar tamsayı minor unit; açık referans yoksa yalnız bir uygun aday otomatik eşleşir.

Alan motoru ve komut satırı `app.py`, kabul senaryosu `scenario.json`, sınır ve hata testleri `test_core.py` içindedir. Yapılandırma veri sözleşmesi [data-contract.md](data-contract.md), ayrıntılı akış [architecture.md](architecture.md), işletim adımları [runbook.md](runbook.md) içinde açıklanır.

## Doğrulama ve değerlendirme

Testler yalnız örneğin çalışmasını kontrol etmez; projenin davranışına özgü kabul ve ret koşullarını sınar. Örnek senaryoda gözlenen sonuçlar [results.md](results.md) içinde kayıtlıdır. CI Python 3.12/3.13, Ubuntu/Windows için tanımlıdır; yerel doğrulama Python 3.12 üzerinde yapılmıştır. GitHub'da ilk push sonrasında CI ayrıca çalışmalıdır.

## Sınırlar ve üretime geçiş

Kur dönüşümü ve banka entegrasyonu yoktur; toleransla kapanan bakiyeler raporda görünmeye devam eder.

Bu sürümde otomatik canlı entegrasyon, kullanıcı kimlik doğrulama, izleme altyapısı ve gerçek veriyle performans garantisi yoktur. İş kuralları sentetik kabul senaryolarıyla görünür hale getirilmiştir. Üretime geçmeden örnek sözleşmeyi gerçek alanlarla eşleyin, aşağıdaki deneyleri uygulayın ve sonuçları sürümleyin.

## Zorlaştırma deneyleri

1. Bir ödemeyi 100 fatura referansına tahsis edip tutar korunumunu test edin.
2. Banka hareketi ve valör gününü ayrı alanlarla modelleyin.
3. İadelerin önceki allocation kayıtlarına referansını zorunlu tutun.
4. Döviz dönüşümünü kur sürümü ve yuvarlama hesabıyla ayrı ledger olarak ekleyin.

## GitHub'a taşıma

```bash
git init
git add .
git commit -m "Initial working analysis laboratory"
git branch -M main
git remote add origin https://github.com/olcayto-akbudak/payment-ledger-reconciliation.git
git push -u origin main
```

Kendi hesabınıza taşırken `olcayto-akbudak` alanını değiştirin. Hesap bilgisi veya erişim anahtarı kaynak koda koymayın. Çalışan kaynak kod, testler ve teknik belgeler bu depoda yayımlanmıştır.

## Depo yerleşimi

GitHub sürümü dosyaları depo kökünde tutar; `app.py` alan motorunu ve CLI girişini içerir. `test_core.py` doğrudan bu modülü test eder. Belgeler ve örnek veriler aynı kökte yer alır.
