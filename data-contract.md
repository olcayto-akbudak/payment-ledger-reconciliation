# Girdi ve çıktı sözleşmesi

UTF-8 JSON nesnesi; örnek dosya alanların tam iç içe yapısını gösterir. Zamanlar bu laboratuvarda sayısal sanal zaman/gün değeridir; saat dilimi dönüşümü yapılmaz.

| Üst alan | Tür | Örnek |
|---|---|---|
| `invoices` | `list` | [{'id': 'I1', 'customer': 'C1', 'currency': 'TRY', 'day': 1, 'amount_minor': 10000}, {'id': 'I2', 'customer': 'C1', 'currency': 'TRY', 'day': 2, 'amount_minor': |
| `payments` | `list` | [{'id': 'P1', 'customer': 'C1', 'currency': 'TRY', 'day': 3, 'amount_minor': 5000, 'invoice_refs': []}, {'id': 'P2', 'customer': 'C1', 'currency': 'TRY', 'day': |

## Semantik

Tutarlar tamsayı minor unit; açık referans yoksa yalnız bir uygun aday otomatik eşleşir.

Alan motorunun doğrulamaları `app.py` içinde açıkça bulunur. Eksik zorunlu anahtarlar hata verir. Satır bazında karantina/bulgu üreten motorlar rapora yazar; yapısal konfigürasyon hataları işlemi keser. Tam JSON Schema dosyası bu sürümün kapsamında değildir.

## Çıktı

Gerçek çıktı şeması ve örnek değerler `sample-report.json` içinde yer alır. Örnek işleme özgü sonuçlar `results.md` içinde açıklanır. Dış tüketici alan adlarını ve birimleri değiştirmeden sözleşmeyi sürümlemelidir.
