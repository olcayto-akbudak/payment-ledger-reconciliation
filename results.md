# Çalıştırılmış kabul sonuçları

Python 3.12.14, sentetik `scenario.json`; yerel test sayısı **8**, tümü başarılı. Ham test günlüğü `test-log.txt`.

2 tahsis, 1 inceleme; para korunum kontrolleri: [{'currency': 'TRY', 'net_minor': 23000, 'allocated_minor': 18000, 'unallocated_minor': 5000}]

Sonuçlar yalnız bu örneğe aittir; üretim doğruluğu veya performans garantisi olarak yorumlanmamalıdır. Ölçülen iş sonucunu kontrol edin; örnek negatif vaka içeriyorsa ret beklenir. Tam çıktı `sample-report.json`.

## Sınanan davranışlar

| Test | Kontrol |
|---|---|
| `test_ambiguity` | ambiguity |
| `test_cash_conservation` | cash conservation |
| `test_explicit_multi` | explicit multi |
| `test_duplicate` | duplicate |
| `test_negative_fee` | negative fee |
| `test_cross_currency` | cross currency |
| `test_partial` | partial |
| `test_invalid_reference` | invalid reference |

## Gelişmiş deney planı

1. Bir ödemeyi 100 fatura referansına tahsis edip tutar korunumunu test edin.
2. Banka hareketi ve valör gününü ayrı alanlarla modelleyin.
3. İadelerin önceki allocation kayıtlarına referansını zorunlu tutun.
4. Döviz dönüşümünü kur sürümü ve yuvarlama hesabıyla ayrı ledger olarak ekleyin.
